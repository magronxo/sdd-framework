#!/usr/bin/env python3
"""Read-only status and next-route surface for Canonical SDD Model v1."""
from __future__ import annotations

import sys

# A read-only invocation must not create __pycache__ beside installed tools.
sys.dont_write_bytecode = True

import argparse
import json
from pathlib import Path
from typing import Any, Iterable

import sdd_validate as validator

CONTRACT_VERSION = "v1"


def _finding_dict(item: validator.Finding) -> dict[str, str]:
    return dict(item._asdict())


def _validation_fields(record: dict[str, Any], validation: dict[str, Any]) -> dict[str, Any]:
    return {
        "valid": validation["valid"],
        "state": record.get("state"),
        "effective_state": validation["effective"]["state"],
        "migration_review_required": validation["migration_review_required"],
        "warnings": [_finding_dict(item) for item in validation["warnings"]],
        "errors": [_finding_dict(item) for item in validation["errors"]],
    }


def status_result(
    record_path: Path,
    record: dict[str, Any],
    schema: dict[str, Any],
    protocol: dict[str, Any],
) -> dict[str, Any]:
    validation = validator.validate_record(record, schema, protocol, mode="read")
    return {
        "contract_version": CONTRACT_VERSION,
        "command": "status",
        "read_only": True,
        "record": str(record_path),
        **_validation_fields(record, validation),
    }


def _candidate_rules(protocol: dict[str, Any], effective_state: Any) -> list[tuple[str, dict[str, Any]]]:
    candidates: list[tuple[str, dict[str, Any]]] = []
    for kind, key in (("transition", "transitions"), ("regression", "regressions")):
        candidates.extend(
            (kind, rule)
            for rule in protocol.get(key, [])
            if rule.get("from") == effective_state
        )
    return candidates


def _route_result(
    kind: str,
    rule: dict[str, Any],
    record: dict[str, Any],
    protocol: dict[str, Any],
) -> dict[str, Any]:
    gate = validator.evaluate_transition(
        record,
        protocol,
        rule["from"],
        rule["to"],
    )
    return {
        "kind": kind,
        "from": rule["from"],
        "to": rule["to"],
        "result": gate.result,
        "reasons": [_finding_dict(item) for item in gate.reasons],
    }


def _next_summary(
    routes: list[dict[str, Any]],
    effective_state: Any,
    protocol: dict[str, Any],
) -> tuple[str, dict[str, Any] | None]:
    allowed = [route for route in routes if route["result"] == "ALLOW"]
    if len(allowed) == 1:
        route = allowed[0]
        return "READY", {
            key: route[key]
            for key in ("kind", "from", "to", "result")
        }
    if len(allowed) > 1:
        return "AMBIGUOUS", None
    if any(route["result"] == "HUMAN_REQUIRED" for route in routes):
        return "HUMAN_REQUIRED", None
    if routes:
        return "BLOCKED", None
    terminal_state = protocol["lifecycle"]["persistent_states"][-1]
    if effective_state == terminal_state:
        return "TERMINAL", None
    return "NO_DECLARED_ROUTE", None


def next_result(
    record_path: Path,
    record: dict[str, Any],
    schema: dict[str, Any],
    protocol: dict[str, Any],
) -> dict[str, Any]:
    validation = validator.validate_record(record, schema, protocol, mode="read")
    fields = _validation_fields(record, validation)
    result = {
        "contract_version": CONTRACT_VERSION,
        "command": "next",
        "read_only": True,
        "record": str(record_path),
        **fields,
        "next_status": None,
        "ready_route": None,
        "routes": [],
    }
    if not validation["valid"]:
        return result

    effective_state = validation["effective"]["state"]
    routes = [
        _route_result(kind, rule, record, protocol)
        for kind, rule in _candidate_rules(protocol, effective_state)
    ]
    next_status, ready_route = _next_summary(routes, effective_state, protocol)
    result.update(
        next_status=next_status,
        ready_route=ready_route,
        routes=routes,
    )
    return result


def _finding_lines(payload: dict[str, Any]) -> list[str]:
    lines: list[str] = []
    for label, key in (("WARNING", "warnings"), ("ERROR", "errors")):
        lines.extend(
            f"{label} {item['code']}: {item['message']}"
            for item in payload[key]
        )
    return lines


def _format_status(payload: dict[str, Any]) -> str:
    raw = payload["state"] if payload["state"] is not None else "UNKNOWN"
    effective = (
        payload["effective_state"]
        if payload["effective_state"] is not None
        else "UNKNOWN"
    )
    lines = [
        f"RECORD: {payload['record']}",
        f"STATE: {raw} (effective: {effective})",
        f"VALID: {'YES' if payload['valid'] else 'NO'}",
    ]
    lines.extend(_finding_lines(payload))
    return "\n".join(lines)


def _format_route(route: dict[str, Any]) -> str:
    return f"{route['from']} -> {route['to']}"


def _format_next(payload: dict[str, Any]) -> str:
    if not payload["valid"]:
        return "\n".join([f"INVALID: {payload['record']}", *_finding_lines(payload)])

    status = payload["next_status"]
    routes = payload["routes"]
    if status == "READY":
        route = payload["ready_route"]
        prefix = "REGRESSION READY" if route["kind"] == "regression" else "READY"
        lines = [f"{prefix}: {_format_route(route)}"]
    elif status == "TERMINAL":
        lines = [f"TERMINAL: {payload['effective_state']}"]
    elif status == "NO_DECLARED_ROUTE":
        lines = [f"NO DECLARED ROUTE: {payload['effective_state']}"]
    elif status == "BLOCKED" and len(routes) == 1:
        lines = [f"BLOCKED: {_format_route(routes[0])}"]
    else:
        lines = [f"{status}: {payload['effective_state']}"]

    if status in {"BLOCKED", "HUMAN_REQUIRED", "AMBIGUOUS"}:
        for route in routes:
            lines.append(f"- {route['kind']} {_format_route(route)}: {route['result']}")
            lines.extend(
                f"  {item['code']}: {item['message']}"
                for item in route["reasons"]
            )
    lines.extend(_finding_lines(payload))
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    for command in ("status", "next"):
        child = subparsers.add_parser(command)
        child.add_argument("record", type=Path)
        child.add_argument("--json", action="store_true", dest="as_json")
    return parser


def _read_record(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("feature record must be a JSON object")
    return value


def main(argv: Iterable[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        schema, protocol = validator.load_contracts()
    except (OSError, json.JSONDecodeError, validator.SchemaError, ValueError) as exc:
        print(f"CONTRACT_ERROR: {exc}", file=sys.stderr)
        return validator.EXIT_USAGE
    try:
        record = _read_record(args.record)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"INPUT_ERROR: {exc}", file=sys.stderr)
        return validator.EXIT_USAGE

    payload = (
        status_result(args.record, record, schema, protocol)
        if args.command == "status"
        else next_result(args.record, record, schema, protocol)
    )
    if args.as_json:
        print(json.dumps(payload, sort_keys=True, separators=(",", ":")))
    elif args.command == "status":
        print(_format_status(payload))
    else:
        print(_format_next(payload))
    return validator.EXIT_OK if payload["valid"] else validator.EXIT_INVALID


if __name__ == "__main__":
    raise SystemExit(main())
