# SDD Guide – Spec-Driven Development (Simplified)

> **Diátaxis Mode**: Explanation  
> **Spec-Driven Development** for agent systems.  
> The **spec** is the single source of truth. Code only implements approved specs.

---

## Axioms (non-negotiable)

1. **spec_as_source** – No behavior exists without a spec.
2. **no_ambiguity** – Vague terms = invalid spec.
3. **edge_cases_first** – If fallback is not defined, behavior is undefined.
4. **hardware_aware** – Every decision must pass the project resource filter.
5. **no_direct_mutation** – Never modify code directly; always through feature documents and specs.
6. **external_dev_first** – Flow, governance, context, and integration problems must be solved outside the core before opening critical changes.

---

## Simplified SDD Pipeline with Audit

Every functionality is represented by a **`SYSTEM_SPEC` document** that advances through the following states:

```
DESIGN → SPEC → VALIDATION → TASKS → IMPLEMENT → VERIFY → AUDIT → ARCHIVE
                              ↑______________↓ (if revision needed)
```

### Implementation: SDT vs TDD

**For deterministic components (Go, C, Rust, etc.):** We use **TDD** (Test-Driven Development) during the implementation phase.
- Write test → Implement minimal code → Refactor
- Tests derive from SDT scenarios defined in the spec

**For components with LLM (non-deterministic):** We use **SDT** (Spec-Driven Testing) as final validation.
- Implement according to spec → Validate against SDT scenarios manually/automatically

**Hybrid flow:**
```
SDD (Documents) → TDD (Code) → SDT Validation (Complete system) → Audit → Archive
```

| State | Role | Prompt/Skill | Artifact | Description |
|-------|------|--------------|----------|-------------|
| **DESIGN** | Designer | `01_execution/prompts/designer.md` | `artifacts/design/<feature_id>.md` | Defines the WHAT: architecture, components, hardware budget. |
| **SPEC** | Specifier | `01_execution/prompts/specifier.md` | `artifacts/specs/<feature_id>.md` | Defines the HOW: inputs, outputs, errors, SDT scenarios, Gherkin. |
| **VALIDATION** | Validator | `01_execution/prompts/validator.md` | `validation_result` | Validates that the spec is complete, deterministic, and unambiguous. |
| **TASKS** | Planner | `01_execution/prompts/planner.md` | `artifacts/tasks/<feature_id>.md` | Generates a minimal, ordered task list from a validated spec. |
| **IMPLEMENT** | Developer | TDD/SDT | Code + Tests | Implements according to spec, tests pass. |
| **VERIFY** | Verifier | `01_execution/prompts/verifier.md` | `verification_result` | Verifies that implementation complies with spec and SDT scenarios. |
| **AUDIT** | Auditor | `01_execution/skills/sdd-audit` (if configured) | `audit_report` | Lightweight audit: spec-code coherence, tests, quality. |
| **ARCHIVE** | Archiver | `N/A (manual)` | `feature_archived` | Documental consolidation and feature closure. |

### Audit Skills

**sdd-audit (Lightweight):**
- **Trigger:** Automatic after VERIFY
- **Model:** Fast, economical (sufficient for light audits)
- **Scope:** Spec-code coherence, tests, basic quality
- **Output:** Report at `artifacts/audit_reports/audit_[feature]_[date].md`
- **Result:** PASS/WARN/FAIL
- **Action:** If FAIL → deep audit; If WARN/PASS → Archive

**sdd-deep-audit (Deep):**
- **Trigger:** Manual (`/audit-deep`) or every N features (configurable)
- **Model:** Exhaustive (necessary for deep analysis)
- **Scope:** Security, architecture, global consistency
- **Output:** Report at `artifacts/audit_reports/audit_batch_[n]_[date].md`
- **Result:** PASS/WARN/FAIL with generated tickets
- **Action:** Can block release if FAIL or CRITICAL

### External vs Internal Audit

**External (recommended):**
- System core is audited via external skills
- Impossible to audit oneself (immutable, conflict of interest)
- More secure, faster, more flexible

**Internal (optional):**
- Teams or departments may have internal auditor
- IDE dashboard allows developing from within
- Autonomous system for departments, NOT for critical core

**Rule:** Critical core audit is always EXTERNAL. Department audit may be INTERNAL.

### SDD Re-audit of Existing Artifacts

When what is reviewed is not a new feature but an existing spec, the flow changes:

1. Read the spec, design, tasks, and feature record
2. Perform internal structural audit
3. Optionally contrast with external audit frameworks
4. Triage findings as `adopt`, `adapt`, or `discard`
5. Normalize affected artifacts
6. Close the case with an unequivocal report

Re-audit priority is governed by:

- `03_operations/SPEC_REAUDIT_WORKFLOW.md`
- `90_transitional/SPEC_REAUDIT_PRIORITY_PLAN.md` (non-canonical priority planning, if still used)

**Rule:** A re-audit is not a new implementation. If it detects misalignment, documentation and traceability are corrected before touching runtime.

### External Frameworks

External frameworks do not replace the SDD framework:

- They are audit complements, external memory, and spec review
- Compatible external environments/harnesses
- Other frameworks: only after explicit mapping

**Rule:** First mapping, then adaptation; never direct fusion.

### Transition Rules

- No state can be skipped.
- If VALIDATION fails → return to SPEC (never patch code directly).
- If AUDIT fails → mandatory deep audit; NO archive until PASS/WARN.
- No open `[?]` may leave DESIGN.
- **Audit does not block but documents:** You can always archive, but with warnings if WARN.
- If a re-audit opens documental inconsistencies, runtime must not be touched until artifact closure is explicit.

### Complete Flow with Example

```
1. DESIGN:   Create feat-010-worker-pool-v2.md
             ↓
2. SPEC:     Specify requirements, SDT scenarios
             ↓
3. VALIDATION: Verify completeness, determinism
             ↓ [APPROVED]
4. IMPLEMENT: TDD → workerpool_v2.go + _test.go
             ↓
5. VERIFY:   go test ./... (12/12 PASS)
             ↓
6. AUDIT:    sdd-audit runs automatically
             Result: WARN (Score: 75, 1 warning)
             Report: audit_feat-010_2026-03-29.md
             Ticket: AUD-007 (improve documentation)
             ↓
7. ARCHIVE:  Sync to specs main, update features_for_specs.
             ↓
```

### Audit Reports

**Location:** `artifacts/audit_reports/`

**Naming:**
- Soft: `audit_[feature]_[YYYY-MM-DD].md`
- Deep: `audit_batch_[n]_[YYYY-MM-DD].md`

**Format:** Simple, no noise. Issues table + recommendations + tickets.

### Commands

```bash
/verify [feature]       # Verify implementation
/audit [feature]        # Manual soft audit
/audit-deep             # Deep batch audit
/audit-report           # Show latest report
```

---

## Mandatory Formats

### File Naming (MANDATORY)

All feature documents MUST follow this format:

```
feat_{sequential}_{descriptive-name}.md
```

**Rules:**
1. **Sequential**: 3-digit number (001, 002, ..., 012, ...)
2. **Descriptive name**: Lowercase words separated by hyphens (`-`)
3. **Extension**: `.md` for all documents

**Valid examples:**
```
feat-001-kernel-core.md
feat-006-api-server.md
feat-006-dashboard-react.md
feat-007-worker-pool.md
feat-012-kernel-status-api.md
```

**Folder mapping:**
| Folder | Content | Format |
|--------|---------|--------|
| `artifacts/design/` | Design documents (WHAT) | `feat-XXX_name.md` |
| `artifacts/specs/` | Specifications (HOW) | `feat-XXX_name.md` |
| `artifacts/tasks/` | Task breakdowns | `feat-XXX_name.md` |
| `artifacts/features_for_specs/` | State JSON | `feat-XXX.json` |

**Renaming:**
- `dashboard-backend.md` → `feat-006-api-server.md` (already done)
- **DO NOT rename** `feat-006.md` (it is the React frontend, differentiated by `backend_` in JSON)

### Design Document (`artifacts/design/<feature_id>.md`)

Follow the `templates/design.md` template and include:

- Motivation and affected components
- Data models (structs or JSON schemas)
- Mermaid flow diagram
- Hardware budget (RAM, CPU, disk) — if applicable to the project
- Open questions `[?]` (must be ZERO to pass to SPEC)

### Functional Specification (`artifacts/specs/<feature_id>.md`)

Follow the `templates/specs.md` template and include:

- Functional requirements (FR) with RFC 2119 keywords (MUST / MAY / MUST NOT)
- Typed inputs and outputs
- Errors (code, message, action)
- SDT Scenarios (happy path, edge cases, failure modes)
- Acceptance criteria in Gherkin (Given/When/Then)
- Dependencies

### Feature Document Format

Follow the format defined in `00_core/SDD_FEATURE_FORMAT.md`.

---

## Step-by-Step Process

1. **Create feature record**: Create `artifacts/features_for_specs/<feature_id>.json` with `state: DESIGN`
2. **Run Designer**: Read `01_execution/prompts/designer.md`, create `artifacts/design/<feature_id>.md`, update to `state: SPEC`
3. **Run Specifier**: Read `01_execution/prompts/specifier.md`, create `artifacts/specs/<feature_id>.md`, update to `state: VALIDATION`
4. **Run Validator**: Read `01_execution/prompts/validator.md`, validate:
   - PASS → update to `state: TASKS`
   - FAIL → return to `state: SPEC` (without modifying the spec)
5. **Run Planner**: Read `01_execution/prompts/planner.md`, create `artifacts/tasks/<feature_id>.md`, update to `state: IMPLEMENT`
6. **Implementer**: Execute `tasks/` with TDD and implement code + tests
7. **Run Verifier**: Read `01_execution/prompts/verifier.md`, run tests + SDT:
   - PASS → `state: AUDIT`
   - FAIL → return to `state: IMPLEMENT`
8. **Run Auditor + Archive**: Generate report at `artifacts/audit_reports/` and close feature to `state: ARCHIVE`

---

## SDT (Spec-Driven Testing)

Integrated into the SPEC state. Every spec must define:

1. **Happy Path**: Normal behavior under ideal conditions
2. **Edge Cases**: Physical limits (disk full, timeout, low memory)
3. **Failure Modes**: How the system recovers from errors

These scenarios translate into integration tests.

---

## Relationship with Code

- **Spec**: Documents WHAT and HOW (source of truth)
- **Implementation**: Code that complies with the spec
- **Tests**: Derived from Gherkin criteria and SDT scenarios

**Correct order:**
1. Write spec (SDD)
2. Implement according to spec
3. Test against acceptance criteria
4. If it fails → fix spec (not code), return to 1

### Re-audit on Existing Code

When implementation already exists and the problem is documental coherence:

1. Do not reimplement by default
2. Reconstruct the truth chain between spec, design, tasks, and feature record
3. Record the closure in the audit report
4. Only then continue with the next spec in the batch

---

## Design Document Update (Mandatory)

**When:** When a feature is marked as ARCHIVE (implementation completed)

**What to update:**
1. **Design document** (`artifacts/design/*.md`): Add "Implementation Status" section with:
   - ✅ Implemented components (with files and tests)
   - ⬜ Pending components (with notes)
   - References to specs and tests
   - Changes from original design (if any)

2. **Project Map** (if it exists): Update:
   - Features section (ARCHIVE/PENDING)
   - Components implemented per feature
   - % completion against design

3. **Other documents** (if needed):
   - Manifest (if there are philosophical changes)
   - Parking lot (if pending features are removed)

**Why:**
- Source of truth must reflect real state
- Future sessions should not have to read all documents
- Maintain design-implementation coherence
- Avoid confusion when returning to the project

**Rule:** DO NOT move a feature to ARCHIVE without updating design documents.

---

**History:** Simplified version (3 roles) to facilitate adoption.  
**Updated:** 2026-04-23 — Generic framework version.
