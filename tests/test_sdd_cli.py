from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "tools/sdd.py"
VALIDATOR = ROOT / "tools/sdd_validate.py"
INSTALLER = ROOT / "tools/sdd_install.py"


def base_record(state: str) -> dict:
    return {
        "id": "feat-900-cli",
        "type": "SYSTEM_SPEC",
        "state": state,
        "title": "CLI route fixture",
        "created_at": "2026-08-01T00:00:00Z",
        "updated_at": "2026-08-01T00:10:00Z",
    }


def route_record(state: str, **updates) -> dict:
    record = base_record(state)
    record.update(updates)
    return record


class SddCliTests(unittest.TestCase):
    def run_cli(
        self,
        command: str,
        record: dict,
        *,
        as_json: bool = True,
        cli: Path = CLI,
        cwd: Path = ROOT,
        env: dict[str, str] | None = None,
    ) -> tuple[subprocess.CompletedProcess[str], Path, tempfile.TemporaryDirectory]:
        temp = tempfile.TemporaryDirectory()
        path = Path(temp.name) / "feature.json"
        path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
        argv = [sys.executable, str(cli), command, str(path)]
        if as_json:
            argv.append("--json")
        done = subprocess.run(
            argv,
            cwd=cwd,
            text=True,
            capture_output=True,
            check=False,
            env=env,
        )
        return done, path, temp

    def payload(self, command: str, record: dict) -> dict:
        done, _, temp = self.run_cli(command, record)
        try:
            self.assertEqual(done.returncode, 0, done.stderr)
            return json.loads(done.stdout)
        finally:
            temp.cleanup()

    def assert_ready(
        self,
        record: dict,
        source: str,
        target: str,
        kind: str = "transition",
    ) -> dict:
        payload = self.payload("next", record)
        self.assertEqual(payload["next_status"], "READY")
        self.assertEqual(
            payload["ready_route"],
            {"kind": kind, "from": source, "to": target, "result": "ALLOW"},
        )
        return payload

    def test_status_json_contract_for_valid_design(self) -> None:
        record = route_record(
            "DESIGN",
            design_path="docs/sdd/artifacts/design/feat-900-cli.md",
        )
        payload = self.payload("status", record)
        self.assertEqual(
            set(payload),
            {
                "contract_version",
                "command",
                "read_only",
                "record",
                "valid",
                "state",
                "effective_state",
                "migration_review_required",
                "warnings",
                "errors",
            },
        )
        self.assertEqual(payload["contract_version"], "v1")
        self.assertEqual(payload["command"], "status")
        self.assertTrue(payload["read_only"])
        self.assertTrue(payload["valid"])
        self.assertEqual(payload["state"], "DESIGN")
        self.assertEqual(payload["effective_state"], "DESIGN")
        self.assertEqual(payload["warnings"], [])
        self.assertEqual(payload["errors"], [])

    def test_valid_timestamp_status_and_next_remain_normal(self) -> None:
        record = route_record(
            "DESIGN",
            created_at="2026-08-26T00:00:00Z",
            updated_at="2026-08-26T02:10:00+02:00",
            design_path="docs/sdd/artifacts/design/feat-900-cli.md",
        )
        status = self.payload("status", record)
        self.assertTrue(status["valid"])
        next_route = self.payload("next", record)
        self.assertEqual(next_route["next_status"], "READY")
        self.assertEqual(next_route["ready_route"]["to"], "SPEC")

    def test_mixed_awareness_timestamp_clis_fail_structured_without_mutation(self) -> None:
        record = route_record(
            "DESIGN",
            created_at="2026-08-26",
            updated_at="2026-08-26T00:00:00Z",
            design_path="docs/sdd/artifacts/design/feat-900-cli.md",
        )
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "feature.json"
            path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
            before = path.read_bytes()
            digest = hashlib.sha256(before).hexdigest()
            mtime = path.stat().st_mtime_ns
            commands = {
                "validator": [
                    sys.executable,
                    str(VALIDATOR),
                    str(path),
                    "--format",
                    "json",
                ],
                "status": [sys.executable, str(CLI), "status", str(path), "--json"],
                "next": [sys.executable, str(CLI), "next", str(path), "--json"],
            }
            for command, argv in commands.items():
                with self.subTest(command=command):
                    done = subprocess.run(
                        argv,
                        cwd=ROOT,
                        text=True,
                        capture_output=True,
                        check=False,
                    )
                    self.assertEqual(done.returncode, 1, done.stderr)
                    self.assertNotIn("Traceback", done.stderr)
                    payload = json.loads(done.stdout)
                    self.assertFalse(payload["valid"])
                    self.assertIn(
                        "SCHEMA_INVALID",
                        {item["code"] for item in payload["errors"]},
                    )
                    if command == "next":
                        self.assertIsNone(payload["next_status"])
                        self.assertIsNone(payload["ready_route"])
                        self.assertEqual(payload["routes"], [])
                    self.assertEqual(path.read_bytes(), before)
                    self.assertEqual(
                        hashlib.sha256(path.read_bytes()).hexdigest(), digest
                    )
                    self.assertEqual(path.stat().st_mtime_ns, mtime)

    def test_status_tolerant_legacy_alias_exposes_warning(self) -> None:
        record = base_record("DESIGN")
        record["feature_id"] = record.pop("id")
        payload = self.payload("status", record)
        self.assertTrue(payload["valid"])
        self.assertEqual(
            {item["code"] for item in payload["warnings"]},
            {"LEGACY_FEATURE_ID"},
        )

    def test_status_invalid_record_is_structured_and_exits_invalid(self) -> None:
        record = base_record("DESIGN")
        del record["title"]
        done, _, temp = self.run_cli("status", record)
        try:
            self.assertEqual(done.returncode, 1, done.stderr)
            payload = json.loads(done.stdout)
            self.assertFalse(payload["valid"])
            self.assertIn("SCHEMA_INVALID", {item["code"] for item in payload["errors"]})
            self.assertTrue(payload["read_only"])
        finally:
            temp.cleanup()

    def test_status_text_is_bounded_and_useful(self) -> None:
        done, _, temp = self.run_cli("status", base_record("DESIGN"), as_json=False)
        try:
            self.assertEqual(done.returncode, 0, done.stderr)
            lines = done.stdout.splitlines()
            self.assertLessEqual(len(lines), 6)
            self.assertIn("RECORD:", lines[0])
            self.assertIn("STATE: DESIGN (effective: DESIGN)", lines)
            self.assertIn("VALID: YES", lines)
            self.assertNotIn("CLI route fixture", done.stdout)
        finally:
            temp.cleanup()

    def test_status_and_next_do_not_mutate_record(self) -> None:
        record = route_record(
            "IMPLEMENT",
            task_path="docs/sdd/artifacts/tasks/feat-900-cli.md",
        )
        for command in ("status", "next"):
            with self.subTest(command=command), tempfile.TemporaryDirectory() as temp:
                path = Path(temp) / "feature.json"
                path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
                before = path.read_bytes()
                digest = hashlib.sha256(before).hexdigest()
                mtime = path.stat().st_mtime_ns
                done = subprocess.run(
                    [sys.executable, str(CLI), command, str(path), "--json"],
                    cwd=ROOT,
                    text=True,
                    capture_output=True,
                    check=False,
                )
                self.assertEqual(done.returncode, 0, done.stderr)
                self.assertEqual(path.read_bytes(), before)
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), digest)
                self.assertEqual(path.stat().st_mtime_ns, mtime)

    def test_forward_routes_are_protocol_gated(self) -> None:
        cases = (
            (
                route_record(
                    "DESIGN",
                    design_path="docs/sdd/artifacts/design/feat-900-cli.md",
                ),
                "DESIGN",
                "SPEC",
            ),
            (
                route_record(
                    "SPEC",
                    spec_path="docs/sdd/artifacts/specs/feat-900-cli.md",
                ),
                "SPEC",
                "VALIDATION",
            ),
            (
                route_record(
                    "VALIDATION",
                    validation_result="PASS",
                    validated_at="2026-08-01T00:05:00Z",
                ),
                "VALIDATION",
                "TASKS",
            ),
            (
                route_record(
                    "TASKS",
                    validation_result="PASS",
                    validated_at="2026-08-01T00:05:00Z",
                    task_path="docs/sdd/artifacts/tasks/feat-900-cli.md",
                ),
                "TASKS",
                "IMPLEMENT",
            ),
            (
                route_record(
                    "IMPLEMENT",
                    task_path="docs/sdd/artifacts/tasks/feat-900-cli.md",
                ),
                "IMPLEMENT",
                "VERIFY",
            ),
            (
                route_record(
                    "VERIFY",
                    verification_result="PASS",
                    verified_at="2026-08-01T00:06:00Z",
                ),
                "VERIFY",
                "AUDIT",
            ),
        )
        for record, source, target in cases:
            with self.subTest(route=f"{source}->{target}"):
                self.assert_ready(record, source, target)

    def test_validation_fail_selects_only_allowed_regression(self) -> None:
        payload = self.assert_ready(
            route_record(
                "VALIDATION",
                validation_result="FAIL",
                validated_at="2026-08-01T00:05:00Z",
                validation_issues=["Ambiguous requirement."],
            ),
            "VALIDATION",
            "SPEC",
            "regression",
        )
        routes = {(route["kind"], route["to"]): route for route in payload["routes"]}
        self.assertEqual(routes[("transition", "TASKS")]["result"], "DENY")
        self.assertEqual(routes[("regression", "SPEC")]["result"], "ALLOW")

    def test_verify_fail_selects_only_allowed_regression(self) -> None:
        payload = self.assert_ready(
            route_record(
                "VERIFY",
                verification_result="FAIL",
                verified_at="2026-08-01T00:06:00Z",
            ),
            "VERIFY",
            "IMPLEMENT",
            "regression",
        )
        routes = {(route["kind"], route["to"]): route for route in payload["routes"]}
        self.assertEqual(routes[("transition", "AUDIT")]["result"], "DENY")
        self.assertEqual(routes[("regression", "IMPLEMENT")]["result"], "ALLOW")

    def test_verify_without_result_is_blocked_by_authoritative_gate(self) -> None:
        payload = self.payload("next", base_record("VERIFY"))
        self.assertEqual(payload["next_status"], "BLOCKED")
        self.assertIsNone(payload["ready_route"])
        self.assertFalse(any(route["result"] == "ALLOW" for route in payload["routes"]))
        codes = {
            item["code"]
            for route in payload["routes"]
            for item in route["reasons"]
        }
        self.assertIn("VERIFICATION_NOT_EXECUTED", codes)

    def test_audit_results_and_waiver_follow_archive_gate(self) -> None:
        for result in ("PASS", "WARN"):
            with self.subTest(result=result):
                self.assert_ready(
                    route_record(
                        "AUDIT",
                        audit_result=result,
                        audited_at="2026-08-01T00:07:00Z",
                    ),
                    "AUDIT",
                    "ARCHIVE",
                )
        self.assert_ready(
            route_record(
                "AUDIT",
                audit_result="FAIL",
                audited_at="2026-08-01T00:07:00Z",
                owner_waiver={
                    "waived_by": "owner",
                    "waived_at": "2026-08-01T00:08:00Z",
                    "reason": "Documented archival exception.",
                },
            ),
            "AUDIT",
            "ARCHIVE",
        )

    def test_audit_fail_is_blocked_without_automatic_repair(self) -> None:
        payload = self.payload(
            "next",
            route_record(
                "AUDIT",
                audit_result="FAIL",
                audited_at="2026-08-01T00:07:00Z",
            ),
        )
        self.assertEqual(payload["next_status"], "BLOCKED")
        self.assertIsNone(payload["ready_route"])
        self.assertEqual(len(payload["routes"]), 1)
        self.assertEqual(payload["routes"][0]["to"], "ARCHIVE")
        self.assertEqual(payload["routes"][0]["result"], "DENY")
        self.assertEqual(
            {item["code"] for item in payload["routes"][0]["reasons"]},
            {"AUDIT_FAILED"},
        )

    def test_archive_is_terminal(self) -> None:
        payload = self.payload(
            "next",
            route_record(
                "ARCHIVE",
                archived_at="2026-08-01T00:09:00Z",
            ),
        )
        self.assertEqual(payload["next_status"], "TERMINAL")
        self.assertEqual(payload["routes"], [])
        self.assertIsNone(payload["ready_route"])

    def test_blocking_question_code_is_exposed(self) -> None:
        payload = self.payload(
            "next",
            route_record(
                "VALIDATION",
                validation_result="PASS",
                validated_at="2026-08-01T00:05:00Z",
                open_questions=[
                    {
                        "id": "Q-900",
                        "text": "Blocking decision",
                        "blocking": True,
                        "owner": "owner",
                        "status": "OPEN",
                    }
                ],
            ),
        )
        self.assertEqual(payload["next_status"], "BLOCKED")
        codes = {
            item["code"]
            for route in payload["routes"]
            for item in route["reasons"]
        }
        self.assertIn("BLOCKING_OPEN_QUESTION", codes)

    def test_legacy_terminal_partial_is_warning_not_fake_route(self) -> None:
        for alias in ("DONE", "ARCHIVED"):
            with self.subTest(alias=alias):
                record = route_record(
                    alias,
                    archived_at="2026-08-01T00:09:00Z",
                    verification_result="PARTIAL",
                    verified_at="2026-08-01T00:06:00Z",
                )
                payload = self.payload("next", record)
                self.assertTrue(payload["migration_review_required"])
                self.assertEqual(payload["effective_state"], "ARCHIVE")
                self.assertEqual(payload["next_status"], "TERMINAL")
                self.assertEqual(payload["routes"], [])
                self.assertEqual(
                    {item["code"] for item in payload["warnings"]},
                    {"LEGACY_PARTIAL_AMBIGUOUS", "LEGACY_STATE_ALIAS"},
                )

    def test_active_partial_is_invalid_and_has_no_routes(self) -> None:
        done, _, temp = self.run_cli(
            "next",
            route_record(
                "VERIFY",
                verification_result="PARTIAL",
                verified_at="2026-08-01T00:06:00Z",
            ),
        )
        try:
            self.assertEqual(done.returncode, 1, done.stderr)
            payload = json.loads(done.stdout)
            self.assertFalse(payload["valid"])
            self.assertIsNone(payload["next_status"])
            self.assertEqual(payload["routes"], [])
            self.assertIn(
                "VERIFICATION_NOT_EXECUTED",
                {item["code"] for item in payload["errors"]},
            )
        finally:
            temp.cleanup()

    def test_undeclared_implement_to_spec_hint_is_not_exposed(self) -> None:
        payload = self.payload(
            "next",
            route_record(
                "IMPLEMENT",
                task_path="docs/sdd/artifacts/tasks/feat-900-cli.md",
                implementation_notes='CLI-local hint: {"to": "SPEC"}',
            ),
        )
        self.assertEqual(
            {(route["from"], route["to"]) for route in payload["routes"]},
            {("IMPLEMENT", "VERIFY")},
        )

    def test_next_text_is_compact_and_surfaces_blocker_code(self) -> None:
        done, _, temp = self.run_cli("next", base_record("VERIFY"), as_json=False)
        try:
            self.assertEqual(done.returncode, 0, done.stderr)
            self.assertIn("BLOCKED: VERIFY", done.stdout)
            self.assertIn("VERIFICATION_NOT_EXECUTED", done.stdout)
            self.assertLessEqual(len(done.stdout.splitlines()), 8)
        finally:
            temp.cleanup()

    def test_installed_copy_loads_sibling_contracts_and_validator(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "product"
            target.mkdir()
            install = subprocess.run(
                [sys.executable, str(INSTALLER), "--target", str(target)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(install.returncode, 0, install.stderr)
            cli = target / "docs/sdd/tools/sdd.py"
            record = route_record(
                "DESIGN",
                design_path="docs/sdd/artifacts/design/feat-900-cli.md",
            )
            env = dict(os.environ)
            env.pop("PYTHONDONTWRITEBYTECODE", None)
            done, _, record_temp = self.run_cli(
                "next", record, cli=cli, cwd=target, env=env
            )
            try:
                self.assertEqual(done.returncode, 0, done.stderr)
                payload = json.loads(done.stdout)
                self.assertEqual(payload["next_status"], "READY")
                self.assertEqual(payload["ready_route"]["to"], "SPEC")
                self.assertFalse(any(target.rglob("__pycache__")))
            finally:
                record_temp.cleanup()

    def test_source_has_no_effectful_runtime_facilities(self) -> None:
        source = CLI.read_text(encoding="utf-8")
        for token in (
            "subprocess",
            "socket",
            "requests",
            "urllib",
            "write_text(",
            "write_bytes(",
            "touch(",
            "os.environ",
            "git ",
        ):
            with self.subTest(token=token):
                self.assertNotIn(token, source)
        self.assertIn("validator.validate_record", source)
        self.assertIn("validator.evaluate_transition", source)
        self.assertIn('(\"transition\", \"transitions\")', source)
        self.assertIn('(\"regression\", \"regressions\")', source)


if __name__ == "__main__":
    unittest.main()
