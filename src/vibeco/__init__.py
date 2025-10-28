# Agent Guide
# Purpose: Expose the endpoint validator package namespace for reusable automation helpers.
# Notes: This module intentionally keeps a minimal surface, exporting the validator config
#        and execution entry points used by the CLI and tests.

"""Endpoint validation toolkit for VibeCO automation workflows."""

from .endpoint_validator import (  # noqa: F401
    BatchValidationReport,
    EndpointDefinition,
    EndpointResult,
    EndpointValidationReport,
    ValidatorConfig,
    build_batch_markdown_report,
    render_markdown_report,
    run_batch,
    run_validator,
)

__all__ = [
    "BatchValidationReport",
    "EndpointDefinition",
    "EndpointResult",
    "EndpointValidationReport",
    "ValidatorConfig",
    "build_batch_markdown_report",
    "render_markdown_report",
    "run_batch",
    "run_validator",
]
