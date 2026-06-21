# SDD Guide – Spec-Driven Development (Simplified)

> **Diátaxis Mode**: Explanation  
> **Spec-Driven Development** for agent systems.  
> The **spec** is the feature source of truth. Code only implements approved specs.

---

## Canonical Installation Model

SDD is embedded inside a product repository under:

```text
docs/sdd/
```

The product repository owns product code, tests, packaging, and runtime files. SDD owns governance, prompts, templates, configuration, and generated SDD artifacts.

Default generated artifacts live under:

```text
docs/sdd/artifacts/
```

The live SDD config is:

```text
docs/sdd/sdd.config.json
```

---

## Axioms (non-negotiable)

1. **spec_as_source** – No behavior exists without a spec.
2. **no_ambiguity** – Vague terms = invalid spec.
3. **edge_cases_first** – If fallback is not defined, behavior is undefined.
4. **hardware_aware** – Every decision must pass the project resource filter when relevant.
5. **no_direct_mutation** – Never modify code directly; always work through feature documents and specs.
6. **external_dev_first** – Flow, governance, context, and integration problems must be solved outside critical runtime before opening critical changes.

---

## Simplified SDD Pipeline with Audit

Every functionality is represented by a **`SYSTEM_SPEC` feature record** that advances through the following states:

```text
DESIGN → SPEC → VALIDATION → TASKS → IMPLEMENT → VERIFY → AUDIT → ARCHIVE
                              ↑______________↓ (if revision needed)
```

### Implementation: SDT vs TDD

**For deterministic components (Go, C, Rust, etc.):** use **TDD** during implementation.

- Write test → implement minimal code → refactor.
- Tests derive from SDT scenarios defined in the spec.

**For components with LLM behavior:** use **SDT** as final validation.

- Implement according to spec.
- Validate against SDT scenarios manually or automatically.

**Hybrid flow:**

```text
SDD documents → TDD code → SDT validation → Audit → Archive
```

| State | Role | Prompt/Skill | Default Artifact | Description |
|-------|------|--------------|------------------|-------------|
| DESIGN | Designer | `docs/sdd/01_execution/prompts/designer.md` | `docs/sdd/artifacts/design/<feature_id>.md` | Defines WHAT. |
| SPEC | Specifier | `docs/sdd/01_execution/prompts/specifier.md` | `docs/sdd/artifacts/specs/<feature_id>.md` | Defines HOW. |
| VALIDATION | Validator | `docs/sdd/01_execution/prompts/validator.md` | `validation_result` | Validates completeness, determinism, and implementability. |
| TASKS | Planner | `docs/sdd/01_execution/prompts/planner.md` | `docs/sdd/artifacts/tasks/<feature_id>.md` | Generates minimal ordered tasks. |
| IMPLEMENT | Implementer | TDD/SDT | product code + tests | Implements according to spec. |
| VERIFY | Verifier | `docs/sdd/01_execution/prompts/verifier.md` | `verification_result` | Verifies compliance with spec and SDT scenarios. |
| AUDIT | Auditor | `docs/sdd/01_execution/skills/sdd-audit` if configured | `docs/sdd/artifacts/audit_reports/<report>.md` | Reviews coherence, quality, risk, and traceability. |
| ARCHIVE | Archiver / Human | manual or configured role | `feature_archived` | Consolidates and closes feature. |

---

## Audit Skills

### sdd-audit (Lightweight)

- **Trigger:** after VERIFY.
- **Scope:** spec-code coherence, tests, basic quality.
- **Output:** report at `docs/sdd/artifacts/audit_reports/audit_<feature>_<date>.md`.
- **Result:** PASS/WARN/FAIL.
- **Action:** PASS/WARN may proceed to archive; FAIL blocks archive until resolved or waived.

### sdd-deep-audit (Deep)

- **Trigger:** manual or every N features, if configured.
- **Scope:** security, architecture, global consistency.
- **Output:** report at `docs/sdd/artifacts/audit_reports/audit_batch_<n>_<date>.md`.
- **Result:** PASS/WARN/FAIL with generated tickets.
- **Action:** FAIL or CRITICAL blocks final acceptance and SDD-governed release/merge gates unless explicitly waived by the project owner.

---

## External vs Internal Audit

**External audit is recommended** for critical core or high-risk work, because self-audit can hide conflicts of interest.

**Internal audit is acceptable** for departments, documentation, low-risk work, or non-critical project areas.

Rule: critical core audit is external unless the owner explicitly accepts the risk.

---

## SDD Re-audit of Existing Artifacts

When what is reviewed is not a new feature but an existing spec, the flow changes:

1. Read the spec, design, tasks, and feature record.
2. Perform structural audit.
3. Optionally contrast with external audit frameworks.
4. Triage findings as `adopt`, `adapt`, or `discard`.
5. Normalize affected artifacts.
6. Close the case with an unequivocal report.

A re-audit is not a new implementation. If it detects misalignment, documentation and traceability are corrected before touching runtime.

---

## Transition Rules

- No state can be skipped.
- If VALIDATION fails → return to SPEC.
- If VERIFY fails → return to IMPLEMENT.
- If AUDIT fails → corrective work may continue, but archive/final acceptance/release gates are blocked until PASS/WARN or explicit owner waiver.
- No open `[?]` may leave DESIGN.
- If a re-audit opens documental inconsistencies, runtime must not be touched until artifact closure is explicit.

---

## Complete Flow with Example

```text
1. DESIGN:   Create docs/sdd/artifacts/design/feat-010-worker-pool-v2.md
             ↓
2. SPEC:     Specify requirements and SDT scenarios
             ↓
3. VALIDATION: Verify completeness and determinism
             ↓ PASS
4. TASKS:    Create docs/sdd/artifacts/tasks/feat-010-worker-pool-v2.md
             ↓
5. IMPLEMENT: TDD → product code + tests
             ↓
6. VERIFY:   tests + SDT PASS
             ↓
7. AUDIT:    Generate docs/sdd/artifacts/audit_reports/audit_feat-010_2026-03-29.md
             ↓ PASS/WARN
8. ARCHIVE:  Update feature record and trace links
```

---

## Audit Reports

**Location:** `docs/sdd/artifacts/audit_reports/`

**Naming:**

- Soft: `audit_<feature>_<YYYY-MM-DD>.md`
- Deep: `audit_batch_<n>_<YYYY-MM-DD>.md`

**Format:** simple, evidence-first, with issues, recommendations, and generated tickets where needed.

---

## Mandatory Formats

### File Naming (MANDATORY)

All feature markdown documents MUST follow this format:

```text
feat-{NNN}-{short-name}.md
```

Rules:

1. **NNN:** 3-digit number, such as `001`, `002`, `012`.
2. **Short name:** lowercase words separated by hyphens.
3. **Extension:** `.md` for markdown documents.

Valid examples:

```text
feat-001-kernel-core.md
feat-006-api-server.md
feat-007-worker-pool.md
feat-012-kernel-status-api.md
```

Feature record JSON files use:

```text
feat-{NNN}-{short-name}.json
```

Folder mapping:

| Folder | Content | Format |
|--------|---------|--------|
| `docs/sdd/artifacts/design/` | Design documents | `feat-{NNN}-{short-name}.md` |
| `docs/sdd/artifacts/specs/` | Specifications | `feat-{NNN}-{short-name}.md` |
| `docs/sdd/artifacts/tasks/` | Task breakdowns | `feat-{NNN}-{short-name}.md` |
| `docs/sdd/artifacts/features_for_specs/` | Feature records | `feat-{NNN}-{short-name}.json` |

---

## Feature Document Format

Follow the format defined in:

```text
docs/sdd/00_core/SDD_FEATURE_FORMAT.md
```

---

## Step-by-Step Process

1. Create feature record: `docs/sdd/artifacts/features_for_specs/<feature_id>.json` with `state: DESIGN`.
2. Run Designer: create `docs/sdd/artifacts/design/<feature_id>.md`, update state to `SPEC`.
3. Run Specifier: create `docs/sdd/artifacts/specs/<feature_id>.md`, update state to `VALIDATION`.
4. Run Validator:
   - PASS → update state to `TASKS`.
   - FAIL → return to `SPEC` without modifying the spec.
5. Run Planner: create `docs/sdd/artifacts/tasks/<feature_id>.md`, update state to `IMPLEMENT`.
6. Run Implementer: execute tasks with TDD/SDT and implement product code + tests.
7. Run Verifier:
   - PASS → update state to `AUDIT`.
   - FAIL → return to `IMPLEMENT`.
8. Run Auditor: generate report under `docs/sdd/artifacts/audit_reports/`.
9. Archive only if audit is PASS/WARN, or if an explicit owner waiver records why archive is allowed despite FAIL.

---

## SDT (Spec-Driven Testing)

SDT is integrated into the SPEC state. Every spec should define:

1. Happy path.
2. Edge cases.
3. Failure modes.

These scenarios translate into tests or verification checks.

---

## Relationship with Code

- **Spec:** documents expected behavior and constraints.
- **Implementation:** product code that complies with the spec.
- **Tests:** derived from acceptance criteria and SDT scenarios.

Correct order:

1. Write and validate spec.
2. Implement according to spec.
3. Test against acceptance criteria.
4. If behavior is undefined, return to spec rather than guessing in code.

---

## Design Document Update

When a feature reaches ARCHIVE, update design and trace documents as needed so future agents can understand what was actually implemented.

Do not move a feature to ARCHIVE without resolving traceability and audit gates.

---

## Examples

Examples are educational only and never framework authority. If an example conflicts with `00_core/`, `01_execution/`, `02_policies/`, templates, or `docs/sdd/sdd.config.json`, the framework contracts win.

---

**History:** Simplified version to facilitate adoption.  
**Updated:** 2026-06-21 — Canonical `docs/sdd/` installation model.
