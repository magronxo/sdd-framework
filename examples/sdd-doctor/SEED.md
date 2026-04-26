# SEED: sdd-doctor — SDD Framework Diagnostic CLI

**Date**: 2026-04-26
**Type**: NEW_FEATURE
**Status**: DRAFT

---

## 1. Concept & Vision

A deterministic CLI tool that validates the structural integrity of any SDD framework project. It answers one question: **"Does this project follow the framework conventions?"** The output is a human-readable report with clear severity levels (PASS/WARN/FAIL/BLOCKED), designed for CI/CD integration and developer self-check.

The tool is **strict by default** — it does not guess or suggest fixes. It reports what it finds.

---

## 2. Problem Statement

SDD framework projects rely on specific directory structures, config files, and artifact conventions. Manually auditing these is error-prone and tedious. Existing validation is ad-hoc.

sdd-doctor automates this audit with:
- Deterministic output (same input → same output)
- Clear severity taxonomy
- CI-friendly exit codes

---

## 3. Project Overview

### Name
`sdd-doctor`

### Type
Go CLI tool (single binary, stdlib-only)

### Core Functionality
Scans a target directory and reports findings about SDD framework compliance across three domains:
1. **Core checks** (RF-01 to RF-08): Config file, required directories, artifact structure
2. **Governance checks** (RF-09 to RF-12): Feature records, validation gates
3. **Envelope checks** (RF-13 to RF-16): Spec format, verification artifacts, audit reports

### Target Users
- Developers validating their own projects
- CI/CD pipelines enforcing framework compliance
- Teams auditing inherited codebases

---

## 4. Decomposition

Three incremental features:

| Feature | Scope | Status |
|---------|-------|--------|
| feat-001 | Core CLI Doctor | Draft |
| feat-002 | Governance Checks | Draft |
| feat-003 | Envelope Checks | Draft |

### Feature 001: Core CLI Doctor
- CLI entrypoint (`sdd-doctor check <path>`)
- Config file detection and parsing
- Core directory structure validation
- Artifact directory structure validation
- Human-readable report output

### Feature 002: Governance Checks
- Feature record validation (schema, required fields)
- Validation gate enforcement (validation_result = PASS required before TASKS)

### Feature 003: Envelope Checks
- Spec format validation (RF-13 to RF-16)
- Verification artifact existence
- Audit report format checks

---

## 5. Constraints

- **Language**: Go 1.25
- **Dependencies**: stdlib only (no external packages)
- **Build**: `go build ./cmd/sdd-doctor` produces single static binary
- **Portability**: Works on Windows, macOS, Linux
- **Output**: Human-readable terminal output only (no JSON, no HTML)
- **Determinism**: Same input always produces same output

---

## 6. Non-Goals

- Auto-fix functionality
- JSON or machine-readable output
- Web UI or TUI
- Remote validation (network calls)
- Config file customization of rules
- Multi-language support (English only for now)

---

## 7. Success Metrics

| Metric | Target |
|--------|--------|
| CLI help works | `sdd-doctor --help` returns usage |
| Valid project | Exit code 0, no FAIL/BLOCKED |
| Missing config | Exit code 1, FAIL finding |
| Unreadable path | Exit code 2, error to stderr |
| Determinism | Same result on repeated runs |

---

## 8. Out of Scope (v1)

- Parallel scanning
- Custom rule configuration
- Fix suggestions
- Machine-readable output
- Non-English localization
- Network-based validation
- IDE integration

---

## 9. Next Step

Author the **DESIGN** artifact for feat-001 following the SDD template.