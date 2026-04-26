# Spec Re-Audit Workflow

> **Status:** Active
> **Date:** 2026-04-04
> **Scope:** Re-audit of specs with native flow + external complement

---

## 1. Purpose

This workflow defines how to re-audit existing specs without:

- blindly rewriting them
- letting external tools govern the flow
- turning review into noise
- leaving the spec in an ambiguous state after contrast

---

## 2. Guiding Principle

Re-audit is a **contrast**, not a surrender.

Correct order:

1. read native spec
2. audit with native criteria
3. optionally contrast with external audit frameworks
4. incorporate only what fits

---

## 3. Workflow

### Step 1. Base Reading

Read:

- spec
- design
- associated tasks
- associated feature record

### Step 2. Internal Structural Audit

Review:

- internal coherence
- inputs/outputs/errors
- edge cases
- dependencies
- consistency with current documental model

### Step 3. External Contrast (optional)

Use external audit tools to:

- find non-obvious gaps
- pressure edge cases
- challenge implicit assumptions
- improve semantic clarity

Do not use them to:

- redefine the pipeline
- impose a new schema
- substitute the source of truth

### Step 4. Finding Triage

Each external finding must be classified as:

- **adopt**
- **adapt**
- **discard**

### Step 5. Controlled Integration

Only integrate improvements that:

- respect the project manifest
- fit with native SDD
- do not break defined external governance

### Step 6. Closure

Document:

- what was found
- what was adopted
- what was discarded
- why

### Step 7. Output Normalization

When the spec is considered closed:

- update the canonical spec state
- align design, tasks, and feature record with the same reality
- mark the audit report as closed or normalized
- clearly separate internal and external findings
- avoid leaving old references as an active source of truth

---

## 4. Recommended Assessment Format

For each re-audited spec:

| Field | Content |
|-------|---------|
| `spec_id` | reviewed feature or spec |
| `audit_round` | round or batch |
| `internal_findings` | native flow findings |
| `external_findings` | external tool findings |
| `adopted` | incorporated improvements |
| `rejected` | discarded improvements |
| `notes` | tensions or decisions |

---

## 5. Role of External Audit

### Correct role

- external auditor
- comparator
- quality pressurer

### Incorrect role

- sovereign co-author of the model
- substitute for `SDD_GUIDE`
- source of truth

---

## 6. Anti-Patterns

- passing the spec to an external tool and accepting everything
- using re-audit to redesign the project every time
- reviewing superficial specs before central primitives
- mixing internal and external findings without triage
- leaving a spec "more or less OK" but without documental closure

---

## 7. Recommended Operational Order

Do re-audit in batches according to:

- `02_policies/SPECS_REAUDIT_PRIORITIZATION_POLICY.md`

Not by random availability or personal preference.

---

## 8. Expected Result

A good re-audit:

- does not force automatic reimplementation of anything
- does improve the quality of the source of truth
- and better prepares the system for future integrations and audits
- leaves an unequivocal final state: open, normalized, or pending explicit decisions
