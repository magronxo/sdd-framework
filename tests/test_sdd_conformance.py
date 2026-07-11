from __future__ import annotations

import importlib.util
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

spec = importlib.util.spec_from_file_location(
    "sdd_conformance", TOOLS / "sdd_conformance.py"
)
assert spec and spec.loader
conformance = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = conformance
spec.loader.exec_module(conformance)


class ConformanceGuardTests(unittest.TestCase):
    def codes(self, root: Path) -> set[str]:
        return {item["code"] for item in conformance.check(root)["findings"]}

    def mutated_root(self):
        temp = tempfile.TemporaryDirectory()
        root = Path(temp.name) / "repo"
        shutil.copytree(
            ROOT, root, ignore=shutil.ignore_patterns(".git", "__pycache__")
        )
        return temp, root

    def assert_waiver_statement(self, statement: str, expected: bool) -> None:
        self.assertEqual(
            conformance._waiver_statement_authorizes_external_operation(statement),
            expected,
            statement,
        )

    def test_repository_is_conformant(self) -> None:
        result = conformance.check(ROOT)
        self.assertTrue(result["conformant"], result["findings"])
        self.assertIn("legacy_compatibility_docs", result["allowlists"])
        self.assertIn("intentional_invalid_fixtures", result["allowlists"])

    def test_detects_partial_to_audit_and_active_partial_output(self) -> None:
        temp, root = self.mutated_root()
        try:
            path = root / "01_execution/prompts/verifier.md"
            path.write_text(
                path.read_text(encoding="utf-8")
                + '\nPARTIAL -> AUDIT\n{"verification_result": "PARTIAL"}\n',
                encoding="utf-8",
            )
            codes = self.codes(root)
            self.assertIn("ACTIVE_PARTIAL_TO_AUDIT", codes)
            self.assertIn("ACTIVE_PARTIAL_OUTPUT", codes)
        finally:
            temp.cleanup()

    def test_detects_universal_human_approval(self) -> None:
        temp, root = self.mutated_root()
        try:
            path = root / "contract/v1/sdd-protocol.json"
            protocol = json.loads(path.read_text(encoding="utf-8"))
            rule = next(
                item
                for item in protocol["transitions"]
                if (item["from"], item["to"]) == ("TASKS", "IMPLEMENT")
            )
            rule["requirements"].append({"type": "human_approval"})
            path.write_text(json.dumps(protocol), encoding="utf-8")
            self.assertIn("UNIVERSAL_HUMAN_APPROVAL", self.codes(root))
        finally:
            temp.cleanup()

    def test_detects_waiver_external_authority(self) -> None:
        temp, root = self.mutated_root()
        try:
            path = root / "AGENTS.md"
            path.write_text(
                path.read_text(encoding="utf-8")
                + "\nAn owner waiver allows merge and release.\n",
                encoding="utf-8",
            )
            self.assertIn("WAIVER_EXTERNAL_AUTHORITY", self.codes(root))
        finally:
            temp.cleanup()

    def test_detects_owner_waiver_only_allows_merge(self) -> None:
        self.assert_waiver_statement("An owner waiver only allows merge.", True)

    def test_owner_waiver_archive_only_scope_is_not_detected(self) -> None:
        self.assert_waiver_statement(
            "An owner waiver applies only to AUDIT -> ARCHIVE.", False
        )

    def test_owner_waiver_external_negation_is_not_detected(self) -> None:
        self.assert_waiver_statement(
            "An owner waiver does not authorize merge, release, deploy, or push.",
            False,
        )

    def test_owner_waiver_no_external_effect_is_not_detected(self) -> None:
        self.assert_waiver_statement(
            "An owner waiver has no effect on external operations.", False
        )

    def test_detects_waiver_regression_in_operational_prompt(self) -> None:
        temp, root = self.mutated_root()
        try:
            path = root / "01_execution/prompts/verifier.md"
            path.write_text(
                path.read_text(encoding="utf-8")
                + "\nAn owner waiver unblocks deploy or push.\n",
                encoding="utf-8",
            )
            self.assertIn("WAIVER_EXTERNAL_AUTHORITY", self.codes(root))
        finally:
            temp.cleanup()

    def test_detects_mixed_negated_merge_but_permitted_release(self) -> None:
        self.assert_waiver_statement(
            "An owner waiver does not authorize merge but permits release.", True
        )

    def test_detects_mixed_archive_scope_and_allowed_merge(self) -> None:
        self.assert_waiver_statement(
            "An owner waiver applies only to AUDIT -> ARCHIVE and allows merge.",
            True,
        )

    def test_detects_mixed_no_external_effect_and_allowed_deploy(self) -> None:
        self.assert_waiver_statement(
            "An owner waiver has no effect on external operations but allows deploy.",
            True,
        )

    def test_detects_mixed_negated_push_and_unblocked_release(self) -> None:
        self.assert_waiver_statement(
            "An owner waiver cannot authorize push; however, it unblocks release.",
            True,
        )

    def test_detects_mixed_negated_release_and_allowed_merge(self) -> None:
        self.assert_waiver_statement(
            "An owner waiver does not permit release, although it allows merge.",
            True,
        )

    def test_accepts_two_locally_negated_external_authorizations(self) -> None:
        self.assert_waiver_statement(
            "An owner waiver cannot permit merge and must not unblock release.",
            False,
        )

    def test_accepts_archive_authorization_and_external_negation(self) -> None:
        self.assert_waiver_statement(
            "The waiver allows AUDIT -> ARCHIVE only and does not authorize external operations.",
            False,
        )

    def test_waiver_scan_covers_all_required_authority_and_prompt_markdown(self) -> None:
        actual = {
            path.relative_to(ROOT).as_posix()
            for path in conformance._waiver_scan_paths()
        }
        expected = {
            "README.md",
            "AGENTS.md",
            "contract/v1/README.md",
        }
        for directory in (
            ROOT / "00_core",
            ROOT / "02_policies",
            ROOT / "01_execution/prompts",
        ):
            expected.update(
                path.relative_to(ROOT).as_posix()
                for path in directory.rglob("*.md")
            )
        self.assertEqual(actual, expected)

    def test_detects_authority_order_and_install_documentation_drift(self) -> None:
        temp, root = self.mutated_root()
        try:
            agents = root / "AGENTS.md"
            agents.write_text(
                agents.read_text(encoding="utf-8").replace(
                    "2. `docs/sdd/contract/v1/feature-record.schema.json`\n", ""
                ),
                encoding="utf-8",
            )
            readme = root / "README.md"
            readme.write_text(
                readme.read_text(encoding="utf-8").replace(
                    "python tools/sdd_install.py --target",
                    "python legacy-copy --target",
                ),
                encoding="utf-8",
            )
            codes = self.codes(root)
            self.assertIn("AUTHORITY_ORDER_INVALID", codes)
            self.assertIn("INSTALL_DOCUMENTATION_INCOMPLETE", codes)
        finally:
            temp.cleanup()

    def test_detects_lifecycle_and_root_path_drift(self) -> None:
        temp, root = self.mutated_root()
        try:
            agents = root / "AGENTS.md"
            agents.write_text(
                agents.read_text(encoding="utf-8")
                + "\nDESIGN -> TASKS -> IMPLEMENT -> ARCHIVE\n",
                encoding="utf-8",
            )
            policy = root / "02_policies/LEGACY_SPECS_POLICY.md"
            policy.write_text(
                policy.read_text(encoding="utf-8")
                + "\nWrite to artifacts/specs/example.md.\n",
                encoding="utf-8",
            )
            codes = self.codes(root)
            self.assertIn("LIFECYCLE_DRIFT", codes)
            self.assertIn("ROOT_PATH_DRIFT", codes)
        finally:
            temp.cleanup()

    def test_detects_manifest_missing_source_outside_and_collision(self) -> None:
        mutations = []

        def missing(root, raw):
            raw["entries"][0]["source"] = "missing/file.txt"

        def outside(root, raw):
            raw["entries"][0]["destination"] = "outside/file.txt"

        def duplicate(root, raw):
            raw["entries"][1]["destination"] = raw["entries"][0]["destination"]

        mutations.extend([missing, outside, duplicate])
        for mutation in mutations:
            temp, root = self.mutated_root()
            try:
                path = root / "contract/v1/install-manifest.json"
                raw = json.loads(path.read_text(encoding="utf-8"))
                mutation(root, raw)
                path.write_text(json.dumps(raw), encoding="utf-8")
                self.assertIn("INSTALL_MANIFEST_INVALID", self.codes(root))
            finally:
                temp.cleanup()


if __name__ == "__main__":
    unittest.main()
