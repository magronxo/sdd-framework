from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "tools/sdd_validate.py"
INSTALLER = ROOT / "tools/sdd_install.py"
INSTALL_MANIFEST = ROOT / "contract/v1/install-manifest.json"
TUTORIAL = ROOT / "docs/GETTING_STARTED.md"
PROMPT_ROOT = ROOT / "01_execution/prompts"
PROMPT_NAMES = (
    "designer.md",
    "specifier.md",
    "validator.md",
    "planner.md",
    "implementer.md",
    "verifier.md",
    "migration_auditor.md",
)
COMPATIBILITY_DOCS = {
    "00_core/SDD_FEATURE_FORMAT.md",
    "00_core/SDD_RUNTIME.md",
}
BARE_ARTIFACT_LINE_ALLOWLIST = {
    "04_project_governance/PROJECT_MAP.md": ("└── artifacts/",),
    "docs/PROJECT_TOUR.md": ("└─ artifacts/",),
}

spec = importlib.util.spec_from_file_location("manual_lifecycle_sdd_validate", VALIDATOR)
assert spec and spec.loader
sdd = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = sdd
spec.loader.exec_module(sdd)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def extract_json_after(text: str, marker: str) -> dict:
    match = re.search(
        re.escape(marker) + r".*?```json\n(.*?)\n```",
        text,
        flags=re.DOTALL,
    )
    if match is None:
        raise AssertionError(f"JSON block not found after marker: {marker}")
    value = json.loads(match.group(1))
    require(isinstance(value, dict), f"JSON block after {marker} must be an object")
    return value


def canonical_base_record(state: str = "DESIGN") -> dict:
    return {
        "id": "feat-900-semantic-regression",
        "type": "SYSTEM_SPEC",
        "state": state,
        "title": "Semantic regression fixture",
        "created_at": "2026-08-01T00:00:00Z",
        "updated_at": "2026-08-01T00:00:00Z",
    }


def normalized_patch(patch: dict) -> dict:
    normalized = deepcopy(patch)
    for field in tuple(normalized):
        if field.endswith("_at"):
            normalized[field] = "2026-08-01T00:10:00Z"
    return normalized


def assert_patch_fields(patch: dict, schema: dict, label: str) -> None:
    allowed = set(schema["properties"])
    unknown = set(patch) - allowed
    require(not unknown, f"{label} contains unknown feature-record fields: {sorted(unknown)}")


def assert_write_valid(record: dict, schema: dict, protocol: dict, label: str) -> None:
    result = sdd.validate_record(record, schema, protocol, mode="write")
    require(result["valid"], f"{label} is not canonical-write valid: {result['errors']}")
    require(not result["warnings"], f"{label} emitted canonical-write warnings: {result['warnings']}")


def apply_claimed_transition(
    source: dict,
    patch: dict,
    schema: dict,
    protocol: dict,
    from_state: str,
    to_state: str,
    label: str,
) -> dict:
    patch = normalized_patch(patch)
    assert_patch_fields(patch, schema, label)
    require(patch.get("state") == to_state, f"{label} targets {patch.get('state')}, expected {to_state}")

    gate_record = {**source, **patch, "state": from_state}
    assert_write_valid(gate_record, schema, protocol, f"{label} source-state evidence")
    gate = sdd.evaluate_transition(gate_record, protocol, from_state, to_state)
    require(gate.result == "ALLOW", f"{label} transition denied: {gate.reasons}")

    target = {**source, **patch}
    assert_write_valid(target, schema, protocol, f"{label} target record")
    return target


def read_prompt_texts(prompt_root: Path) -> dict[str, str]:
    return {
        name: (prompt_root / name).read_text(encoding="utf-8")
        for name in PROMPT_NAMES
    }


def assert_prompt_semantics(
    prompts: dict[str, str], schema: dict, protocol: dict
) -> dict[str, dict]:
    for name, text in prompts.items():
        require(
            re.search(r"(?<!docs/sdd/)artifacts/", text) is None,
            f"{name} contains a current root-level artifact path",
        )
    assert_implementer_installed_authority_paths(prompts["implementer.md"])

    record = canonical_base_record()
    designer_patch = extract_json_after(
        prompts["designer.md"], "Apply this PATCH (fields to update) to the feature record:"
    )
    record = apply_claimed_transition(
        record, designer_patch, schema, protocol, "DESIGN", "SPEC", "Designer PATCH"
    )

    specifier_patch = extract_json_after(
        prompts["specifier.md"], "Apply this PATCH (fields to update) to the feature record:"
    )
    record = apply_claimed_transition(
        record, specifier_patch, schema, protocol, "SPEC", "VALIDATION", "Specifier PATCH"
    )
    scenarios = specifier_patch.get("sdt_scenarios")
    require(
        isinstance(scenarios, list)
        and scenarios
        and all(isinstance(item, dict) for item in scenarios),
        "Specifier sdt_scenarios must be a non-empty array of objects",
    )
    validation_source = deepcopy(record)

    pass_patch = extract_json_after(
        prompts["validator.md"],
        "PASS — apply this PATCH (fields to update) to the feature record:",
    )
    require(pass_patch.get("validation_result") == "PASS", "Validator PASS result drift")
    require("validated_at" in pass_patch, "Validator PASS lacks validated_at")
    require("validation_issues" not in pass_patch, "Validator PASS must not require issues")
    task_record = apply_claimed_transition(
        validation_source,
        pass_patch,
        schema,
        protocol,
        "VALIDATION",
        "TASKS",
        "Validator PASS PATCH",
    )

    fail_patch = extract_json_after(
        prompts["validator.md"],
        "FAIL — apply this PATCH (fields to update) to the feature record:",
    )
    require(fail_patch.get("validation_result") == "FAIL", "Validator FAIL result drift")
    require("validated_at" in fail_patch, "Validator FAIL lacks validated_at")
    require(
        isinstance(fail_patch.get("validation_issues"), list)
        and fail_patch["validation_issues"],
        "Validator FAIL requires a non-empty validation_issues list",
    )
    apply_claimed_transition(
        validation_source,
        fail_patch,
        schema,
        protocol,
        "VALIDATION",
        "SPEC",
        "Validator FAIL PATCH",
    )

    planner_patch = extract_json_after(
        prompts["planner.md"],
        "After the task document is complete, apply this PATCH (fields to update) to the feature record:",
    )
    implement_record = apply_claimed_transition(
        task_record,
        planner_patch,
        schema,
        protocol,
        "TASKS",
        "IMPLEMENT",
        "Planner PATCH",
    )
    require("task_path" in planner_patch, "Planner PATCH lacks task_path")
    require("tasks_path" not in planner_patch, "Planner PATCH uses legacy tasks_path")

    implementer_patch = extract_json_after(
        prompts["implementer.md"],
        "When ALL tasks and required evidence are complete, apply this PATCH (fields to update) to the feature record:",
    )
    verify_record = apply_claimed_transition(
        implement_record,
        implementer_patch,
        schema,
        protocol,
        "IMPLEMENT",
        "VERIFY",
        "Implementer PATCH",
    )

    verifier_pass = extract_json_after(prompts["verifier.md"], "### PASS — handoff to AUDIT")
    require(verifier_pass.get("verification_result") == "PASS", "Verifier PASS result drift")
    require("verified_at" in verifier_pass, "Verifier PASS lacks verified_at")
    audit_record = apply_claimed_transition(
        verify_record,
        verifier_pass,
        schema,
        protocol,
        "VERIFY",
        "AUDIT",
        "Verifier PASS PATCH",
    )

    verifier_fail = extract_json_after(prompts["verifier.md"], "### FAIL — return to IMPLEMENT")
    require(verifier_fail.get("verification_result") == "FAIL", "Verifier FAIL result drift")
    require("verified_at" in verifier_fail, "Verifier FAIL lacks verified_at")
    apply_claimed_transition(
        verify_record,
        verifier_fail,
        schema,
        protocol,
        "VERIFY",
        "IMPLEMENT",
        "Verifier FAIL PATCH",
    )

    not_executed = normalized_patch(
        extract_json_after(prompts["verifier.md"], "### NOT EXECUTED — remain in VERIFY")
    )
    assert_patch_fields(not_executed, schema, "Verifier NOT EXECUTED PATCH")
    require(not_executed.get("state") == "VERIFY", "NOT EXECUTED must remain VERIFY")
    require("verification_result" not in not_executed, "NOT EXECUTED must omit verification_result")
    require("verified_at" not in not_executed, "NOT EXECUTED must omit verified_at")
    not_executed_record = {**verify_record, **not_executed}
    assert_write_valid(not_executed_record, schema, protocol, "Verifier NOT EXECUTED record")
    denied = sdd.evaluate_transition(not_executed_record, protocol, "VERIFY", "AUDIT")
    require(denied.result == "DENY", "NOT EXECUTED must not permit VERIFY -> AUDIT")
    require(
        {item.code for item in denied.reasons} == {"VERIFICATION_NOT_EXECUTED"},
        f"Unexpected NOT EXECUTED blockers: {denied.reasons}",
    )

    migration = prompts["migration_auditor.md"]
    require("PARITY REPORT examples only" in migration, "Migration examples lack report-local label")
    for marker, expected in (
        ("### PARITY_PASS report example", "PARITY_PASS"),
        ("### PARITY_WARN report example", "PARITY_WARN"),
        ("### PARITY_FAIL report example", "PARITY_FAIL"),
    ):
        report = extract_json_after(migration, marker)
        require(report.get("migration_result") == expected, f"{marker} result drift")
        require("state" not in report, f"{marker} must not claim canonical state")
        require("recommended_next_action" in report, f"{marker} lacks recommendation")

    return {
        "DESIGN": canonical_base_record(),
        "VALIDATION": validation_source,
        "TASKS": task_record,
        "IMPLEMENT": implement_record,
        "VERIFY": verify_record,
        "AUDIT": audit_record,
    }


def current_surface_paths(root: Path) -> list[Path]:
    paths = [
        root / "README.md",
        root / "AGENTS.md",
        root / "SDD_BOOTSTRAP_CHECKLIST.md",
        root / "docs/GETTING_STARTED.md",
        root / "docs/PROJECT_TOUR.md",
        root / "docs/SDD_PIPELINE_VISUAL.md",
    ]
    for pattern in (
        "00_core/*.md",
        "01_execution/prompts/*.md",
        "02_policies/*.md",
        "03_operations/pre_sdd/*.md",
        "03_operations/pre_sdd/templates/*.md",
        "04_project_governance/*.md",
        "templates/*.md",
    ):
        paths.extend(sorted(root.glob(pattern)))
    return sorted(set(paths))


def assert_tutorial_implementation_correction_semantics(
    tutorial: str, protocol: dict
) -> None:
    declared = {
        (rule.get("from"), rule.get("to"))
        for rule in protocol.get("transitions", []) + protocol.get("regressions", [])
    }
    source = canonical_base_record("IMPLEMENT")
    for target in ("SPEC", "VALIDATION"):
        require(
            ("IMPLEMENT", target) not in declared,
            f"Protocol unexpectedly declares IMPLEMENT -> {target}",
        )
        gate = sdd.evaluate_transition(source, protocol, "IMPLEMENT", target)
        require(gate.result == "DENY", f"IMPLEMENT -> {target} must be denied")
        require(
            {item.code for item in gate.reasons} == {"INVALID_TRANSITION"},
            f"IMPLEMENT -> {target} did not fail as an undeclared transition: {gate.reasons}",
        )

    active_route_patterns = (
        r"(?im)^(?![^\n]*\b(?:no|not|undeclared)\b)[^\n]*\bIMPLEMENT\s*->\s*(?:SPEC|VALIDATION)\b",
        r"(?is)\breopen the spec\b.{0,120}\bre-?run VALIDATION\b",
    )
    for pattern in active_route_patterns:
        require(
            re.search(pattern, tutorial) is None,
            "Getting Started claims an undeclared IMPLEMENT correction route",
        )
    require("Stop implementation." in tutorial, "IMPLEMENT spec defects must stop implementation")
    require(
        "do not silently modify the validated spec" in tutorial
        and "undeclared transition" in tutorial,
        "Getting Started lacks fail-closed IMPLEMENT correction guidance",
    )


def assert_implementer_installed_authority_paths(prompt: str) -> None:
    match = re.search(
        r"^## Must Read \(strict\)\n(.*?)(?=^---$)",
        prompt,
        flags=re.DOTALL | re.MULTILINE,
    )
    require(match is not None, "Implementer strict-read block is missing")
    strict_reads = match.group(1)
    installed = (
        "docs/sdd/AGENTS.md",
        "docs/sdd/00_core/SDD_RUNTIME.md",
        "docs/sdd/00_core/SDD_HANDOFF_CONTRACT.md",
        "docs/sdd/sdd.config.json",
    )
    bare = (
        "AGENTS.md",
        "00_core/SDD_RUNTIME.md",
        "00_core/SDD_HANDOFF_CONTRACT.md",
        "sdd.config.json",
    )
    for path in installed:
        require(f"`{path}`" in strict_reads, f"Implementer strict reads lack installed path {path}")
    for path in bare:
        require(f"`{path}`" not in strict_reads, f"Implementer strict reads use bare path {path}")
    require("`sdd.config.json`" not in prompt, "Implementer uses bare config path outside strict reads")


def _markdown_h2_section(text: str, heading: str) -> str:
    marker = f"## {heading}\n"
    start = text.find(marker)
    require(start >= 0, f"Markdown section is missing: {heading}")
    body_start = start + len(marker)
    next_heading = re.search(r"^## ", text[body_start:], flags=re.MULTILINE)
    end = body_start + next_heading.start() if next_heading else len(text)
    return text[body_start:end]


def _manifest_installs_static_document(path: str, manifest: dict, root: Path) -> bool:
    candidate = PurePosixPath(path)
    for entry in manifest.get("entries", []):
        destination = PurePosixPath(entry["destination"])
        source = root / entry["source"]
        if entry["source_kind"] == "file" and candidate == destination:
            return source.is_file()
        if entry["source_kind"] == "directory" and candidate.is_relative_to(destination):
            relative = candidate.relative_to(destination)
            return (source / Path(*relative.parts)).is_file()
    return False


def assert_tutorial_installed_navigation(tutorial: str, manifest: dict, root: Path) -> None:
    navigation = _markdown_h2_section(tutorial, "Next Steps") + _markdown_h2_section(
        tutorial, "Related Documents"
    )
    installed_paths = re.findall(r"`(docs/sdd/[^`]+)`", navigation)
    require(installed_paths, "Getting Started installed navigation is empty")
    runtime_generated_prefixes = (
        "docs/sdd/artifacts/",
        "docs/sdd/03_operations/pre_sdd/seeds/",
    )
    static_paths = [
        path
        for path in installed_paths
        if not path.startswith(runtime_generated_prefixes)
    ]
    for path in static_paths:
        require(
            _manifest_installs_static_document(path, manifest, root),
            f"Getting Started navigation is not manifest-backed: {path}",
        )


def assert_current_use_semantics(
    root: Path, overrides: dict[str, str] | None = None
) -> None:
    overrides = overrides or {}
    for path in current_surface_paths(root):
        relative = path.relative_to(root).as_posix()
        text = overrides.get(relative, path.read_text(encoding="utf-8"))

        if relative not in COMPATIBILITY_DOCS:
            require("PASS_WITH_FOLLOWUP" not in text, f"active legacy validation guidance in {relative}")
            require("PARTIAL" not in text, f"active PARTIAL guidance in {relative}")
            require("tasks_path" not in text, f"active tasks_path guidance in {relative}")

        for token in (
            "seed_reference",
            "migration_source",
            "migration_target",
            "reopened_at",
            "reopened_reason",
        ):
            require(token not in text, f"unsupported feature-record field {token} in {relative}")

        if relative == "00_core/SDD_FEATURE_FORMAT.md":
            continue
        allowed_lines = BARE_ARTIFACT_LINE_ALLOWLIST.get(relative, ())
        for line in text.splitlines():
            if re.search(r"(?<!docs/sdd/)artifacts/", line):
                require(
                    any(allowed in line for allowed in allowed_lines),
                    f"current root-level artifact path in {relative}: {line.strip()}",
                )


class ManualLifecycleCanonicalV1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema, cls.protocol = sdd.load_contracts()
        cls.tutorial = TUTORIAL.read_text(encoding="utf-8")
        cls.records = cls._tutorial_records()

    @classmethod
    def _tutorial_records(cls) -> dict[str, dict]:
        record = extract_json_after(cls.tutorial, "**Complete feature record:**")
        records = {"DESIGN": deepcopy(record)}
        patches = (
            ("SPEC", "**Feature record PATCH (fields to update) — DESIGN to SPEC:**"),
            ("VALIDATION", "**Feature record PATCH (fields to update) — SPEC to VALIDATION:**"),
            ("TASKS", "**Feature record PATCH (fields to update) — VALIDATION to TASKS:**"),
            ("IMPLEMENT", "**Feature record PATCH (fields to update) — TASKS to IMPLEMENT:**"),
            ("VERIFY", "**Feature record PATCH (fields to update) — IMPLEMENT to VERIFY:**"),
        )
        for state, marker in patches:
            patch = extract_json_after(cls.tutorial, marker)
            assert_patch_fields(patch, cls.schema, marker)
            record.update(patch)
            require(record["state"] == state, f"{marker} produced wrong state")
            records[state] = deepcopy(record)

        for marker in (
            "**Feature record PATCH (fields to update) — VERIFY to AUDIT:**",
            "**Feature record PATCH (fields to update) — record the AUDIT decision:**",
        ):
            patch = extract_json_after(cls.tutorial, marker)
            assert_patch_fields(patch, cls.schema, marker)
            record.update(patch)
        records["AUDIT"] = deepcopy(record)

        archive = extract_json_after(
            cls.tutorial,
            "**Feature record PATCH (fields to update) — AUDIT to ARCHIVE:**",
        )
        assert_patch_fields(archive, cls.schema, "Tutorial ARCHIVE PATCH")
        record.update(archive)
        records["ARCHIVE"] = deepcopy(record)
        return records

    def test_prompt_feature_patches_and_transitions_are_semantic(self) -> None:
        assert_prompt_semantics(read_prompt_texts(PROMPT_ROOT), self.schema, self.protocol)

    def test_implementer_uses_installed_authority_paths(self) -> None:
        prompt = (PROMPT_ROOT / "implementer.md").read_text(encoding="utf-8")
        assert_implementer_installed_authority_paths(prompt)
        mutated = prompt.replace("`docs/sdd/AGENTS.md`", "`AGENTS.md`", 1)
        with self.assertRaises(AssertionError):
            assert_implementer_installed_authority_paths(mutated)

    def test_tutorial_implementation_correction_guidance_matches_protocol(self) -> None:
        assert_tutorial_implementation_correction_semantics(self.tutorial, self.protocol)
        injections = (
            "\nDuring IMPLEMENT, use IMPLEMENT -> SPEC to correct the spec.\n",
            "\nDuring IMPLEMENT, reopen the spec and re-run VALIDATION.\n",
        )
        for injection in injections:
            with self.subTest(injection=injection.strip()):
                with self.assertRaises(AssertionError):
                    assert_tutorial_implementation_correction_semantics(
                        self.tutorial + injection, self.protocol
                    )

    def test_tutorial_installed_navigation_is_manifest_backed(self) -> None:
        manifest = json.loads(INSTALL_MANIFEST.read_text(encoding="utf-8"))
        assert_tutorial_installed_navigation(self.tutorial, manifest, ROOT)
        mutated = self.tutorial.replace(
            "## Related Documents",
            "- `docs/sdd/docs/PROJECT_TOUR.md` — installed tour\n\n## Related Documents",
            1,
        )
        with self.assertRaises(AssertionError):
            assert_tutorial_installed_navigation(mutated, manifest, ROOT)

    def test_validator_swapped_state_mutation_is_rejected(self) -> None:
        prompts = read_prompt_texts(PROMPT_ROOT)
        validator = prompts["validator.md"]
        validator = validator.replace('"state": "TASKS"', '"state": "__SWAP__"', 1)
        validator = validator.replace('"state": "SPEC"', '"state": "TASKS"', 1)
        validator = validator.replace('"state": "__SWAP__"', '"state": "SPEC"', 1)
        prompts["validator.md"] = validator
        with self.assertRaises(AssertionError):
            assert_prompt_semantics(prompts, self.schema, self.protocol)

    def test_tutorial_records_are_canonical_write_valid(self) -> None:
        self.assertEqual(
            tuple(self.records),
            ("DESIGN", "SPEC", "VALIDATION", "TASKS", "IMPLEMENT", "VERIFY", "AUDIT", "ARCHIVE"),
        )
        for state, record in self.records.items():
            with self.subTest(state=state):
                assert_write_valid(record, self.schema, self.protocol, f"Tutorial {state}")
                self.assertEqual(record["state"], state)
                for field, value in record.items():
                    if field.endswith("_path"):
                        self.assertTrue(value.startswith("docs/sdd/artifacts/"))
        self.assertIn("validated_at", self.records["TASKS"])
        self.assertIn("verified_at", self.records["AUDIT"])
        self.assertIn("audited_at", self.records["AUDIT"])
        self.assertIn("task_path", self.records["IMPLEMENT"])
        self.assertIn("archived_at", self.records["ARCHIVE"])

    def test_forward_transition_matrix(self) -> None:
        for source, target in (
            ("DESIGN", "SPEC"),
            ("SPEC", "VALIDATION"),
            ("VALIDATION", "TASKS"),
            ("TASKS", "IMPLEMENT"),
            ("IMPLEMENT", "VERIFY"),
            ("VERIFY", "AUDIT"),
            ("AUDIT", "ARCHIVE"),
        ):
            with self.subTest(transition=f"{source}->{target}"):
                source_evidence = {**self.records[target], "state": source}
                assert_write_valid(source_evidence, self.schema, self.protocol, f"{source}->{target} source")
                gate = sdd.evaluate_transition(source_evidence, self.protocol, source, target)
                self.assertEqual(gate.result, "ALLOW", gate.reasons)

    def test_regressions_and_no_automatic_audit_fail_repair(self) -> None:
        validation_fail = {
            **self.records["VALIDATION"],
            "validation_result": "FAIL",
            "validated_at": "2026-04-23T10:50:00Z",
            "validation_issues": ["A requirement is ambiguous."],
            "validation_details": "Return to specification.",
            "updated_at": "2026-04-23T10:50:00Z",
        }
        assert_write_valid(validation_fail, self.schema, self.protocol, "VALIDATION FAIL")
        self.assertEqual(
            sdd.evaluate_transition(validation_fail, self.protocol, "VALIDATION", "SPEC").result,
            "ALLOW",
        )

        verification_fail = {
            **self.records["VERIFY"],
            "verification_result": "FAIL",
            "verified_at": "2026-04-23T11:50:00Z",
            "verification_details": "An SDT scenario failed.",
            "updated_at": "2026-04-23T11:50:00Z",
        }
        assert_write_valid(verification_fail, self.schema, self.protocol, "VERIFY FAIL")
        self.assertEqual(
            sdd.evaluate_transition(verification_fail, self.protocol, "VERIFY", "IMPLEMENT").result,
            "ALLOW",
        )

        audit_fail = {**self.records["AUDIT"], "audit_result": "FAIL"}
        archive_gate = sdd.evaluate_transition(audit_fail, self.protocol, "AUDIT", "ARCHIVE")
        self.assertEqual(archive_gate.result, "DENY")
        self.assertEqual({item.code for item in archive_gate.reasons}, {"AUDIT_FAILED"})
        self.assertIsNone(self.protocol["audit_fail_repair"]["automatic_target"])
        self.assertEqual(
            sdd.evaluate_transition(audit_fail, self.protocol, "AUDIT", "IMPLEMENT").result,
            "DENY",
        )

    def test_current_use_policy_semantics(self) -> None:
        assert_current_use_semantics(ROOT)

    def test_current_use_text_mutation_probes_are_rejected(self) -> None:
        probes = (
            (
                "02_policies/REPORT_ENVELOPE_POLICY.md",
                '\nverification_result: PARTIAL\n',
            ),
            (
                "03_operations/pre_sdd/PRE_SDD_RUNTIME.md",
                '\nfeature record PATCH: {"seed_reference": "seed.md"}\n',
            ),
            (
                "01_execution/prompts/migration_auditor.md",
                '\nfeature record requires migration_source\n',
            ),
            (
                "templates/specs.md",
                '\nCurrent spec: artifacts/specs/feat-900.md\n',
            ),
            (
                "02_policies/VALIDATION_BOUNDARIES_POLICY.md",
                '\nfeature record PATCH: {"reopened_at": "now"}\n',
            ),
        )
        for relative, injection in probes:
            with self.subTest(probe=relative):
                original = (ROOT / relative).read_text(encoding="utf-8")
                with self.assertRaises(AssertionError):
                    assert_current_use_semantics(ROOT, {relative: original + injection})

    def test_closed_schema_rejects_private_patch_fields(self) -> None:
        for field in ("seed_reference", "migration_source", "reopened_at"):
            with self.subTest(field=field):
                record = {**canonical_base_record(), field: "private-value"}
                result = sdd.validate_record(record, self.schema, self.protocol, mode="write")
                self.assertFalse(result["valid"])
                self.assertIn("SCHEMA_INVALID", {item.code for item in result["errors"]})
                with self.assertRaises(AssertionError):
                    assert_patch_fields({field: "private-value"}, self.schema, f"{field} probe")

    def test_report_policy_feature_record_projection(self) -> None:
        policy = (ROOT / "02_policies/REPORT_ENVELOPE_POLICY.md").read_text(encoding="utf-8")
        source = {
            **canonical_base_record("VERIFY"),
            "design_path": "docs/sdd/artifacts/design/feat-900-semantic-regression.md",
            "spec_path": "docs/sdd/artifacts/specs/feat-900-semantic-regression.md",
            "validation_result": "PASS",
            "validated_at": "2026-08-01T00:03:00Z",
            "task_path": "docs/sdd/artifacts/tasks/feat-900-semantic-regression.md",
        }
        for marker, target in (("### PASS", "AUDIT"), ("### FAIL", "IMPLEMENT")):
            patch = extract_json_after(policy, marker)
            apply_claimed_transition(
                source,
                patch,
                self.schema,
                self.protocol,
                "VERIFY",
                target,
                f"Report policy {marker}",
            )
        not_executed = normalized_patch(extract_json_after(policy, "### NOT EXECUTED"))
        assert_patch_fields(not_executed, self.schema, "Report NOT EXECUTED projection")
        self.assertEqual(not_executed["state"], "VERIFY")
        self.assertNotIn("verification_result", not_executed)
        self.assertNotIn("verified_at", not_executed)
        assert_write_valid({**source, **not_executed}, self.schema, self.protocol, "Report NOT EXECUTED")

    def test_migration_report_fields_are_explicitly_report_local(self) -> None:
        prompt = (PROMPT_ROOT / "migration_auditor.md").read_text(encoding="utf-8")
        self.assertIn("PARITY REPORT examples only", prompt)
        for marker in (
            "### PARITY_PASS report example",
            "### PARITY_WARN report example",
            "### PARITY_FAIL report example",
        ):
            report = extract_json_after(prompt, marker)
            self.assertNotIn("state", report)
            self.assertIn("migration_result", report)
            self.assertTrue(set(report).isdisjoint(self.schema["properties"]))
        self.assertIn("must never be merged into a Canonical v1 feature record", prompt)

    def test_installed_lifecycle_prompts_are_semantic(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "product"
            target.mkdir()
            done = subprocess.run(
                [sys.executable, str(INSTALLER), "--target", str(target)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(done.returncode, 0, done.stderr)
            installed_prompts = target / "docs/sdd/01_execution/prompts"
            assert_prompt_semantics(read_prompt_texts(installed_prompts), self.schema, self.protocol)
            for name in PROMPT_NAMES:
                self.assertEqual(
                    (PROMPT_ROOT / name).read_bytes(),
                    (installed_prompts / name).read_bytes(),
                )


if __name__ == "__main__":
    unittest.main()
