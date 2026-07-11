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


def _effective_state(value: Any, protocol: dict[str, Any]) -> Any:
    return protocol["lifecycle"]["legacy_state_aliases"].get(value, value)


def _effective_verification(value: Any) -> Any:
    return "PASS" if value == "PASS_WITH_FOLLOWUP" else None if value == "PARTIAL" else value


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
    if not isinstance(protocol.get("blockers"), dict) or not protocol["blockers"]:
        raise ValueError("protocol blockers are missing")
    declared = {(r.get("from"), r.get("to")) for r in protocol.get("transitions", [])}
    required = {(states[i], states[i + 1]) for i in range(len(states) - 1)}
    if declared != required:
        raise ValueError("protocol canonical transitions are incomplete or duplicated")

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
    for rule in protocol.get("transitions", []):
        if any(hook not in checkpoints for hook in rule.get("policy_hooks", [])):
            raise ValueError("transition references an undeclared policy hook")


def load_contracts(schema_path: Path = DEFAULT_SCHEMA, protocol_path: Path = DEFAULT_PROTOCOL) -> tuple[dict[str, Any], dict[str, Any]]:
    schema, protocol = _read_json(schema_path), _read_json(protocol_path)
    Draft202012Validator.check_schema(schema)
    _validate_protocol(protocol)
    return schema, protocol


def validate_record(record: dict[str, Any], schema: dict[str, Any], protocol: dict[str, Any], mode: str = "read") -> dict[str, Any]:
    if mode not in {"read", "write"}:
        raise ValueError("mode must be read or write")
    errors: list[Finding] = []
    warnings: list[Finding] = []
    add_error = lambda code, msg, path="$": errors.append(Finding(code, msg, path))
    add_warning = lambda code, msg, path: warnings.append(Finding(code, msg, path, "WARNING"))

    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    for err in sorted(validator.iter_errors(record), key=lambda item: list(item.absolute_path)):
        add_error("SCHEMA_INVALID", err.message, _json_path(err.absolute_path))

    if "feature_id" in record:
        add_warning("LEGACY_FEATURE_ID", "feature_id is a legacy read alias; canonical writes use id.", "$.feature_id")
    if "id" in record and "feature_id" in record and record["id"] != record["feature_id"]:
        add_error("ALIAS_DIVERGENCE", "id and feature_id contain different values.", "$.feature_id")
    if "tasks_path" in record:
        add_warning("LEGACY_TASKS_PATH", "tasks_path is a legacy read alias; canonical writes use task_path.", "$.tasks_path")
    if "task_path" in record and "tasks_path" in record and record["task_path"] != record["tasks_path"]:
        add_error("ALIAS_DIVERGENCE", "task_path and tasks_path contain different values.", "$.tasks_path")

    state = record.get("state")
    if state in protocol["lifecycle"]["legacy_state_aliases"]:
        add_warning("LEGACY_STATE_ALIAS", f"{state} is a legacy read alias for ARCHIVE.", "$.state")
    for field, value in record.items():
        if (field.endswith("_path") or field == "tasks_path") and isinstance(value, str) and value.startswith("artifacts/"):
            add_warning("LEGACY_ARTIFACT_PATH", "Legacy artifacts/... path is relative to sdd_root and was not normalized.", f"$.{field}")

    verification = record.get("verification_result")
    if verification == "PARTIAL":
        add_error("VERIFICATION_NOT_EXECUTED", "PARTIAL is not canonical verification evidence.", "$.verification_result")
    elif verification == "PASS_WITH_FOLLOWUP":
        add_warning("LEGACY_PASS_WITH_FOLLOWUP", "PASS_WITH_FOLLOWUP was interpreted as PASS with non-blocking follow-up questions.", "$.verification_result")
        if _blocking_questions(record):
            add_error("BLOCKING_OPEN_QUESTION", "PASS_WITH_FOLLOWUP cannot coexist with a blocking open question.", "$.open_questions")

    created, updated = record.get("created_at"), record.get("updated_at")
    if isinstance(created, str) and isinstance(updated, str):
        try:
            if _parse_time(updated) < _parse_time(created):
                add_error("TIMESTAMP_ORDER_INVALID", "updated_at is earlier than created_at.", "$.updated_at")
        except ValueError:
            pass
    if _effective_state(state, protocol) == "ARCHIVE" and "archived_at" not in record:
        add_error("ARCHIVE_TIMESTAMP_MISSING", "Archived records require archived_at.", "$.archived_at")
    if mode == "write":
        errors.extend(Finding("NON_CANONICAL_WRITE", f"Canonical write rejected legacy construct {w.code}.", w.path) for w in warnings)

    return {
        "valid": not errors,
        "mode": mode,
        "errors": errors,
        "warnings": warnings,
        "effective": {
            "id": record.get("id", record.get("feature_id")),
            "state": _effective_state(state, protocol),
            "task_path": record.get("task_path", record.get("tasks_path")),
            "verification_result": _effective_verification(verification),
        },
    }


def _reason(code: str, message: str, path: str = "$") -> Finding:
    return Finding(code, message, path)


def evaluate_transition(
    record: dict[str, Any],
    protocol: dict[str, Any],
    from_state: str,
    to_state: str,
    approvals: Iterable[str] = (),
    required_approvals: Iterable[str] = (),
) -> GateResult:
    if _effective_state(record.get("state"), protocol) != from_state:
        return GateResult("DENY", from_state, to_state, (_reason("SOURCE_STATE_MISMATCH", "Record state does not match the requested transition source.", "$.state"),))
    rule = _find_rule(protocol, from_state, to_state)
    if rule is None:
        return GateResult("DENY", from_state, to_state, (_reason("INVALID_TRANSITION", f"Transition {from_state} -> {to_state} is not declared."),))

    deny: list[Finding] = []
    human: list[Finding] = []
    approvals, required_approvals = set(approvals), set(required_approvals)
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
        elif kind == "effective_verification_equals":
            if _effective_verification(record.get("verification_result")) != req["value"]:
                deny.append(_reason(blocker, f"verification_result must provide effective {req['value']} evidence.", "$.verification_result"))
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
    for checkpoint in sorted(required_approvals):
        if checkpoint not in checkpoints or checkpoint not in hooks:
            deny.append(_reason("POLICY_REQUIREMENT_INVALID", f"Policy checkpoint {checkpoint} does not apply to {from_state} -> {to_state}.", "$.policy"))
        elif checkpoint not in approvals:
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
            "valid": validation["valid"], "mode": validation["mode"], "effective": validation["effective"],
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
    print(f"VALIDATION: {status}\nMODE: {payload['mode']}\nREAD_ONLY: true")
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
    gate = evaluate_transition(
        record, protocol, *args.transition,
        approvals=args.approval, required_approvals=args.require_approval,
    ) if args.transition else None
    payload = _payload(args.record, validation, gate)
    if args.format == "json":
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        _print_text(payload)
    if not validation["valid"] or (gate and gate.result == "DENY"):
        return EXIT_INVALID
    return EXIT_HUMAN_REQUIRED if gate and gate.result == "HUMAN_REQUIRED" else EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())
