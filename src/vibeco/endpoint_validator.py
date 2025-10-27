# Agent Guide
# Agent Guide
# Purpose: Provide the core endpoint validation engine that discovers API routes, probes
#          capabilities, and reports regressions for remote services.
# Notes: Designed for reuse by the CLI and automated workflows; keep helper functions
#        deterministic and side-effect free to simplify unit testing.

"""Endpoint discovery and validation utilities for remote API surfaces."""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from datetime import datetime
from html.parser import HTMLParser
from typing import Any, Iterable
from urllib.parse import urljoin, urlparse
import logging

import yaml
import requests
from requests import Response
from requests.exceptions import RequestException, Timeout

LOGGER = logging.getLogger(__name__)

SAFE_METHODS = {"GET", "HEAD", "OPTIONS"}
DESTRUCTIVE_METHODS = {"POST", "PUT", "PATCH", "DELETE"}
COMMON_SPEC_PATHS = [
    "/openapi.json",
    "/openapi.yaml",
    "/swagger.json",
    "/swagger/v1/swagger.json",
    "/v3/api-docs",
    "/v3/api-docs.json",
]
COMMON_PREFIXES = [
    "/api",
    "/api/v1",
    "/api/v2",
    "/v1",
    "/v2",
    "/v1/api",
    "/v2/api",
]
JSON_LIKE_TYPES = ("application/json", "+json")
STREAMING_CONTENT_TYPES = ("text/event-stream",)


@dataclass(frozen=True)
class EndpointDefinition:
    """Describe a single method/path pair that should be validated."""

    method: str
    path: str
    source: str
    schema: dict[str, Any] | None = None
    content_type: str | None = None

    def is_destructive(self) -> bool:
        return self.method.upper() in DESTRUCTIVE_METHODS

    def absolute_url(self, base_url: str) -> str:
        return urljoin(base_url.rstrip("/") + "/", self.path.lstrip("/"))


@dataclass
class EndpointResult:
    """Capture the outcome of a single endpoint probe."""

    method: str
    path: str
    url: str
    status_code: int | None
    latency: float | None
    ok: bool
    flagged: bool
    reason: str
    excerpt: str
    likely_cause: str
    suggested_fix: str
    ignored: bool = False
    content_type: str | None = None


@dataclass
class EndpointValidationReport:
    """Aggregate the validator run into structured metadata and per-endpoint results."""

    base_url: str
    generated_at: str
    results: list[EndpointResult]
    failures: list[EndpointResult]
    allowlisted_failures: list[EndpointResult]

    def to_json(self) -> dict[str, Any]:
        return {
            "base_url": self.base_url,
            "generated_at": self.generated_at,
            "results": [result.__dict__ for result in self.results],
            "failures": [result.__dict__ for result in self.failures],
            "allowlisted_failures": [result.__dict__ for result in self.allowlisted_failures],
        }


@dataclass
class ValidatorConfig:
    """Runtime options controlling discovery, execution, and reporting."""

    base_url: str
    headers: dict[str, str] = field(default_factory=dict)
    seeds: list[str] = field(default_factory=list)
    include_destructive: bool = False
    timeout: float = 10.0
    max_retries: int = 2
    backoff_factor: float = 1.5
    concurrency: int = 4
    rate_limit_per_second: float = 4.0
    allowlist: set[tuple[str, str]] = field(default_factory=set)


class RateLimiter:
    """Simple token-based rate limiter shared across worker threads."""

    def __init__(self, rate_per_second: float) -> None:
        self._interval = 1.0 / rate_per_second if rate_per_second > 0 else 0.0
        self._lock = threading.Lock()
        self._last_time = 0.0

    def acquire(self) -> None:
        with self._lock:
            if self._interval <= 0:
                self._last_time = time.monotonic()
                return
            now = time.monotonic()
            wait = self._interval - (now - self._last_time)
            if wait > 0:
                time.sleep(wait)
            self._last_time = time.monotonic()


class _LinkExtractor(HTMLParser):
    """Collect href and src attributes from HTML documents."""

    def __init__(self) -> None:
        super().__init__()
        self.links: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for attr, value in attrs:
            if attr in {"href", "src"} and value:
                self.links.add(value)


def normalize_path(candidate: str, base_url: str) -> str | None:
    parsed = urlparse(candidate)
    if parsed.scheme and parsed.netloc:
        # Ensure the link belongs to the base host
        base = urlparse(base_url)
        if parsed.netloc != base.netloc:
            return None
        path = parsed.path or "/"
    else:
        path = candidate
    if not path:
        return None
    if not path.startswith("/"):
        path = "/" + path
    return path


def extract_api_like_paths(paths: Iterable[str]) -> set[str]:
    api_paths = set()
    for path in paths:
        lowered = path.lower()
        if "/api" in lowered or lowered.startswith("/v"):
            api_paths.add(path)
    return api_paths


def parse_allow_header(response: Response) -> set[str]:
    header = response.headers.get("Allow", "")
    return {method.strip().upper() for method in header.split(",") if method.strip()}


def infer_request_body(schema: dict[str, Any] | None) -> tuple[Any | None, str | None]:
    """Generate a minimal JSON-like payload from an OpenAPI schema."""

    if not schema:
        return {}, "application/json"

    if "example" in schema:
        return schema["example"], "application/json"

    schema_type = schema.get("type")
    if schema_type == "object":
        properties = schema.get("properties", {})
        required = schema.get("required", list(properties.keys()))
        payload: dict[str, Any] = {}
        for name in required:
            prop_schema = properties.get(name, {})
            value, _ = infer_request_body(prop_schema)
            payload[name] = value
        return payload, "application/json"
    if schema_type == "array":
        items = schema.get("items")
        if not items:
            return [], "application/json"
        value, _ = infer_request_body(items)
        return [value], "application/json"
    if schema_type == "string":
        return schema.get("default", ""), "application/json"
    if schema_type == "integer":
        return schema.get("default", 0), "application/json"
    if schema_type == "number":
        return schema.get("default", 0), "application/json"
    if schema_type == "boolean":
        return schema.get("default", False), "application/json"

    return {}, "application/json"


def classify_failure(response: Response | None, error: str | None, json_issue: bool) -> tuple[bool, str, str, str]:
    """Derive failure classification metadata."""

    if error:
        likely = "Request timeout" if "timeout" in error.lower() else "Network or connection issue"
        fix = "Verify connectivity and endpoint availability"
        reason = error
        return True, reason, likely, fix

    if response is None:
        return True, "No response received", "Request did not return a response", "Investigate upstream availability"

    status = response.status_code
    status_reason = f"{status} {response.reason}"
    if status in {404, 405}:
        likely = "Endpoint missing or method not allowed"
        fix = "Confirm routing configuration and update the validator seeds if needed"
        return True, status_reason, likely, fix
    if 500 <= status < 600:
        likely = "Server-side error triggered during validation"
        fix = "Check service logs for exceptions and harden input validation"
        return True, status_reason, likely, fix
    if json_issue:
        likely = "Successful response without valid JSON"
        fix = "Return structured JSON or extend the allowlist if intentional"
        return True, f"{status_reason} (invalid JSON)", likely, fix

    return False, status_reason, "", ""


class EndpointValidator:
    """Core orchestration class executing endpoint discovery and validation."""

    def __init__(self, config: ValidatorConfig) -> None:
        self.config = config
        self._rate_limiter = RateLimiter(config.rate_limit_per_second)
        self._thread_local = threading.local()

    # Session management -------------------------------------------------
    def _session(self) -> requests.Session:
        session = getattr(self._thread_local, "session", None)
        if session is None:
            session = requests.Session()
            if self.config.headers:
                session.headers.update(self.config.headers)
            self._thread_local.session = session
        return session

    # Discovery ----------------------------------------------------------
    def discover_endpoints(self) -> list[EndpointDefinition]:
        discovered: dict[tuple[str, str], EndpointDefinition] = {}
        session = self._session()

        for spec_endpoint in self._discover_from_openapi(session):
            key = (spec_endpoint.method, spec_endpoint.path)
            discovered[key] = spec_endpoint

        generic_paths: set[str] = set(self.config.seeds)
        generic_paths.update(self._discover_from_sitemap(session))
        generic_paths.update(self._discover_from_html(session))
        generic_paths.update(COMMON_PREFIXES)

        for path in sorted(generic_paths):
            normalized = normalize_path(path, self.config.base_url)
            if not normalized:
                continue
            existing = any(key[1] == normalized for key in discovered)
            if existing:
                continue
            for endpoint in self._expand_methods_via_options(session, normalized):
                key = (endpoint.method, endpoint.path)
                discovered.setdefault(key, endpoint)

        return sorted(discovered.values(), key=lambda item: (item.path, item.method))

    def _discover_from_openapi(self, session: requests.Session) -> list[EndpointDefinition]:
        endpoints: list[EndpointDefinition] = []
        for spec_path in COMMON_SPEC_PATHS:
            url = urljoin(self.config.base_url.rstrip("/") + "/", spec_path.lstrip("/"))
            try:
                response = session.get(url, timeout=self.config.timeout)
            except RequestException as exc:
                LOGGER.debug("Unable to fetch spec %s: %s", url, exc)
                continue
            if not response.ok:
                continue
            try:
                document = response.json()
            except ValueError:
                try:
                    document = yaml.safe_load(response.text)
                except yaml.YAMLError:
                    continue
            paths_section = document.get("paths") if isinstance(document, dict) else None
            if not isinstance(paths_section, dict):
                continue
            for path, methods in paths_section.items():
                if not isinstance(methods, dict):
                    continue
                normalized = normalize_path(path, self.config.base_url)
                if not normalized:
                    continue
                for method, details in methods.items():
                    if not isinstance(details, dict):
                        continue
                    method_upper = method.upper()
                    if method_upper not in SAFE_METHODS.union(DESTRUCTIVE_METHODS):
                        continue
                    request_body = details.get("requestBody", {})
                    content_type, schema = self._extract_schema(request_body)
                    endpoints.append(
                        EndpointDefinition(
                            method=method_upper,
                            path=normalized,
                            source=f"openapi:{spec_path}",
                            schema=schema,
                            content_type=content_type,
                        )
                    )
        return endpoints

    def _extract_schema(self, request_body: dict[str, Any]) -> tuple[str | None, dict[str, Any] | None]:
        content = request_body.get("content")
        if not isinstance(content, dict):
            return None, None
        for content_type, body in content.items():
            if not isinstance(body, dict):
                continue
            if any(marker in content_type for marker in JSON_LIKE_TYPES):
                schema = body.get("schema") if isinstance(body.get("schema"), dict) else body.get("schema")
                if isinstance(schema, dict):
                    return content_type, schema
        # Fallback to first entry
        for content_type, body in content.items():
            schema = body.get("schema") if isinstance(body, dict) else None
            if isinstance(schema, dict):
                return content_type, schema
        return None, None

    def _discover_from_sitemap(self, session: requests.Session) -> set[str]:
        url = urljoin(self.config.base_url.rstrip("/") + "/", "sitemap.xml")
        try:
            response = session.get(url, timeout=self.config.timeout)
        except RequestException:
            return set()
        if not response.ok:
            return set()
        try:
            import xml.etree.ElementTree as ET

            tree = ET.fromstring(response.text)
        except ET.ParseError:
            return set()
        paths = {
            normalize_path(loc.text or "", self.config.base_url)
            for loc in tree.findall(".//{*}loc")
            if loc.text
        }
        return {path for path in paths if path}

    def _discover_from_html(self, session: requests.Session) -> set[str]:
        try:
            response = session.get(self.config.base_url, timeout=self.config.timeout)
        except RequestException:
            return set()
        if not response.ok or not response.text:
            return set()
        parser = _LinkExtractor()
        parser.feed(response.text)
        paths = {
            normalize_path(link, self.config.base_url)
            for link in parser.links
        }
        return extract_api_like_paths({path for path in paths if path})

    def _expand_methods_via_options(self, session: requests.Session, path: str) -> list[EndpointDefinition]:
        url = urljoin(self.config.base_url.rstrip("/") + "/", path.lstrip("/"))
        try:
            response = session.options(url, timeout=self.config.timeout)
        except RequestException:
            return []
        allowed = parse_allow_header(response)
        endpoints: list[EndpointDefinition] = []
        for method in allowed:
            if method not in SAFE_METHODS.union(DESTRUCTIVE_METHODS):
                continue
            endpoints.append(
                EndpointDefinition(
                    method=method,
                    path=path,
                    source="options",
                )
            )
        if not endpoints and response.ok and response.status_code != 405:
            # OPTIONS succeeded but did not advertise methods; default to GET
            endpoints.append(
                EndpointDefinition(
                    method="GET",
                    path=path,
                    source="options-fallback",
                )
            )
        return endpoints

    # Execution ----------------------------------------------------------
    def should_skip(self, endpoint: EndpointDefinition) -> bool:
        return endpoint.is_destructive() and not self.config.include_destructive

    def _prepare_payload(
        self, endpoint: EndpointDefinition
    ) -> tuple[dict[str, str], Any | None, Any | None]:
        headers: dict[str, str] = {}
        json_payload: Any | None = None
        data_payload: Any | None = None

        if endpoint.schema or endpoint.method in {"POST", "PUT", "PATCH"}:
            payload, inferred_type = infer_request_body(endpoint.schema)
            if isinstance(payload, (dict, list)):
                json_payload = payload
            elif payload is not None:
                data_payload = payload
            content_type = endpoint.content_type or inferred_type or "application/json"
            if content_type:
                headers["Content-Type"] = content_type
        return headers, json_payload, data_payload

    def _evaluate_response(self, response: Response | None, error: str | None) -> tuple[bool, str, str, str, bool]:
        json_issue = False
        if response is not None:
            if 200 <= response.status_code < 300 and response.status_code not in {204, 205}:
                content_type = response.headers.get("Content-Type", "")
                if any(marker in content_type for marker in JSON_LIKE_TYPES):
                    text = response.text.strip()
                    if not text:
                        json_issue = True
                    else:
                        try:
                            parsed = response.json()
                        except ValueError:
                            json_issue = True
                        else:
                            if parsed in ({}, [], None):
                                json_issue = True
        flagged, reason, likely, fix = classify_failure(response, error, json_issue)
        return flagged, reason, likely, fix, json_issue

    def _read_excerpt(self, response: Response | None) -> tuple[str, str | None]:
        if response is None:
            return "", None
        content_type = response.headers.get("Content-Type")
        if content_type and any(ct in content_type for ct in STREAMING_CONTENT_TYPES):
            for line in response.iter_lines(decode_unicode=True):
                if line:
                    return line[:200], content_type
            return "", content_type
        body = response.text if response.text else ""
        return body[:200].replace("\n", " ").replace("|", "\\|").strip(), content_type

    def _execute_endpoint(self, endpoint: EndpointDefinition) -> EndpointResult:
        url = endpoint.absolute_url(self.config.base_url)
        attempt = 0
        response: Response | None = None
        error: str | None = None
        start_time: float | None = None
        latency: float | None = None
        while attempt <= self.config.max_retries:
            self._rate_limiter.acquire()
            session = self._session()
            headers, json_payload, data_payload = self._prepare_payload(endpoint)
            request_headers = headers.copy()
            try:
                start_time = time.monotonic()
                response = session.request(
                    endpoint.method,
                    url,
                    timeout=self.config.timeout,
                    json=json_payload,
                    data=None if json_payload is not None else data_payload,
                    headers=request_headers,
                    stream=True,
                )
                latency = time.monotonic() - start_time
                error = None
                break
            except Timeout as exc:
                latency = time.monotonic() - start_time if start_time else None
                error = f"Timeout after {self.config.timeout}s"
                if attempt == self.config.max_retries:
                    break
                time.sleep(self.config.backoff_factor * (2**attempt))
            except RequestException as exc:  # pragma: no cover - network edge case
                latency = time.monotonic() - start_time if start_time else None
                error = str(exc)
                if attempt == self.config.max_retries:
                    break
                time.sleep(self.config.backoff_factor * (2**attempt))
            attempt += 1

        try:
            excerpt, content_type = self._read_excerpt(response)
        finally:
            if response is not None:
                response.close()
        flagged, reason, likely, fix, json_issue = self._evaluate_response(response, error)
        status_code = response.status_code if response is not None else None
        ok = response.ok if response is not None else False

        return EndpointResult(
            method=endpoint.method,
            path=endpoint.path,
            url=url,
            status_code=status_code,
            latency=latency,
            ok=ok and not flagged,
            flagged=flagged,
            reason=reason,
            excerpt=excerpt,
            likely_cause=likely,
            suggested_fix=fix,
            content_type=content_type,
        )

    # Public API ---------------------------------------------------------
    def run(self) -> EndpointValidationReport:
        endpoints = [endpoint for endpoint in self.discover_endpoints() if not self.should_skip(endpoint)]

        results: list[EndpointResult] = []
        with concurrent_executor(self.config.concurrency) as executor:
            futures = [executor.submit(self._execute_endpoint, endpoint) for endpoint in endpoints]
            for future in futures:
                result = future.result()
                allowlisted = (result.method, result.path) in self.config.allowlist
                if allowlisted and result.flagged:
                    result.ignored = True
                results.append(result)

        failures = [res for res in results if res.flagged and not res.ignored]
        allowlisted_failures = [res for res in results if res.flagged and res.ignored]
        report = EndpointValidationReport(
            base_url=self.config.base_url,
            generated_at=datetime.utcnow().isoformat() + "Z",
            results=results,
            failures=failures,
            allowlisted_failures=allowlisted_failures,
        )
        return report

    def build_markdown_report(self, report: EndpointValidationReport) -> str:
        header = [
            "## Endpoint validation report",
            f"- Base URL: {report.base_url}",
            f"- Generated: {report.generated_at}",
            f"- Total endpoints checked: {len(report.results)}",
            f"- Failures: {len(report.failures)}",
        ]
        if report.allowlisted_failures:
            header.append(f"- Allowlisted failures: {len(report.allowlisted_failures)}")
        lines = header + ["", "| Method | Path | Status | Latency (s) | Excerpt | Likely cause | Suggested fix |", "| --- | --- | --- | --- | --- | --- | --- |"]
        if not report.failures and not report.allowlisted_failures:
            lines.append("| ✅ | No failures detected | | | | | |")
        else:
            for result in report.results:
                if not result.flagged:
                    continue
                status = result.status_code or "N/A"
                latency = f"{result.latency:.2f}" if result.latency is not None else "-"
                badge = "(allowlisted)" if result.ignored else ""
                excerpt = result.excerpt or ""
                lines.append(
                    f"| {result.method} | {result.path} | {status} {badge} | {latency} | {excerpt} | {result.likely_cause} | {result.suggested_fix} |"
                )
        return "\n".join(lines) + "\n"


class concurrent_executor:
    """Context manager returning a thread pool with graceful shutdown."""

    def __init__(self, workers: int) -> None:
        from concurrent.futures import ThreadPoolExecutor

        self._executor = ThreadPoolExecutor(max_workers=max(1, workers))

    def __enter__(self):
        return self._executor

    def __exit__(self, exc_type, exc, tb) -> None:
        self._executor.shutdown(wait=True)


def load_allowlist(path: str | None) -> set[tuple[str, str]]:
    if not path:
        return set()
    with open(path, "r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    allowlist: set[tuple[str, str]] = set()
    if isinstance(data, list):
        for entry in data:
            if not isinstance(entry, dict):
                continue
            method = entry.get("method")
            route = entry.get("path")
            if isinstance(method, str) and isinstance(route, str):
                allowlist.add((method.upper(), route))
    return allowlist


def run_validator(config: ValidatorConfig) -> EndpointValidationReport:
    validator = EndpointValidator(config)
    return validator.run()
