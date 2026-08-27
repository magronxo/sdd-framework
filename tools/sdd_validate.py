#!/usr/bin/env python3
"""Read-only validator and gate evaluator for Canonical SDD Model v1."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable, NamedTuple

from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import SchemaError

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCHEMA = ROOT / "contract/v1/feature-record.schema.json"
DEFAULT_PROTOCOL = ROOT / "contract/v1/sdd-protocol.json"
EXIT_OK, EXIT_INVALID, EXIT_USAGE, EXIT_HUMAN_REQUIRED = 0, 1, 2, 3
DATETIME_CHECKER_ERROR = (
    "Required date-time format checker unavailable or broken; install dependencies from "
    "contract/v1/requirements-validator.txt (or the installed "
    "docs/sdd/contract/v1/requirements-validator.txt)."
)
DATETIME_PROBE_SCHEMA = {"type": "string", "format": "date-time"}
DATETIME_VALID_PROBE = "2026-08-26T00:00:00Z"
DATETIME_INVALID_PROBE = "NOT-A-RFC3339-TIMESTAMP"


class Finding(NamedTuple):
    code: str
    message: str
    path: str = "$"
    severity: str = "ERROR"


class GateResult(NamedTuple):
    result: str
    from_state: str
    to_state: str
    reasons: tuple[Finding, ...]


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _json_path(parts: Iterable[Any]) -> str:
    out = "$"
    for part in parts:
        out += f"[{part}]" if isinstance(part, int) else f".{part}"
    return out


def _parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value[:-1] + "+00:00" if value.endswith("Z") else value)


def _format_checker() -> FormatChecker:
    checker = FormatChecker()
    try:
        probe_validator = Draft202012Validator(
            DATETIME_PROBE_SCHEMA,
            format_checker=checker,
        )
        valid_errors = list(probe_validator.iter_errors(DATETIME_VALID_PROBE))
        invalid_errors = list(probe_validator.iter_errors(DATETIME_INVALID_PROBE))
    except Exception as exc:
        raise ValueError(DATETIME_CHECKER_ERROR) from exc
    if valid_errors or not invalid_errors:
        raise ValueError(DATETIME_CHECKER_ERROR)
    return checker


def _effective_state(value: Any, protocol: dict[str, Any]) -> Any:
    return protocol["lifecycle"]["legacy_state_aliases"].get(value, value)


def _effective_validation(value: Any) -> Any:
    return "PASS" if value == "PASS_WITH_FOLLOWUP" else value


def _effective_verification(value: Any) -> Any:
    return None if value == "PARTIAL" else value


def _blocking_questions(record: dict[str, Any]) -> list[dict[str, Any]]:
    questions = record.get("open_questions", [])
    if not isinstance(questions, list):
        return []
    return [q for q in questions if isinstance(q, dict) and q.get("status") == "OPEN" and q.get("blocking") is True]


def _valid_waiver(record: dict[str, Any]) -> bool:
    waiver = record.get("owner_waiver")
    if not isinstance(waiver, dict):
        return False
    if not all(isinstance(waiver.get(k), str) and waiver[k].strip() for k in ("waived_by", "waived_at", "reason")):
        return False
    try:
        _parse_time(waiver["waived_at"])
    except (TypeError, ValueError):
        return False
    return True


def _find_rule(protocol: dict[str, Any], from_state: str, to_state: str) -> dict[str, Any] | None:
    rules = protocol.get("transitions", []) + protocol.get("regressions", [])
    return next((r for r in rules if r.get("from") == from_state and r.get("to") == to_state), None)


def _validate_protocol(protocol: dict[str, Any]) -> None:
    states = ["DESIGN", "SPEC", "VALIDATION", "TASKS", "IMPLEMENT", "VERIFY", "AUDIT", "ARCHIVE"]
    if protocol.get("protocol_version") != "1.0.0":
        raise ValueError("unsupported protocol_version")
    if protocol.get("lifecycle", {}).get("persistent_states") != states:
        raise ValueError("protocol lifecycle does not match Canonical SDD Model v1")
    if protocol.get("gate_results") != ["ALLOW", "DENY", "HUMAN_REQUIRED"]:
        raise ValueError("protocol gate_results are invalid")
    if protocol.get("lifecycle", {}).get("legacy_state_aliases") != {"DONE": "ARCHIVE", "ARCHIVED": "ARCHIVE"}:
        raise ValueError("protocol legacy state aliases are invalid")
    declared = {(r.get("from"), r.get("to")) for r in protocol.get("transitions", [])}
    required = {(states[i], states[i + 1]) for i in range(len(states) - 1)}
    if declared != required:
        raise ValueError("protocol canonical transitions are incomplete or duplicated")

    interpretations = protocol.get("gate_interpretations", {})
    validation_legacy = interpretations.get("validation_legacy_reads", {})
    verification_legacy = interpretations.get("verification_legacy_reads", {})
    if validation_legacy.get("PASS_WITH_FOLLOWUP", {}).get("effective_result") != "PASS":
        raise ValueError("PASS_WITH_FOLLOWUP must be a validation legacy read")
    if "PASS_WITH_FOLLOWUP" in verification_legacy:
        raise ValueError("PASS_WITH_FOLLOWUP must not be a verification legacy read")
    partial = verification_legacy.get("PARTIAL", {})
    archived = partial.get("historical_archive", {})
    if partial.get("active_feature", {}).get("blocker") != "VERIFICATION_NOT_EXECUTED":
        raise ValueError("active PARTIAL semantics are invalid")
    if archived.get("warning") != "LEGACY_PARTIAL_AMBIGUOUS" or archived.get("migration_review_required") is not True or archived.get("mutation_allowed") is not False:
        raise ValueError("historical PARTIAL semantics are invalid")

    policy = protocol.get("human_approval_policy", {})
    if policy.get("core_default") != "not_required" or policy.get("resolution_mode") != "external_input_only":
        raise ValueError("human approval must be conditional external policy input")
    if policy.get("integration_implemented") is not False:
        raise ValueError("Phase 1 must not implement external governance integration")
    checkpoints = protocol.get("human_checkpoints", {})
    checkpoint = checkpoints.get("TASKS_TO_IMPLEMENT", {})
    if checkpoint.get("default_required") is not False or checkpoint.get("transition") != {"from": "TASKS", "to": "IMPLEMENT"}:
        raise ValueError("TASKS_TO_IMPLEMENT checkpoint is invalid")
    task_rule = _find_rule(protocol, "TASKS", "IMPLEMENT")
    if task_rule is None or task_rule.get("policy_hooks") != ["TASKS_TO_IMPLEMENT"]:
        raise ValueError("TASKS -> IMPLEMENT conditional policy hook is missing")
    if any(req.get("type") == "human_approval" for req in task_rule.get("requirements", [])):
        raise ValueError("TASKS -> IMPLEMENT must not require universal human approval")
    validation_rule = _find_rule(protocol, "VALIDATION", "TASKS")
    if not validation_rule or not any(req.get("type") == "effective_validation_equals" for req in validation_rule.get("requirements", [])):
        raise ValueError("VALIDATION -> TASKS must use effective validation")


def load_contracts(schema_path: Path = DEFAULT_SCHEMA, protocol_path: Path = DEFAULT_PROTOCOL) -> tuple[dict[str, Any], dict[str, Any]]:
    schema, protocol = _read_json(schema_path), _read_json(protocol_path)
    Draft202012Validator.check_schema(schema)
    _validate_protocol(protocol)
    _format_checker()
    return schema, protocol


def validate_record(record: dict[str, Any], schema: dict[str, Any], protocol: dict[str, Any], mode: str = "read") -> dict[str, Any]:
    if mode not in {"read", "write"}:
        raise ValueError("mode must be read or write")
    errors: list[Finding] = []
    warnings: list[Finding] = []

    def error(code: str, message: str, path: str = "$") -> None:
        errors.append(Finding(code, message, path))

    def warning(code: str, message: str, path: str) -> None:
        warnings.append(Finding(code, message, path, "WARNING"))

    validator = Draft202012Validator(schema, format_checker=_format_checker())
    for item in sorted(validator.iter_errors(record), key=lambda e: _json_path(e.absolute_path)):
        error("SCHEMA_INVALID", item.message, _json_path(item.absolute_path))

    if "feature_id" in record:
        warning("LEGACY_FEATURE_ID", "feature_id is a legacy read alias; canonical writes use id.", "$.feature_id")
    if "id" in record and "feature_id" in record and record["id"] != record["feature_id"]:
        error("ALIAS_DIVERGENCE", "id and feature_id contain different values.", "$.feature_id")
    if "tasks_path" in record:
        warning("LEGACY_TASKS_PATH", "tasks_path is a legacy read alias; canonical writes use task_path.", "$.tasks_path")
    if "task_path" in record and "tasks_path" in record and record["task_path"] != record["tasks_path"]:
        error("ALIAS_DIVERGENCE", "task_path and tasks_path contain different values.", "$.tasks_path")

    state = record.get("state")
    effective_state = _effective_state(state, protocol)
    if state in protocol["lifecycle"]["legacy_state_aliases"]:
        warning("LEGACY_STATE_ALIAS", f"{state} is a legacy read alias for ARCHIVE.", "$.state")
    for field, value in record.items():
        if (field.endswith("_path") or field == "tasks_path") and isinstance(value, str) and value.startswith("artifacts/"):
            warning("LEGACY_ARTIFACT_PATH", "Legacy artifacts/... path is relative to sdd_root and was not normalized.", f"$.{field}")

    validation = record.get("validation_result")
    if validation == "PASS_WITH_FOLLOWUP":
        warning("LEGACY_PASS_WITH_FOLLOWUP", "validation_result PASS_WITH_FOLLOWUP was interpreted as effective PASS.", "$.validation_result")

    verification = record.get("verification_result")
    migration_review_required = False
    if verification == "PARTIAL":
        if effective_state == "ARCHIVE":
            migration_review_required = True
            warning("LEGACY_PARTIAL_AMBIGUOUS", "Archived verification_result PARTIAL is ambiguous; migration review is required without modifying the record.", "$.verification_result")
        else:
            error("VERIFICATION_NOT_EXECUTED", "Active features cannot use PARTIAL as verification evidence.", "$.verification_result")

    created, updated = record.get("created_at"), record.get("updated_at")
    if isinstance(created, str) and isinstance(updated, str):
        try:
            if _parse_time(updated) < _parse_time(created):
                error("TIMESTAMP_ORDER_INVALID", "updated_at is earlier than created_at.", "$.updated_at")
        except (TypeError, ValueError):
            pass
    if effective_state == "ARCHIVE" and "archived_at" not in record:
        error("ARCHIVE_TIMESTAMP_MISSING", "Archived records require archived_at.", "$.archived_at")

    if mode == "write":
        errors.extend(Finding("NON_CANONICAL_WRITE", f"Canonical write rejected legacy construct {w.code}.", w.path) for w in warnings)
        if verification == "PARTIAL" and not any(e.code == "NON_CANONICAL_WRITE" and e.path == "$.verification_result" for e in errors):
            error("NON_CANONICAL_WRITE", "Canonical writes reject verification_result PARTIAL.", "$.verification_result")

    return {
        "valid": not errors,
        "mode": mode,
        "errors": errors,
        "warnings": warnings,
        "migration_review_required": migration_review_required,
        "effective": {
            "id": record.get("id", record.get("feature_id")),
            "state": effective_state,
            "task_path": record.get("task_path", record.get("tasks_path")),
            "validation_result": _effective_validation(validation),
            "verification_result": _effective_verification(verification),
        },
    }


def _reason(code: str, message: str, path: str = "$") -> Finding:
    return Finding(code, message, path)


def evaluate_transition(record: dict[str, Any], protocol: dict[str, Any], from_state: str, to_state: str, approvals: Iterable[str] = (), required_approvals: Iterable[str] = ()) -> GateResult:
    if _effective_state(record.get("state"), protocol) != from_state:
        return GateResult("DENY", from_state, to_state, (_reason("SOURCE_STATE_MISMATCH", "Record state does not match the requested transition source.", "$.state"),))
    rule = _find_rule(protocol, from_state, to_state)
    if rule is None:
        return GateResult("DENY", from_state, to_state, (_reason("INVALID_TRANSITION", f"Transition {from_state} -> {to_state} is not declared."),))

    deny: list[Finding] = []
    human: list[Finding] = []
    for req in rule.get("requirements", []):
        kind, blocker = req.get("type"), req.get("blocker", "SCHEMA_INVALID")
        if kind == "field_present":
            field = req["field"]
            if not isinstance(record.get(field), str) or not record[field].strip():
                deny.append(_reason(blocker, f"Required field {field} is missing.", f"$.{field}"))
        elif kind == "field_present_alias_aware":
            field, alias = req["field"], req["legacy_alias"]
            value = record.get(field, record.get(alias))
            if not isinstance(value, str) or not value.strip():
                deny.append(_reason(blocker, f"Required field {field} is missing.", f"$.{field}"))
        elif kind == "field_equals":
            field, expected = req["field"], req["value"]
            if record.get(field) != expected:
                deny.append(_reason(blocker, f"{field} must equal {expected}.", f"$.{field}"))
        elif kind == "effective_validation_equals":
            expected = req["value"]
            if _effective_validation(record.get("validation_result")) != expected:
                deny.append(_reason(blocker, f"validation_result must provide effective {expected} evidence.", "$.validation_result"))
        elif kind == "effective_verification_equals":
            expected = req["value"]
            if _effective_verification(record.get("verification_result")) != expected:
                deny.append(_reason(blocker, f"verification_result must provide effective {expected} evidence.", "$.verification_result"))
        elif kind == "no_blocking_open_questions":
            blocked = _blocking_questions(record)
            if blocked:
                ids = ", ".join(str(q.get("id", "?")) for q in blocked)
                deny.append(_reason(blocker, f"Blocking open questions remain: {ids}.", "$.open_questions"))
        elif kind == "audit_allows_archive":
            result = record.get("audit_result")
            if result not in {"PASS", "WARN"} and not (result == "FAIL" and _valid_waiver(record)):
                code = "OWNER_WAIVER_INVALID" if result == "FAIL" and "owner_waiver" in record else blocker
                path = "$.owner_waiver" if code == "OWNER_WAIVER_INVALID" else "$.audit_result"
                deny.append(_reason(code, "AUDIT FAIL blocks ARCHIVE without a valid owner waiver.", path))
        else:
            deny.append(_reason("SCHEMA_INVALID", f"Unknown protocol requirement type: {kind}."))

    checkpoints = protocol.get("human_checkpoints", {})
    hooks = set(rule.get("policy_hooks", []))
    approvals_set = set(approvals)
    for checkpoint in sorted(set(required_approvals)):
        if checkpoint not in checkpoints or checkpoint not in hooks:
            deny.append(_reason("POLICY_REQUIREMENT_INVALID", f"Policy checkpoint {checkpoint} does not apply to {from_state} -> {to_state}.", "$.policy"))
        elif checkpoint not in approvals_set:
            human.append(Finding("HUMAN_APPROVAL_REQUIRED", f"Active policy requires human approval {checkpoint}.", "$.approvals", "HUMAN_REQUIRED"))

    if deny:
        return GateResult("DENY", from_state, to_state, tuple(deny))
    if human:
        return GateResult("HUMAN_REQUIRED", from_state, to_state, tuple(human))
    return GateResult("ALLOW", from_state, to_state, ())


def _finding_dict(item: Finding) -> dict[str, str]:
    return item._asdict()


def _payload(record: Path | None, validation: dict[str, Any] | None, gate: GateResult | None) -> dict[str, Any]:
    out: dict[str, Any] = {"contract_version": "v1", "contracts_ok": True, "read_only": True}
    if record is not None:
        out["record"] = str(record)
    if validation is not None:
        out.update({
            "valid": validation["valid"],
            "mode": validation["mode"],
            "effective": validation["effective"],
            "migration_review_required": validation["migration_review_required"],
            "errors": [_finding_dict(x) for x in validation["errors"]],
            "warnings": [_finding_dict(x) for x in validation["warnings"]],
        })
    if gate is not None:
        out["gate"] = {"result": gate.result, "from": gate.from_state, "to": gate.to_state, "reasons": [_finding_dict(x) for x in gate.reasons]}
    return out


def _print_text(payload: dict[str, Any]) -> None:
    if "valid" not in payload:
        print("CONTRACTS: PASS\nREAD_ONLY: true")
        return
    status = "FAIL" if not payload["valid"] else "PASS_WITH_WARNINGS" if payload["warnings"] else "PASS"
    print(f"VALIDATION: {status}\nMODE: {payload['mode']}\nREAD_ONLY: true\nMIGRATION_REVIEW_REQUIRED: {str(payload['migration_review_required']).lower()}")
    for kind in ("warnings", "errors"):
        for item in payload[kind]:
            print(f"{item['severity']} [{item['code']}] {item['path']}: {item['message']}")
    if "gate" in payload:
        gate = payload["gate"]
        print(f"GATE: {gate['result']} ({gate['from']} -> {gate['to']})")
        for item in gate["reasons"]:
            print(f"REASON [{item['code']}] {item['path']}: {item['message']}")


def _parse_transition(value: str) -> tuple[str, str]:
    parts = value.split(":", 1)
    if len(parts) != 2 or not all(parts):
        raise argparse.ArgumentTypeError("transition must use FROM:TO")
    return parts[0], parts[1]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("record", nargs="?", type=Path)
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    parser.add_argument("--protocol", type=Path, default=DEFAULT_PROTOCOL)
    parser.add_argument("--mode", choices=("read", "write"), default="read")
    parser.add_argument("--transition", type=_parse_transition, metavar="FROM:TO")
    parser.add_argument("--require-approval", action="append", default=[], metavar="CHECKPOINT")
    parser.add_argument("--approval", action="append", default=[], metavar="CHECKPOINT")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--self-check", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if not args.self_check and args.record is None:
        print("INPUT_ERROR: record is required unless --self-check is used", file=sys.stderr)
        return EXIT_USAGE
    try:
        schema, protocol = load_contracts(args.schema, args.protocol)
    except (OSError, json.JSONDecodeError, SchemaError, ValueError) as exc:
        print(f"CONTRACT_ERROR: {exc}", file=sys.stderr)
        return EXIT_USAGE
    if args.self_check and args.record is None:
        payload = _payload(None, None, None)
        print(json.dumps(payload, indent=2, sort_keys=True) if args.format == "json" else "CONTRACTS: PASS\nREAD_ONLY: true")
        return EXIT_OK
    try:
        record = _read_json(args.record)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"INPUT_ERROR: {exc}", file=sys.stderr)
        return EXIT_USAGE
    if not isinstance(record, dict):
        print("INPUT_ERROR: feature record must be a JSON object", file=sys.stderr)
        return EXIT_USAGE

    validation = validate_record(record, schema, protocol, args.mode)
    gate = evaluate_transition(record, protocol, *args.transition, approvals=args.approval, required_approvals=args.require_approval) if args.transition else None
    payload = _payload(args.record, validation, gate)
    print(json.dumps(payload, indent=2, sort_keys=True) if args.format == "json" else "", end="" if args.format == "json" else "")
    if args.format == "text":
        _print_text(payload)
    elif args.format == "json":
        print()
    if not validation["valid"] or (gate and gate.result == "DENY"):
        return EXIT_INVALID
    return EXIT_HUMAN_REQUIRED if gate and gate.result == "HUMAN_REQUIRED" else EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())
