# Audit Strategy

> **Approved:** 2026-03-29
> **Status:** Active
> **Applies to:** All project phases

---

## 1. Fundamental Principle: Separation of Powers

**Core Runtime - EXTERNAL:**
- The critical system core should be audited via external mechanisms
- **Cannot audit itself** (conflict of interest)
- Validation: tests, lint, static analysis (according to project stack)

**Departments/Components - INTERNAL (optional):**
- Teams or departments may have an **internal auditor**
- Can only audit **other components**, never the critical core

---

## 2. Audit Types

### A. External Audit (recommended)

| Skill | When | Model | Scope | Active |
|-------|------|-------|-------|--------|
| **sdd-audit** | Every feature (post-verify) | Fast, economical | Spec ↔ Code, tests, edge cases | Automatic |
| **sdd-deep-audit** | Batch (N features) or manual | Exhaustive | Security, architecture, global consistency | Manual or pre-release |

**Rule:** No external audit **blocks** the flow. It generates tickets, it does not make changes.

### B. Internal Audit (optional)

When the project has a departmental structure:
- Department or internal auditor role
- Audits **only** non-critical code
- Integrates with project memory for traceability
- DOES NOT audit the critical core (this is always external)

---

## 3. SDD Flow with Audit

```
DESIGN → SPEC → VALIDATION → TASKS → IMPLEMENT → VERIFY → [AUDIT] → ARCHIVE
                                              ↑
                                       sdd-audit (lightweight)
```

---

## 4. Audit Criteria

### sdd-audit (Lightweight)

- **Spec-Code Coherence:** Does every FR have an implementation?
- **Tests:** Do they exist and pass?
- **Edge Cases:** Are errors, timeouts, failures covered?
- **Quality:** According to project stack (lint, types, conventions)

### sdd-deep-audit (Deep)

- **Security:** SQL injection, XSS, race conditions, secrets
- **Architecture:** Coupling, scalability, leaks
- **Global Consistency:** Do all specs have an implementation? Are no-goals respected?

---

## 5. Audit Rules

1. **Evidence-first:** If not executed → `NOT EXECUTED`
2. **No blocking:** Audit generates tickets, does not stop the flow
3. **External > Internal:** The critical core is always audited externally
4. **Structured report:** Follow `02_policies/REPORT_ENVELOPE_POLICY.md`

---

## 6. Audit Tools

The project configures its own tools according to stack:

- **Go:** `go vet`, `golangci-lint`, `gosec`, `go test`
- **TypeScript/React:** `tsc`, `eslint`, `jest`, `cypress`
- **Python:** `pylint`, `mypy`, `pytest`, `bandit`
- **Others:** Adapt to the stack declared in `sdd.config.json`

---

## 7. Integration with SDD

Audit is a **mandatory phase** of the pipeline:

```
[VERIFY] → [AUDIT] → [ARCHIVE]
    ↓           ↓
  Tests    Report + Tickets
```

If AUDIT = FAIL:
- Generate tickets
- Decide: deep audit or rework
- Do not mark as ARCHIVE until PASS/WARN

---

**History:** Generic framework version.
