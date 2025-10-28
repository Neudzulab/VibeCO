# Agent Guide
# Purpose: Command-line interface for the endpoint validator, wiring configuration files,
#          CLI flags, and reporting outputs for local runs and CI workflows.
# Notes: Keep parsing logic declarative and avoid implicit defaults so CI behaviour stays
#        predictable and auditable.

"""CLI entry point for the VibeCO endpoint validator."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from vibeco.endpoint_validator import (
    EndpointValidator,
    ValidatorConfig,
    build_batch_markdown_report,
    load_allowlist,
    render_markdown_report,
    run_batch,
)


def _parse_header(value: str) -> tuple[str, str]:
    if ":" not in value:
        raise argparse.ArgumentTypeError("Headers must follow 'Name: Value' format")
    name, raw_value = value.split(":", 1)
    return name.strip(), raw_value.strip()


def _load_config_file(path: Path | None) -> dict[str, Any]:
    if not path:
        return {}
    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found: {path}")
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError("Configuration file must contain a mapping at the top level")
    return data


def _merge_headers(base: dict[str, str], additions: list[tuple[str, str]]) -> dict[str, str]:
    headers = dict(base)
    for name, value in additions:
        headers[name] = value
    return headers


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Discover and validate API endpoints for a remote service.",
    )
    parser.add_argument("--base-url", help="Root URL for the API (e.g. https://api.example.com)")
    parser.add_argument("--config", type=Path, help="Optional YAML configuration file.")
    parser.add_argument("--header", action="append", type=_parse_header, help="Additional request header (repeatable)")
    parser.add_argument(
        "--seed",
        action="append",
        default=None,
        help="Seed path (e.g. /v1/health) to ensure the validator probes it (repeatable)",
    )
    parser.add_argument(
        "--include-destructive",
        action="store_true",
        help="Also execute potentially destructive methods (POST/PUT/PATCH/DELETE).",
    )
    parser.add_argument("--timeout", type=float, help="Request timeout in seconds")
    parser.add_argument("--retries", type=int, help="Maximum number of retries per endpoint")
    parser.add_argument("--backoff", type=float, help="Backoff factor between retries")
    parser.add_argument("--concurrency", type=int, help="Maximum concurrent requests")
    parser.add_argument("--rate-limit", type=float, help="Requests per second limit")
    parser.add_argument(
        "--allowlist",
        type=Path,
        help="YAML file containing method/path pairs to treat as known exceptions.",
    )
    parser.add_argument("--label", help="Optional label identifying the target service or gateway.")
    parser.add_argument(
        "--report",
        type=Path,
        help="Where to write the Markdown report (default: reports/endpoint_report.md)",
    )
    parser.add_argument(
        "--json",
        type=Path,
        help="Where to write the machine-readable JSON report (default: reports/endpoint_report.json)",
    )
    return parser


def _coalesce(value: Any, fallback: Any) -> Any:
    return value if value is not None else fallback


def _merge_defaults(defaults: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged: dict[str, Any] = {k: v for k, v in defaults.items() if k not in {"headers", "seeds"}}
    for key, value in override.items():
        if key in {"headers", "seeds"}:
            continue
        merged[key] = value

    headers: dict[str, str] = {}
    if isinstance(defaults.get("headers"), dict):
        headers.update(defaults["headers"])
    if isinstance(override.get("headers"), dict):
        headers.update(override["headers"])
    merged["headers"] = headers

    seeds: list[str] = []
    if isinstance(defaults.get("seeds"), list):
        seeds.extend(defaults["seeds"])
    if isinstance(override.get("seeds"), list):
        seeds.extend(override["seeds"])
    merged["seeds"] = list(dict.fromkeys(seeds)) if seeds else []

    return merged


def _build_validator_config_from_mapping(mapping: dict[str, Any]) -> ValidatorConfig:
    base_url = mapping.get("base_url")
    if not isinstance(base_url, str) or not base_url:
        raise ValueError("Each target must define a non-empty base_url")

    headers = mapping.get("headers") if isinstance(mapping.get("headers"), dict) else {}
    seeds = list(mapping.get("seeds", [])) if isinstance(mapping.get("seeds"), list) else []
    allowlist_path = mapping.get("allowlist")
    allowlist = load_allowlist(str(allowlist_path)) if allowlist_path else set()

    timeout_value = mapping.get("timeout")
    timeout = float(timeout_value) if timeout_value is not None else 10.0
    retries_value = mapping.get("max_retries")
    max_retries = int(retries_value) if retries_value is not None else 2
    backoff_value = mapping.get("backoff_factor")
    backoff_factor = float(backoff_value) if backoff_value is not None else 1.5
    concurrency_value = mapping.get("concurrency")
    concurrency = int(concurrency_value) if concurrency_value is not None else 4
    rate_limit_value = mapping.get("rate_limit_per_second")
    rate_limit = float(rate_limit_value) if rate_limit_value is not None else 4.0

    label = mapping.get("label") or mapping.get("name")

    return ValidatorConfig(
        base_url=base_url,
        headers=headers,
        seeds=seeds,
        include_destructive=bool(mapping.get("include_destructive", False)),
        timeout=timeout,
        max_retries=max_retries,
        backoff_factor=backoff_factor,
        concurrency=concurrency,
        rate_limit_per_second=rate_limit,
        allowlist=allowlist,
        label=label,
    )


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    config_data = _load_config_file(args.config) if args.config else {}

    targets_data = config_data.get("targets") if isinstance(config_data.get("targets"), list) else None
    if targets_data:
        conflicting = []
        if args.base_url:
            conflicting.append("--base-url")
        if args.seed:
            conflicting.append("--seed")
        if args.header:
            conflicting.append("--header")
        if args.allowlist:
            conflicting.append("--allowlist")
        if args.label:
            conflicting.append("--label")
        if args.include_destructive:
            conflicting.append("--include-destructive")
        if args.timeout is not None:
            conflicting.append("--timeout")
        if args.retries is not None:
            conflicting.append("--retries")
        if args.backoff is not None:
            conflicting.append("--backoff")
        if args.concurrency is not None:
            conflicting.append("--concurrency")
        if args.rate_limit is not None:
            conflicting.append("--rate-limit")
        if conflicting:
            parser.error(
                "Configuration with multiple targets does not accept CLI overrides: "
                + ", ".join(conflicting)
            )

    report_path = args.report or Path(config_data.get("report", "reports/endpoint_report.md"))
    json_path = args.json or Path(config_data.get("json", "reports/endpoint_report.json"))

    if targets_data:
        defaults = config_data.get("defaults") if isinstance(config_data.get("defaults"), dict) else {}
        configs: list[ValidatorConfig] = []
        for target in targets_data:
            if not isinstance(target, dict):
                parser.error("Each entry under targets must be a mapping")
            merged = _merge_defaults(defaults, target)
            try:
                config = _build_validator_config_from_mapping(merged)
            except ValueError as exc:  # pragma: no cover - defensive guard
                parser.error(str(exc))
            configs.append(config)

        if not configs:
            parser.error("No valid targets discovered in the configuration file")

        batch_report = run_batch(configs)
        markdown = build_batch_markdown_report(batch_report)

        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(markdown, encoding="utf-8")

        json_path.parent.mkdir(parents=True, exist_ok=True)
        json_path.write_text(json.dumps(batch_report.to_json(), indent=2), encoding="utf-8")

        if batch_report.total_failures:
            print(
                f"❌ Endpoint validation detected {batch_report.total_failures} regression(s) "
                f"across {len(batch_report.reports)} service(s). See {report_path} for details."
            )
            return 1

        if batch_report.total_allowlisted:
            print(
                f"⚠️ Endpoint validation matched {batch_report.total_allowlisted} allowlisted failure(s)."
                f" Review {report_path} to confirm they remain acceptable."
            )
        else:
            print(
                f"✅ Endpoint validation succeeded for {len(batch_report.reports)} service(s)."
                f" Report saved to {report_path}."
            )
        return 0

    base_url = args.base_url or config_data.get("base_url")
    if not base_url:
        parser.error("--base-url is required unless provided via the configuration file")

    headers_from_file = config_data.get("headers") if isinstance(config_data.get("headers"), dict) else {}
    cli_headers = args.header or []
    headers = _merge_headers(headers_from_file, cli_headers)

    seeds = list(config_data.get("seeds", [])) if isinstance(config_data.get("seeds"), list) else []
    if args.seed:
        seeds.extend(args.seed)

    allowlist_path = args.allowlist or config_data.get("allowlist")
    allowlist = load_allowlist(str(allowlist_path)) if allowlist_path else set()

    config = ValidatorConfig(
        base_url=base_url,
        headers=headers,
        seeds=seeds,
        include_destructive=_coalesce(args.include_destructive, config_data.get("include_destructive", False)),
        timeout=_coalesce(args.timeout, config_data.get("timeout", 10.0)),
        max_retries=_coalesce(args.retries, config_data.get("max_retries", 2)),
        backoff_factor=_coalesce(args.backoff, config_data.get("backoff_factor", 1.5)),
        concurrency=_coalesce(args.concurrency, config_data.get("concurrency", 4)),
        rate_limit_per_second=_coalesce(args.rate_limit, config_data.get("rate_limit_per_second", 4.0)),
        allowlist=allowlist,
        label=_coalesce(args.label, config_data.get("label")),
    )

    validator = EndpointValidator(config)
    report = validator.run()
    markdown = render_markdown_report(report)

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(markdown, encoding="utf-8")

    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report.to_json(), indent=2), encoding="utf-8")

    if report.failures:
        print(f"❌ Endpoint validation detected {len(report.failures)} regression(s). See {report_path} for details.")
        return 1

    if report.allowlisted_failures:
        print(
            f"⚠️ Endpoint validation matched {len(report.allowlisted_failures)} allowlisted failure(s)."
            f" Review {report_path} to confirm they remain acceptable."
        )
    else:
        print(f"✅ Endpoint validation succeeded. Report saved to {report_path}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
