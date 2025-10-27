# Agent Guide
# Purpose: Validate helper functions and reporting logic for the endpoint validator engine.
# Key Targets:
#   - infer_request_body(): ensures schema-driven payload synthesis works for nested objects.
#   - normalize_path()/extract_api_like_paths(): confirm discovery filters only API candidates.
#   - EndpointValidator.build_markdown_report(): verifies failure summarisation.
#   - load_allowlist(): checks allowlisted endpoints are normalised.

from __future__ import annotations

from pathlib import Path
import sys

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT = PROJECT_ROOT / "src"
for candidate in (PROJECT_ROOT, SRC_ROOT):
    if str(candidate) not in sys.path:
        sys.path.insert(0, str(candidate))

from vibeco.endpoint_validator import (
    EndpointDefinition,
    EndpointResult,
    EndpointValidationReport,
    EndpointValidator,
    ValidatorConfig,
    extract_api_like_paths,
    infer_request_body,
    load_allowlist,
    normalize_path,
)


def test_infer_request_body_for_object_schema() -> None:
    schema = {
        "type": "object",
        "required": ["name", "count"],
        "properties": {
            "name": {"type": "string", "default": "example"},
            "count": {"type": "integer"},
            "optional": {"type": "boolean", "default": True},
        },
    }

    payload, content_type = infer_request_body(schema)

    assert payload == {"name": "example", "count": 0}
    assert content_type == "application/json"


def test_normalize_path_filters_external_links() -> None:
    base = "https://api.example.com"

    assert normalize_path("/api/v1/items", base) == "/api/v1/items"
    assert normalize_path("https://api.example.com/v2/status", base) == "/v2/status"
    assert normalize_path("https://other.example.com/api", base) is None


def test_extract_api_like_paths_only_returns_api_routes() -> None:
    paths = {"/docs", "/api/v1/health", "/V2/users"}

    assert extract_api_like_paths(paths) == {"/api/v1/health", "/V2/users"}


def test_build_markdown_report_highlights_failures() -> None:
    config = ValidatorConfig(base_url="https://api.example.com")
    validator = EndpointValidator(config)
    result = EndpointResult(
        method="GET",
        path="/api/v1/items",
        url="https://api.example.com/api/v1/items",
        status_code=404,
        latency=0.2,
        ok=False,
        flagged=True,
        reason="404 Not Found",
        excerpt="",
        likely_cause="Endpoint missing or method not allowed",
        suggested_fix="Confirm routing configuration and update the validator seeds if needed",
    )
    report = EndpointValidationReport(
        base_url=config.base_url,
        generated_at="2025-01-01T00:00:00Z",
        results=[result],
        failures=[result],
        allowlisted_failures=[],
    )

    markdown = validator.build_markdown_report(report)

    assert "Endpoint validation report" in markdown
    assert "GET" in markdown and "/api/v1/items" in markdown
    assert "404" in markdown


def test_load_allowlist_from_yaml(tmp_path: Path) -> None:
    path = tmp_path / "allowlist.yaml"
    path.write_text(
        yaml.safe_dump([
            {"method": "get", "path": "/api/v1/items"},
            {"method": "POST", "path": "/api/v1/create"},
        ]),
        encoding="utf-8",
    )

    allowlist = load_allowlist(str(path))

    assert allowlist == {("GET", "/api/v1/items"), ("POST", "/api/v1/create")}


def test_validator_skip_destructive_by_default() -> None:
    config = ValidatorConfig(base_url="https://api.example.com")
    validator = EndpointValidator(config)
    endpoint = EndpointDefinition(method="DELETE", path="/api/v1/items/1", source="test")

    assert validator.should_skip(endpoint) is True

    validator_allow = EndpointValidator(ValidatorConfig(base_url="https://api.example.com", include_destructive=True))
    assert validator_allow.should_skip(endpoint) is False
