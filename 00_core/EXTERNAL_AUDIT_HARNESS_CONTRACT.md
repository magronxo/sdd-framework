# External Audit Harness Contract

> **Status:** Active
> **Date:** 2026-04-05
> **Scope:** Minimum contract for external audits of SDD specs and artifacts

---

## 1. Purpose

This document defines the minimum contract so that an external audit tool can intervene in the project **without contaminating its own governance** or forcing changes to the runtime.

The rule is simple:

**The external auditor contrasts, pressures, and reports. It does not govern or implement.**

---

## 2. Guiding Principle

The external harness is a **contrast tool** within the external development layer.

Therefore:

- it does not replace the native SDD flow
- it is not a source of truth
- it does not return code as primary output
- it does not touch the system runtime
- it does not merge development memory with runtime memory

---

## 3. Authorized Intervention Points

### 3.1 Primary intervention

The external harness enters at:

- **AUDIT**
- **audit-deep**
- documental re-audits of existing specs

### 3.2 Unauthorized intervention

The external harness does **not** enter at:

- DESIGN as an authority
- SPEC as a base source
- IMPLEMENT as an executor
- VERIFY as a substitute for tests or native verification
- System runtime

---

## 4. Mandatory Inputs

Any external audit must receive only the minimum necessary context.

### 4.1 Fixed context

- Manifest or project description
- External framework integration map (if it exists)
- External tool adoption policy (if it exists)

### 4.2 Context of the audited feature or spec

- `artifacts/design/feat-XXX*.md`
- `artifacts/specs/feat-XXX*.md`

### 4.3 Optional context

- `artifacts/tasks/feat-XXX*.md`
- prior internal audit report
- associated feature record

### 4.4 Minimum context rule

The entire repo should not be injected by default.

**Contract first. Corpus second.**

---

## 5. Mandatory Output

The external auditor must return a **structured report** and nothing else.

### 5.1 Minimum format per finding

Each finding must include:

- `finding`
- `severity`: `COMPLIANT | WARN | FAIL`
- `scope`: `design | spec | tasks | traceability`
- `violated_rule`
- `recommendation`
- `classification`: `adopt | adapt | discard | park`

### 5.2 Location

The result must be saved to:

- `artifacts/audit_reports/`

### 5.3 Recommended naming

- `audit_external_[feature]_[YYYY-MM-DD].md`
- `audit_external_batch_[n]_[YYYY-MM-DD].md`

---

## 6. Hard Harness Limits

### 6.1 Prohibitions

The external auditor cannot:

- return code patches as primary output
- rewrite the spec by its own authority
- redefine the base SDD pipeline
- impose alien taxonomy of prompts or skills
- touch the runtime or force runtime changes
- merge external memory and runtime memory without explicit contract

### 6.2 Semantic restrictions

The external auditor must accept the project's own nomenclature, including:

- native SDD phases
- established naming conventions

It must not "correct" the system to resemble an external framework.

---

## 7. Evaluation Criteria

The external harness must especially pressure:

- edge case gaps
- operational ambiguity
- consistency between design, spec, and tasks
- compatibility with the project manifest
- hardware limits and timeouts (if defined)
- memory, context, and orchestration risks
- absence of documental traceability

It must not spend primary focus on:

- superficial writing style
- unsolicited internal refactors
- external framework preferences

---

## 8. Triage Rule

No external finding enters the system directly.

Every finding must be classified as:

- **adopt**: fits directly
- **adapt**: adds value but needs translation to the native model
- **discard**: conflicts with manifest, SDD, or runtime
- **park**: has potential value but not actionable now

The final classification is always the responsibility of the project's own flow.

---

## 9. Operational Decision

### `COMPLIANT`

- no material findings
- the case can be closed documentally

### `WARN`

- recommended improvements exist
- does not force touching runtime
- can continue if the report is recorded

### `FAIL`

- real conflict with manifest, SDD, or physical limits
- documental correction needed before considering implementation changes

---

## 10. Relationship with the SDD Flow

This contract complements:

- `03_operations/AUDIT_STRATEGY.md` (if it exists)
- `03_operations/SPEC_REAUDIT_WORKFLOW.md`

Correct order:

1. native reading
2. internal audit
3. external contrast
4. triage `adopt / adapt / discard / park`
5. documental closure

**Never in reverse.**

---

## 11. Model Policy

The harness contract must be clear enough for more than one model to follow.

But this does **not** mean assuming that any model:

- will understand the project manifest equally well
- will maintain limits equally well
- or will produce reliable triage without supervision

Therefore:

- stronger models serve to define and calibrate the contract
- cheaper or heterogeneous models serve to test if the contract is robust enough
- no external model becomes authority by itself

---

## 12. Success Criterion

The external harness is well integrated when:

- it detects real gaps without governing the flow
- it produces comparable reports across models or tools
- it does not force touching runtime
- it reinforces external SDD quality
- it allows external contrast without loss of architectural identity

---

## 13. Current Operational Decision

As of 2026-04-05:

- the external harness is authorized only as an audit complement
- its output is always a report, not a patch
- any future integration must be validated against this document before entering the flow
