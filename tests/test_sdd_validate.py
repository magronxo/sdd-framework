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
VALIDATOR_PATH = ROOT / "tools" / "sdd_validate.py"
SCHEMA_PATH = ROOT / "contract" / "v1" / "feature-record.schema.json"
PROTOCOL_PATH = ROOT / "contract" / "v1" / "sdd-protocol.json"
FIXTURE_PATH = ROOT / "tests" / "fixtures" / "v1" / "feature-record-cases.json"

spec = importlib.util.spec_from_file_location("sdd_validate", VALIDATOR_PATH)
assert spec and spec.loader
sdd_validate = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = sdd_validate
spec.loader.exec_module(sdd_validate)


class CanonicalSddV1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema, cls.protocol = sdd_validate.load_contracts(
            SCHEMA_PATH, PROTOCOL_PATH
        )
        cls.fixtures = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
        cls.cases = {item["name"]: item for item in cls.fixtures["cases"]}

    def test_contract_lifecycle_and_gate_results_are_exact(self) -> None:
        self.assertEqual(
            self.protocol["lifecycle"]["persistent_states"],
            [
                "DESIGN",
                "SPEC",
                "VALIDATION",
                "TASKS",
                "IMPLEMENT",
                "VERIFY",
                "AUDIT",
                "ARCHIVE",
            ],
        )
        self.assertEqual(
            self.protocol["lifecycle"]["pre_record_activities"],
            ["SEED", "INTAKE"],
        )
        self.assertEqual(
            self.protocol["gate_results"],
            ["ALLOW", "DENY", "HUMAN_REQUIRED"],
        )

    def test_tasks_to_implement_approval_is_conditional_not_universal(self) -> None:
        policy = self.protocol["human_approval_policy"]
        checkpoint = self.protocol["human_checkpoints"]["TASKS_TO_IMPLEMENT"]
        task_rule = next(
            item
            for item in self.protocol["transitions"]
            if item["from"] == "TASKS" and item["to"] == "IMPLEMENT"
        )
        self.assertEqual(policy["core_default"], "not_required")
        self.assertEqual(policy["resolution_mode"], "external_input_only")
        self.assertFalse(policy["integration_implemented"])
        self.assertFalse(checkpoint["default_required"])
        self.assertEqual(task_rule["policy_hooks"], ["TASKS_TO_IMPLEMENT"])
        self.assertNotIn(
            "human_approval",
            {requirement["type"] for requirement in task_rule["requirements"]},
        )

    def test_fixture_manifest_contains_all_required_cases(self) -> None:
        expected = {
            "canonical_valid_record",
            "non_canonical_state",
            "done_legacy_alias",
            "feature_id_legacy_alias",
            "canonical_artifact_path",
            "legacy_artifact_path",
            "verification_partial",
            "pass_with_followup",
            "blocking_open_question",
            "tasks_to_implement_without_approval_policy",
            "tasks_to_implement_policy_requires_approval",
            "tasks_to_implement_policy_with_approval",
            "audit_fail_without_waiver",
            "audit_fail_with_valid_waiver",
            "alias_divergence",
            "illegal_transition",
            "validation_fail_regression",
            "verify_fail_regression",
            "archived_legacy_alias",
            "tasks_path_legacy_alias",
        }
        self.assertEqual(set(self.cases), expected)

    def test_all_fixture_cases(self) -> None:
        for case in self.fixtures["cases"]:
            with self.subTest(case=case["name"]):
                validation = sdd_validate.validate_record(
                    case["record"],
                    self.schema,
                    self.protocol,
                    case.get("mode", "read"),
                )
                expected = case["expect"]
                self.assertEqual(validation["valid"], expected["valid"])
                self.assertEqual(
                    sorted(item.code for item in validation["warnings"]),
                    sorted(expected["warning_codes"]),
                )
                self.assertEqual(
                    sorted(set(item.code for item in validation["errors"])),
                    sorted(expected["error_codes"]),
                )

                transition = case.get("transition")
                if transition:
                    gate = sdd_validate.evaluate_transition(
                        case["record"],
                        self.protocol,
                        transition["from"],
                        transition["to"],
                        transition.get("approvals", []),
                        transition.get("required_approvals", []),
                    )
                    self.assertEqual(gate.result, transition["result"])
                    self.assertEqual(
                        sorted(item.code for item in gate.reasons),
                        sorted(transition["reason_codes"]),
                    )

    def test_tasks_to_implement_policy_matrix(self) -> None:
        expected = {
            "tasks_to_implement_without_approval_policy": "ALLOW",
            "tasks_to_implement_policy_requires_approval": "HUMAN_REQUIRED",
            "tasks_to_implement_policy_with_approval": "ALLOW",
        }
        for name, result in expected.items():
            with self.subTest(case=name):
                case = self.cases[name]
                transition = case["transition"]
                gate = sdd_validate.evaluate_transition(
                    case["record"],
                    self.protocol,
                    "TASKS",
                    "IMPLEMENT",
                    transition["approvals"],
                    transition["required_approvals"],
                )
                self.assertEqual(gate.result, result)

    def test_unknown_or_non_applicable_policy_checkpoint_is_denied(self) -> None:
        case = self.cases["tasks_to_implement_without_approval_policy"]
        gate = sdd_validate.evaluate_transition(
            case["record"],
            self.protocol,
            "TASKS",
            "IMPLEMENT",
            required_approvals=["UNKNOWN_CHECKPOINT"],
        )
        self.assertEqual(gate.result, "DENY")
        self.assertEqual(
            {item.code for item in gate.reasons},
            {"POLICY_REQUIREMENT_INVALID"},
        )

    def test_legacy_read_is_warning_but_canonical_write_is_rejected(self) -> None:
        case = self.cases["done_legacy_alias"]
        read_result = sdd_validate.validate_record(
            case["record"], self.schema, self.protocol, "read"
        )
        write_result = sdd_validate.validate_record(
            case["record"], self.schema, self.protocol, "write"
        )
        self.assertTrue(read_result["valid"])
        self.assertFalse(write_result["valid"])
        self.assertIn(
            "NON_CANONICAL_WRITE",
            {item.code for item in write_result["errors"]},
        )

    def test_schema_does_not_define_workflow_or_gate_profiles(self) -> None:
        serialized = json.dumps(self.schema)
        self.assertNotIn('"transitions"', serialized)
        self.assertNotIn('"regressions"', serialized)
        self.assertNotIn('"gate_results"', serialized)
        self.assertNotIn('"human_checkpoints"', serialized)

    def test_protocol_does_not_duplicate_feature_record_properties(self) -> None:
        self.assertNotIn("properties", self.protocol)
        self.assertNotIn("$defs", self.protocol)
        self.assertEqual(
            self.protocol["authority"]["feature_record_shape"],
            "contract/v1/feature-record.schema.json",
        )

    def test_schema_has_only_singular_primary_artifact_fields(self) -> None:
        properties = self.schema["properties"]
        self.assertIn("design_path", properties)
        self.assertIn("spec_path", properties)
        self.assertIn("task_path", properties)
        self.assertNotIn("design_artifacts", properties)
        self.assertNotIn("spec_artifacts", properties)
        self.assertNotIn("task_artifacts", properties)

    def test_audit_warn_allows_archive(self) -> None:
        record = {
            "id": "feat-904-audit-warn",
            "type": "SYSTEM_SPEC",
            "state": "AUDIT",
            "title": "Audit warning fixture",
            "created_at": "2026-07-11T09:00:00Z",
            "updated_at": "2026-07-11T10:00:00Z",
            "open_questions": [],
            "audit_result": "WARN",
            "audited_at": "2026-07-11T09:50:00Z",
        }
        validation = sdd_validate.validate_record(
            record, self.schema, self.protocol
        )
        gate = sdd_validate.evaluate_transition(
            record, self.protocol, "AUDIT", "ARCHIVE"
        )
        self.assertTrue(validation["valid"])
        self.assertEqual(gate.result, "ALLOW")

    def test_transition_source_must_match_record_state(self) -> None:
        case = self.cases["canonical_artifact_path"]
        gate = sdd_validate.evaluate_transition(
            case["record"], self.protocol, "SPEC", "VALIDATION"
        )
        self.assertEqual(gate.result, "DENY")
        self.assertEqual(
            {item.code for item in gate.reasons},
            {"SOURCE_STATE_MISMATCH"},
        )

    def test_cli_json_output_and_exit_codes(self) -> None:
        scenarios = [
            ("canonical_valid_record", None, [], 0, None),
            ("verification_partial", "VERIFY:AUDIT", [], 1, "DENY"),
            (
                "tasks_to_implement_without_approval_policy",
                "TASKS:IMPLEMENT",
                [],
                0,
                "ALLOW",
            ),
            (
                "tasks_to_implement_policy_requires_approval",
                "TASKS:IMPLEMENT",
                ["--require-approval", "TASKS_TO_IMPLEMENT"],
                3,
                "HUMAN_REQUIRED",
            ),
            (
                "tasks_to_implement_policy_with_approval",
                "TASKS:IMPLEMENT",
                [
                    "--require-approval",
                    "TASKS_TO_IMPLEMENT",
                    "--approval",
                    "TASKS_TO_IMPLEMENT",
                ],
                0,
                "ALLOW",
            ),
        ]
        with tempfile.TemporaryDirectory() as temp_dir:
            for name, transition, extra_args, expected_code, expected_gate in scenarios:
                with self.subTest(case=name):
                    path = Path(temp_dir) / f"{name}.json"
                    path.write_text(
                        json.dumps(self.cases[name]["record"]),
                        encoding="utf-8",
                    )
                    command = [
                        sys.executable,
                        str(VALIDATOR_PATH),
                        str(path),
                        "--format",
                        "json",
                    ]
                    if transition:
                        command.extend(["--transition", transition])
                    command.extend(extra_args)
                    completed = subprocess.run(
                        command,
                        cwd=ROOT,
                        text=True,
                        capture_output=True,
                        check=False,
                    )
                    self.assertEqual(
                        completed.returncode,
                        expected_code,
                        completed.stderr,
                    )
                    payload = json.loads(completed.stdout)
                    self.assertTrue(payload["read_only"])
                    if expected_gate is not None:
                        self.assertEqual(payload["gate"]["result"], expected_gate)

    def test_validator_is_read_only_for_input_file(self) -> None:
        case = self.cases["legacy_artifact_path"]
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "record.json"
            path.write_text(
                json.dumps(case["record"], indent=2) + "\n",
                encoding="utf-8",
            )
            before_bytes = path.read_bytes()
            before_hash = hashlib.sha256(before_bytes).hexdigest()
            before_stat = path.stat()

            completed = subprocess.run(
                [
                    sys.executable,
                    str(VALIDATOR_PATH),
                    str(path),
                    "--format",
                    "json",
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            after_bytes = path.read_bytes()
            after_hash = hashlib.sha256(after_bytes).hexdigest()
            after_stat = path.stat()
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertEqual(before_hash, after_hash)
            self.assertEqual(before_bytes, after_bytes)
            self.assertEqual(before_stat.st_mtime_ns, after_stat.st_mtime_ns)

    def test_validator_source_contains_no_write_operations(self) -> None:
        source = VALIDATOR_PATH.read_text(encoding="utf-8")
        forbidden = (
            "write_text(",
            "write_bytes(",
            'open("w',
            "open('w",
            'open("a',
            "open('a",
        )
        for token in forbidden:
            with self.subTest(token=token):
                self.assertNotIn(token, source)

    def test_self_check(self) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                str(VALIDATOR_PATH),
                "--self-check",
                "--format",
                "json",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        payload = json.loads(completed.stdout)
        self.assertTrue(payload["contracts_ok"])
        self.assertTrue(payload["read_only"])


if __name__ == "__main__":
    unittest.main()
