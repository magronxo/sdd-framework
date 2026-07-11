#!/usr/bin/env python3
"""Repository-internal conformance guard for Canonical SDD Model v1."""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

import sdd_install

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "contract/v1/feature-record.schema.json"
PROTOCOL = ROOT / "contract/v1/sdd-protocol.json"
MANIFEST = ROOT / "contract/v1/install-manifest.json"

ALLOWLISTS = {
    "legacy_compatibility_docs": [
        "00_core/SDD_FEATURE_FORMAT.md",
        "00_core/SDD_RUNTIME.md",
        "contract/v1/README.md",
    ],
    "intentional_invalid_fixtures": [
        "tests/fixtures/v1/feature-record-cases.json",
    ],
}

ACTIVE_AUTHORITY_DOCS = (
    "README.md",
    "AGENTS.md",
    "00_core/SDD_RUNTIME.md",
    "00_core/SDD_HANDOFF_CONTRACT.md",
    "01_execution/prompts/verifier.md",
    "02_policies/LEGACY_SPECS_POLICY.md",
)


@dataclass(frozen=True)
class Finding:
    code: str
    path: str
    message: str


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def _json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _statement_fragments(text: str) -> list[str]:
    """Split prose into contextual units without treating a remote negation as global."""
    return [
        part.strip()
        for part in re.split(r"(?<=[.!?])\s+|\n+", text)
        if part.strip()
    ]


def _authority_order_findings() -> list[Finding]:
    path = "AGENTS.md"
    text = _read(path)
    expected = [
        "Validated feature spec for the active feature.",
        "`docs/sdd/contract/v1/feature-record.schema.json`",
        "`docs/sdd/contract/v1/sdd-protocol.json`",
        "`docs/sdd/00_core/SDD_RUNTIME.md`",
        "`docs/sdd/00_core/SDD_HANDOFF_CONTRACT.md`",
    ]
    section = text.split("## Authority Order", 1)
    if len(section) != 2:
        return [Finding("AUTHORITY_ORDER_MISSING", path, "Authority Order section is missing.")]
    found: list[str] = []
    for line in section[1].splitlines():
        match = re.match(r"\s*(\d+)\.\s+(.+?)\s*$", line)
        if match:
            found.append(match.group(2))
            if len(found) == len(expected):
                break
        elif found:
            break
    if found != expected:
        return [
            Finding(
                "AUTHORITY_ORDER_INVALID",
                path,
                f"First authority entries are {found!r}; expected {expected!r}.",
            )
        ]
    return []


def _active_prompt_paths() -> list[Path]:
    prompt_root = ROOT / "01_execution/prompts"
    return sorted(prompt_root.rglob("*.md")) if prompt_root.exists() else []


def _active_prompt_findings() -> list[Finding]:
    findings: list[Finding] = []
    for file in _active_prompt_paths():
        relative = file.relative_to(ROOT).as_posix()
        text = file.read_text(encoding="utf-8")
        if re.search(r"\bPARTIAL\s*(?:→|->)\s*AUDIT\b", text, re.IGNORECASE):
            findings.append(
                Finding(
                    "ACTIVE_PARTIAL_TO_AUDIT",
                    relative,
                    "Active prompt contains PARTIAL -> AUDIT.",
                )
            )
        if re.search(r'["\']verification_result["\']\s*:\s*["\']PARTIAL["\']', text):
            findings.append(
                Finding(
                    "ACTIVE_PARTIAL_OUTPUT",
                    relative,
                    "Active prompt emits verification_result PARTIAL.",
                )
            )
    return findings


def _human_policy_findings(protocol: dict) -> list[Finding]:
    findings: list[Finding] = []
    rule = next(
        (
            item
            for item in protocol.get("transitions", [])
            if (item.get("from"), item.get("to")) == ("TASKS", "IMPLEMENT")
        ),
        None,
    )
    if rule is None:
        return [
            Finding(
                "TASKS_IMPLEMENT_RULE_MISSING",
                "contract/v1/sdd-protocol.json",
                "TASKS -> IMPLEMENT rule is missing.",
            )
        ]
    if any(req.get("type") == "human_approval" for req in rule.get("requirements", [])):
        findings.append(
            Finding(
                "UNIVERSAL_HUMAN_APPROVAL",
                "contract/v1/sdd-protocol.json",
                "TASKS -> IMPLEMENT contains a universal human_approval requirement.",
            )
        )
    policy = protocol.get("human_approval_policy", {})
    if policy.get("core_default") != "not_required" or policy.get("resolution_mode") != "external_input_only":
        findings.append(
            Finding(
                "HUMAN_POLICY_DRIFT",
                "contract/v1/sdd-protocol.json",
                "Human approval is not declared as conditional external input.",
            )
        )
    checkpoint = protocol.get("human_checkpoints", {}).get("TASKS_TO_IMPLEMENT", {})
    if checkpoint.get("default_required") is not False:
        findings.append(
            Finding(
                "UNIVERSAL_HUMAN_CHECKPOINT",
                "contract/v1/sdd-protocol.json",
                "TASKS_TO_IMPLEMENT defaults to required.",
            )
        )
    return findings


def _waiver_scan_paths() -> list[Path]:
    candidates = {
        ROOT / "README.md",
        ROOT / "AGENTS.md",
        ROOT / "contract/v1/README.md",
    }
    for directory in (ROOT / "00_core", ROOT / "02_policies", ROOT / "01_execution/prompts"):
        if directory.exists():
            candidates.update(directory.rglob("*.md"))
    return sorted(path for path in candidates if path.is_file())


def _waiver_statement_authorizes_external_operation(statement: str) -> bool:
    if not re.search(r"\bowner\s+waiver\b|\bwaiver\b", statement, re.IGNORECASE):
        return False
    if not re.search(r"\b(?:merge|release|deploy|push)\b", statement, re.IGNORECASE):
        return False

    verb = r"(?:allow(?:s|ed|ing)?|permit(?:s|ted|ting)?|authori[sz](?:e|es|ed|ing)?|unblock(?:s|ed|ing)?|waive(?:s|d|ing)?)"
    positive = re.compile(rf"\b{verb}\b", re.IGNORECASE)
    if not positive.search(statement):
        return False

    contextual_negative = re.compile(
        rf"\b(?:does\s+not|do\s+not|must\s+not|cannot|can\s+not|never)\s+{verb}\b",
        re.IGNORECASE,
    )
    if contextual_negative.search(statement):
        return False

    safe_scope = re.compile(
        r"\bwaiver\b.*\bappl(?:y|ies)\s+only\s+to\s+`?AUDIT\s*(?:→|->)\s*ARCHIVE`?",
        re.IGNORECASE,
    )
    if safe_scope.search(statement):
        return False

    no_external_effect = re.compile(
        r"\bwaiver\b.*\bhas\s+no\s+effect\s+on\s+external\s+operations\b",
        re.IGNORECASE,
    )
    if no_external_effect.search(statement):
        return False

    return True


def _waiver_findings() -> list[Finding]:
    findings: list[Finding] = []
    for file in _waiver_scan_paths():
        relative = file.relative_to(ROOT).as_posix()
        for statement in _statement_fragments(file.read_text(encoding="utf-8")):
            if _waiver_statement_authorizes_external_operation(statement):
                findings.append(
                    Finding(
                        "WAIVER_EXTERNAL_AUTHORITY",
                        relative,
                        "Owner waiver is presented as authority for an external operation.",
                    )
                )
                break
    return findings


def _install_docs_findings() -> list[Finding]:
    path = "README.md"
    text = _read(path)
    required_tokens = (
        "python tools/sdd_install.py --target",
        "docs/sdd/contract/v1/feature-record.schema.json",
        "docs/sdd/contract/v1/sdd-protocol.json",
        "docs/sdd/tools/sdd_validate.py",
        "requirements-validator.txt",
        "--self-check",
    )
    missing = [token for token in required_tokens if token not in text]
    return (
        [
            Finding(
                "INSTALL_DOCUMENTATION_INCOMPLETE",
                path,
                f"Missing installation documentation tokens: {missing}",
            )
        ]
        if missing
        else []
    )


def _lifecycle_findings(protocol: dict) -> list[Finding]:
    findings: list[Finding] = []
    canonical = protocol["lifecycle"]["persistent_states"]
    state_names = (
        set(canonical)
        | set(protocol["lifecycle"].get("legacy_state_aliases", {}))
        | set(protocol["lifecycle"].get("pre_record_activities", []))
    )
    arrow_line = re.compile(r"(?:[A-Z_]+\s*(?:→|->)\s*){2,}[A-Z_]+")
    for path in ACTIVE_AUTHORITY_DOCS:
        text = _read(path)
        for match in arrow_line.finditer(text):
            tokens = re.findall(r"[A-Z_]+", match.group(0))
            lifecycle_tokens = [token for token in tokens if token in state_names]
            if len(lifecycle_tokens) >= 3 and lifecycle_tokens != canonical:
                findings.append(
                    Finding(
                        "LIFECYCLE_DRIFT",
                        path,
                        f"Normative lifecycle chain differs from protocol: {lifecycle_tokens}",
                    )
                )
    return findings


def _result_and_path_findings() -> list[Finding]:
    findings: list[Finding] = []
    forbidden_results = (
        (
            re.compile(r'["\']verification_result["\']\s*:\s*["\']PASS_WITH_FOLLOWUP["\']'),
            "VERIFICATION_RESULT_DRIFT",
        ),
        (
            re.compile(r'["\']validation_result["\']\s*:\s*["\']PARTIAL["\']'),
            "VALIDATION_RESULT_DRIFT",
        ),
    )
    legacy_path_allow = set(ALLOWLISTS["legacy_compatibility_docs"])
    for path in ACTIVE_AUTHORITY_DOCS:
        text = _read(path)
        for pattern, code in forbidden_results:
            if pattern.search(text):
                findings.append(
                    Finding(
                        code,
                        path,
                        "Document emits a result value assigned to the wrong field.",
                    )
                )
        if path not in legacy_path_allow and re.search(r"(?<!docs/sdd/)artifacts/", text):
            findings.append(
                Finding(
                    "ROOT_PATH_DRIFT",
                    path,
                    "Document contains a root-level artifacts/ path outside an explicit compatibility allowlist.",
                )
            )
    return findings


def _manifest_findings() -> list[Finding]:
    try:
        manifest = sdd_install.load_manifest(MANIFEST, ROOT)
        sdd_install.validate_sources(manifest, ROOT)
    except sdd_install.InstallError as exc:
        return [
            Finding(
                "INSTALL_MANIFEST_INVALID",
                "contract/v1/install-manifest.json",
                str(exc),
            )
        ]
    return []


def check(root: Path = ROOT) -> dict:
    global ROOT, SCHEMA, PROTOCOL, MANIFEST
    previous = (ROOT, SCHEMA, PROTOCOL, MANIFEST)
    ROOT = root.resolve()
    SCHEMA = ROOT / "contract/v1/feature-record.schema.json"
    PROTOCOL = ROOT / "contract/v1/sdd-protocol.json"
    MANIFEST = ROOT / "contract/v1/install-manifest.json"
    try:
        protocol = _json(PROTOCOL)
        findings: list[Finding] = []
        findings.extend(_authority_order_findings())
        findings.extend(_active_prompt_findings())
        findings.extend(_human_policy_findings(protocol))
        findings.extend(_waiver_findings())
        findings.extend(_install_docs_findings())
        findings.extend(_lifecycle_findings(protocol))
        findings.extend(_result_and_path_findings())
        findings.extend(_manifest_findings())
        return {
            "conformant": not findings,
            "findings": [asdict(item) for item in findings],
            "allowlists": ALLOWLISTS,
        }
    finally:
        ROOT, SCHEMA, PROTOCOL, MANIFEST = previous


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = check(args.root)
    if args.format == "json":
        print(json.dumps(result, indent=2, sort_keys=True))
    elif result["conformant"]:
        print("CONFORMANCE: PASS")
    else:
        print("CONFORMANCE: FAIL")
        for finding in result["findings"]:
            print(f"{finding['code']} {finding['path']}: {finding['message']}")
    return 0 if result["conformant"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
