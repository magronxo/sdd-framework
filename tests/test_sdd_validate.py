from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "tools/sdd_validate.py"
SCHEMA = ROOT / "contract/v1/feature-record.schema.json"
PROTOCOL = ROOT / "contract/v1/sdd-protocol.json"
FIXTURES = ROOT / "tests/fixtures/v1/feature-record-cases.json"

spec = importlib.util.spec_from_file_location("sdd_validate", VALIDATOR)
assert spec and spec.loader
sdd = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = sdd
spec.loader.exec_module(sdd)


class CanonicalSddV1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema, cls.protocol = sdd.load_contracts(SCHEMA, PROTOCOL)
        data = json.loads(FIXTURES.read_text(encoding="utf-8"))
        cls.cases = {}
        for source in data["cases"]:
            item = dict(source)
            record = dict(data["base_record"])
            record.update(source.get("record_patch", {}))
            for field in source.get("remove_fields", []):
                record.pop(field, None)
            item["record"] = record
            cls.cases[item["name"]] = item

    def validation(self, name: str, mode: str | None = None):
        case = self.cases[name]
        return sdd.validate_record(
            case["record"], self.schema, self.protocol, mode or case["mode"]
        )

    def gate(self, name: str):
        case = self.cases[name]
        transition = case["transition"]
        return sdd.evaluate_transition(
            case["record"],
            self.protocol,
            transition["from"],
            transition["to"],
            approvals=transition.get("approvals", []),
            required_approvals=transition.get("required_approvals", []),
        )

    def test_contract_baseline_and_authority(self) -> None:
        self.assertEqual(
            self.protocol["lifecycle"]["persistent_states"],
            ["DESIGN", "SPEC", "VALIDATION", "TASKS", "IMPLEMENT", "VERIFY", "AUDIT", "ARCHIVE"],
        )
        self.assertEqual(self.protocol["gate_results"], ["ALLOW", "DENY", "HUMAN_REQUIRED"])
        self.assertNotIn("properties", self.protocol)
        serialized = json.dumps(self.schema)
        self.assertNotIn('"transitions"', serialized)
        self.assertNotIn('"gate_results"', serialized)

    def test_protocol_places_pass_with_followup_only_in_validation(self) -> None:
        interpretations = self.protocol["gate_interpretations"]
        self.assertEqual(
            interpretations["validation_legacy_reads"]["PASS_WITH_FOLLOWUP"]["effective_result"],
            "PASS",
        )
        self.assertNotIn("PASS_WITH_FOLLOWUP", interpretations["verification_legacy_reads"])
        validation_rule = next(
            r for r in self.protocol["transitions"]
            if (r["from"], r["to"]) == ("VALIDATION", "TASKS")
        )
        self.assertIn(
            "effective_validation_equals",
            {req["type"] for req in validation_rule["requirements"]},
        )

    def test_protocol_declares_partial_active_and_historical(self) -> None:
        partial = self.protocol["gate_interpretations"]["verification_legacy_reads"]["PARTIAL"]
        self.assertEqual(partial["active_feature"]["blocker"], "VERIFICATION_NOT_EXECUTED")
        self.assertFalse(partial["active_feature"]["record_valid"])
        archived = partial["historical_archive"]
        self.assertEqual(archived["warning"], "LEGACY_PARTIAL_AMBIGUOUS")
        self.assertTrue(archived["migration_review_required"])
        self.assertFalse(archived["mutation_allowed"])
        self.assertEqual(archived["source_states"], ["ARCHIVE", "DONE", "ARCHIVED"])

    def test_schema_result_placement_and_singular_artifacts(self) -> None:
        validation = json.dumps(self.schema["properties"]["validation_result"])
        verification = json.dumps(self.schema["properties"]["verification_result"])
        self.assertIn("PASS_WITH_FOLLOWUP", validation)
        self.assertNotIn("PASS_WITH_FOLLOWUP", verification)
        self.assertIn("PARTIAL", verification)
        properties = self.schema["properties"]
        for field in ("design_path", "spec_path", "task_path"):
            self.assertIn(field, properties)
        for field in ("design_artifacts", "spec_artifacts", "task_artifacts"):
            self.assertNotIn(field, properties)

    def test_all_30_fixture_cases(self) -> None:
        self.assertEqual(len(self.cases), 30)
        for name, case in self.cases.items():
            with self.subTest(case=name):
                result = self.validation(name)
                expected = case["expect"]
                self.assertEqual(result["valid"], expected["valid"])
                self.assertEqual(
                    sorted(x.code for x in result["warnings"]),
                    sorted(expected["warning_codes"]),
                )
                self.assertEqual(
                    sorted({x.code for x in result["errors"]}),
                    sorted(expected["error_codes"]),
                )
                self.assertEqual(
                    result["migration_review_required"],
                    expected["migration_review_required"],
                )
                if "transition" in case:
                    gate = self.gate(name)
                    self.assertEqual(gate.result, case["transition"]["result"])
                    self.assertEqual(
                        sorted(x.code for x in gate.reasons),
                        sorted(case["transition"]["reason_codes"]),
                    )

    def test_pass_with_followup_validation_semantics(self) -> None:
        nonblocking = self.validation("validation_pass_with_followup_nonblocking")
        self.assertTrue(nonblocking["valid"])
        self.assertEqual(nonblocking["effective"]["validation_result"], "PASS")
        self.assertEqual(self.gate("validation_pass_with_followup_nonblocking").result, "ALLOW")
        blocking = self.gate("validation_pass_with_followup_blocking")
        self.assertEqual(blocking.result, "DENY")
        self.assertEqual({x.code for x in blocking.reasons}, {"BLOCKING_OPEN_QUESTION"})
        write = self.validation("validation_pass_with_followup_write")
        self.assertIn("NON_CANONICAL_WRITE", {x.code for x in write["errors"]})

    def test_verification_pass_with_followup_is_invalid(self) -> None:
        result = self.validation("verification_pass_with_followup_invalid")
        self.assertFalse(result["valid"])
        self.assertIn("SCHEMA_INVALID", {x.code for x in result["errors"]})

    def test_partial_active_and_historical_semantics(self) -> None:
        active = self.validation("verification_partial_active")
        self.assertFalse(active["valid"])
        self.assertFalse(active["migration_review_required"])
        self.assertIsNone(active["effective"]["verification_result"])
        self.assertEqual(self.gate("verification_partial_active").result, "DENY")
        for name in (
            "verification_partial_archived",
            "verification_partial_done",
            "verification_partial_archived_alias",
        ):
            with self.subTest(case=name):
                historical = self.validation(name)
                self.assertTrue(historical["valid"])
                self.assertTrue(historical["migration_review_required"])
                self.assertEqual(historical["effective"]["state"], "ARCHIVE")
                self.assertIsNone(historical["effective"]["verification_result"])
                self.assertIn("LEGACY_PARTIAL_AMBIGUOUS", {x.code for x in historical["warnings"]})
        write = self.validation("verification_partial_archived_write")
        self.assertIn("NON_CANONICAL_WRITE", {x.code for x in write["errors"]})

    def test_path_traversal_and_valid_paths(self) -> None:
        invalid = (
            "path_traversal_canonical_first",
            "path_traversal_canonical_nested",
            "path_traversal_legacy_first",
            "path_traversal_legacy_nested",
        )
        for name in invalid:
            with self.subTest(case=name):
                result = self.validation(name)
                self.assertFalse(result["valid"])
                self.assertIn("SCHEMA_INVALID", {x.code for x in result["errors"]})
        self.assertTrue(self.validation("canonical_artifact_path")["valid"])
        self.assertTrue(self.validation("legacy_artifact_path")["valid"])

    def test_tasks_to_implement_policy_matrix(self) -> None:
        expected = {
            "tasks_to_implement_no_policy": "ALLOW",
            "tasks_to_implement_policy_missing": "HUMAN_REQUIRED",
            "tasks_to_implement_policy_approved": "ALLOW",
        }
        for name, result in expected.items():
            with self.subTest(case=name):
                self.assertEqual(self.gate(name).result, result)
        record = self.cases["tasks_to_implement_no_policy"]["record"]
        gate = sdd.evaluate_transition(
            record, self.protocol, "TASKS", "IMPLEMENT",
            required_approvals=["UNKNOWN_CHECKPOINT"],
        )
        self.assertEqual(gate.result, "DENY")
        self.assertEqual({x.code for x in gate.reasons}, {"POLICY_REQUIREMENT_INVALID"})

    def test_regressions_and_audit_waiver(self) -> None:
        self.assertEqual(self.gate("validation_fail_regression").result, "ALLOW")
        self.assertEqual(self.gate("verify_fail_regression").result, "ALLOW")
        self.assertEqual(self.gate("audit_fail_without_waiver").result, "DENY")
        self.assertEqual(self.gate("audit_fail_with_valid_waiver").result, "ALLOW")

    def test_legacy_read_and_canonical_write(self) -> None:
        record = self.cases["done_legacy_alias"]["record"]
        read = sdd.validate_record(record, self.schema, self.protocol, "read")
        write = sdd.validate_record(record, self.schema, self.protocol, "write")
        self.assertTrue(read["valid"])
        self.assertFalse(write["valid"])
        self.assertIn("NON_CANONICAL_WRITE", {x.code for x in write["errors"]})

    def test_cli_exit_codes_and_migration_flag(self) -> None:
        scenarios = [
            ("canonical_valid_record", None, [], "read", 0, False),
            ("validation_pass_with_followup_nonblocking", "VALIDATION:TASKS", [], "read", 0, False),
            ("verification_partial_active", "VERIFY:AUDIT", [], "read", 1, False),
            ("verification_partial_archived", None, [], "read", 0, True),
            ("tasks_to_implement_policy_missing", "TASKS:IMPLEMENT", ["TASKS_TO_IMPLEMENT"], "read", 3, False),
            ("validation_pass_with_followup_write", None, [], "write", 1, False),
        ]
        with tempfile.TemporaryDirectory() as temp:
            for name, transition, required, mode, code, migration in scenarios:
                with self.subTest(case=name):
                    path = Path(temp) / f"{name}.json"
                    path.write_text(json.dumps(self.cases[name]["record"]), encoding="utf-8")
                    command = [sys.executable, str(VALIDATOR), str(path), "--mode", mode, "--format", "json"]
                    if transition:
                        command.extend(["--transition", transition])
                    for checkpoint in required:
                        command.extend(["--require-approval", checkpoint])
                    done = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
                    self.assertEqual(done.returncode, code, done.stderr)
                    payload = json.loads(done.stdout)
                    self.assertTrue(payload["read_only"])
                    self.assertEqual(payload["migration_review_required"], migration)

    def test_validator_is_read_only(self) -> None:
        record = self.cases["verification_partial_archived"]["record"]
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "record.json"
            path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
            before = path.read_bytes()
            before_hash = hashlib.sha256(before).hexdigest()
            before_time = path.stat().st_mtime_ns
            done = subprocess.run(
                [sys.executable, str(VALIDATOR), str(path), "--format", "json"],
                cwd=ROOT, text=True, capture_output=True, check=False,
            )
            self.assertEqual(done.returncode, 0, done.stderr)
            self.assertEqual(before, path.read_bytes())
            self.assertEqual(before_hash, hashlib.sha256(path.read_bytes()).hexdigest())
            self.assertEqual(before_time, path.stat().st_mtime_ns)
            self.assertTrue(json.loads(done.stdout)["migration_review_required"])

    def test_validator_source_has_no_file_write_operations(self) -> None:
        source = VALIDATOR.read_text(encoding="utf-8")
        for token in ("write_text(", "write_bytes(", 'open("w', "open('w", 'open("a', "open('a"):
            with self.subTest(token=token):
                self.assertNotIn(token, source)

    def test_self_check(self) -> None:
        done = subprocess.run(
            [sys.executable, str(VALIDATOR), "--self-check", "--format", "json"],
            cwd=ROOT, text=True, capture_output=True, check=False,
        )
        self.assertEqual(done.returncode, 0, done.stderr)
        payload = json.loads(done.stdout)
        self.assertTrue(payload["contracts_ok"])
        self.assertTrue(payload["read_only"])


if __name__ == "__main__":
    unittest.main()
