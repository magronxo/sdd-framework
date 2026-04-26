# Retrospective: Phases C and D — Enterprise Policies and Migration Playbook

**Date**: 2026-04-23
**Scope**: 6 new documents (3 policies + 1 template + 1 playbook + 1 skill)
**Reviewer**: Framework self-audit

---

## Summary

Phases C and D bring **enterprise policies**, **strategic planning**, and **migration support**. Quality is high but there are **4 minor-medium issues** to fix.

**Overall verdict**: ✅ **PASS with 4 issues to fix** (all minor or medium, no blockers)

---

## Findings

### 🟡 Issue 1: VALIDATION_BOUNDARIES — Contradictory scope expansion

**Location**: `02_policies/VALIDATION_BOUNDARIES_POLICY.md`, line 79

**Problem**: "Scope expansion" appears as a reopening condition, but in parentheses it says "requires new seed → new feature, not reopening". This is contradictory: either it is a reopening condition or it is not.

**Impact**: Confusion about whether a spec can be reopened to add scope.

**Proposed fix**: Separate into two clear lists:
- "Valid Reopening Conditions" (3 items)
- "What Is NOT Reopening" (scope expansion goes here)

---

### 🟡 Issue 2: MIGRATION_PLAYBOOK — "All new features start as seeds" is imprecise

**Location**: `03_operations/MIGRATION_PLAYBOOK.md`, line 73

**Problem**: It says "All new features start as seeds in `03_operations/pre_sdd/`" but `AGENT_DECISION_TABLE.md` and `DECOMPOSITION_AND_SIZE_POLICY.md` allow "code adjustments" (< 50 lines, ≤ 2 FR) that DO NOT go through Pre-SDD.

**Impact**: A team could force full SDD for trivial changes.

**Proposed fix**: Change to "All new non-trivial features start as seeds. Trivial fixes use the code adjustment path."

---

### 🟡 Issue 3: MIGRATION_PLAYBOOK — No warning about init scripts in existing repos

**Location**: `03_operations/MIGRATION_PLAYBOOK.md`, line 44

**Problem**: It says "Run `init-sdd.ps1` or `init-sdd.sh`" without warning that these scripts could overwrite existing files (e.g. `README.md`, `sdd.config.json`) if the repo already exists.

**Impact**: Accidental loss of existing documentation.

**Proposed fix**: Add note: "Run init scripts with caution on existing repos. Review generated files before committing. Prefer manual creation if the repo already has documentation."

---

### 🟢 Issue 4: ROADMAP_TEMPLATE — "SEED" is not a valid feature state

**Location**: `03_operations/ROADMAP_TEMPLATE.md`, line 47

**Problem**: The "Feature Mapping" table shows `SEED` as a status, but the canonical feature states are: DESIGN, SPEC, VALIDATION, TASKS, IMPLEMENT, VERIFY, AUDIT, ARCHIVE. SEED is pre-SDD.

**Impact**: Confusion between seeds and features.

**Proposed fix**: Change the example to `DESIGN` or `PENDING`, or add a note that seeds do not appear in feature mapping until they are promoted.

---

## Positive Qualities (To Preserve)

1. **EXTERNAL_FRAMEWORK_POLICY.md — "Authority inversion prevention"** is a strong concept well explained with concrete examples (React hooks, ORM, linter).

2. **MIGRATION_PLAYBOOK.md — Common Pitfalls** with "Reality + Fix" is pure gold for adoption. It attacks real objections before they arise.

3. **VALIDATION_BOUNDARIES_POLICY.md — Authority by Artifact Type** with tables per document type is extremely clear. An implementer knows exactly what they can/cannot change and when.

4. **ROADMAP_TEMPLATE.md — Reality Check** with 5 questions and structured output turns the roadmap into a living document, not a static one.

5. **hello-world-skill.md** is exactly what is needed: a minimal example demonstrating contract, surfaces, and errors without complexity.

---

## Recommendations

1. Fix the 4 issues before considering phases C and D closed.

2. Consider adding a link from `GETTING_STARTED.md` to `MIGRATION_PLAYBOOK.md` for users adopting SDD in an existing project (we don't go directly from tutorial to migration).

---

## Correction Checklist

- [x] Issue 1: Separate "Valid Reopening Conditions" from "What Is NOT Reopening" in VALIDATION_BOUNDARIES — ✅ Already properly separated (lines 76-91)
- [x] Issue 2: Clarify "All new non-trivial features start as seeds" in MIGRATION_PLAYBOOK — ✅ Already corrected (line 75)
- [x] Issue 3: Add warning about init scripts in existing repos to MIGRATION_PLAYBOOK — ✅ Already present (line 46)
- [x] Issue 4: Change "SEED" to "PENDING" or add note in ROADMAP_TEMPLATE — ✅ Already uses `PENDING` (line 47)
