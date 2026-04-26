# Migration Playbook

> **Mode Diátaxis**: How-To

## Purpose

Guide the adoption of the SDD framework in a project that **already has code**.

This is not a greenfield bootstrap. It is a **migration** from an existing state to a spec-driven state.

---

## When to Use This Playbook

- You have an existing codebase with little or no specs
- You want to introduce SDD without rewriting everything
- You are migrating from another methodology (or no methodology)

---

## Migration Strategy

### Do NOT

- ❌ Stop all development to "write specs first"
- ❌ Rewrite working code to fit SDD
- ❌ Retroactively spec every legacy feature
- ❌ Force SDD on trivial bug fixes

### DO

- ✅ Introduce SDD **gradually** for new features
- ✅ Write specs for **areas under active change**
- ✅ Use `02_policies/LEGACY_SPECS_POLICY.md` to handle old code
- ✅ Embed SDD alongside existing workflows during transition

---

## Phases

### Phase 1: Embed (Week 1)

**Goal**: SDD infrastructure exists in the repo without disrupting current work.

**Steps**:
1. Run `init-sdd.ps1` or `init-sdd.sh` to create the framework structure. ⚠️ **Caution on existing repos**: review generated files before committing. These scripts may create or overwrite `README.md`, `sdd.config.json`, and other root-level files. Prefer manual creation if the repo already has documentation.
2. Customize `sdd.config.json` for your project
3. Fill `04_project_governance/PROJECT_MANIFEST.md` with your project's identity
4. Fill `04_project_governance/GLOSSARY.md` with your terminology
5. Do NOT create feature records yet

**Checkpoint**: `AGENTS.md` and `sdd.config.json` exist. The repo still works as before.

---

### Phase 2: Pilot (Weeks 2-4)

**Goal**: One complete SDD feature demonstrates the pipeline.

**Steps**:
1. Pick a **small, well-understood** upcoming feature (not a refactor)
2. Create a seed, promote it, and run it through the full pipeline
3. Document pain points and fix them
4. Do NOT require other team members to use SDD yet

**Checkpoint**: One feature is ARCHIVED with full artifacts. The team has seen it work.

---

### Phase 3: Expand (Months 2-3)

**Goal**: SDD is the default for new features.

**Steps**:
1. All new non-trivial features start as seeds in `03_operations/pre_sdd/`. Trivial fixes (< 50 lines, ≤ 2 requirements) use the "code adjustment" path (see `00_core/AGENT_DECISION_TABLE.md`).
2. Legacy code changes use SDD only if they are large or complex
3. Trivial fixes (< 50 lines, ≤ 2 requirements) use the "code adjustment" path (see `00_core/AGENT_DECISION_TABLE.md`)
4. Weekly triage sessions review seeds

**Checkpoint**: 50% of new work flows through SDD. Legacy code is untouched.

---

### Phase 4: Consolidate (Months 4-6)

**Goal**: SDD is the standard. Legacy is managed, not ignored.

**Steps**:
1. Critical legacy modules get retroactive specs **only if** they are being refactored
2. Legacy code that is stable and untouched remains legacy (see `LEGACY_SPECS_POLICY.md`)
3. Audit reports cover both new SDD features and legacy risk areas
4. Update `PROJECT_MANIFEST.md` to reflect SDD as the default methodology

**Checkpoint**: SDD is the assumed workflow. Legacy has clear boundaries.

---

## Handling Legacy Code

### Legacy Code = No Spec

Code written before SDD has **no authoritative spec**. This is fine if the code is stable.

### When to Spec Legacy Code

| Situation | Action |
|-----------|--------|
| Bug in legacy code | Fix it; write a spec only if the fix is large |
| Refactor legacy code | Write a spec for the new behavior; old behavior is legacy |
| Feature depends on legacy module | Write an interface spec for the dependency; internal implementation remains legacy |
| Security audit of legacy code | Treat as audit; findings become seeds |

### Legacy Spec Rules

- Legacy specs (if written) are marked `legacy: true` in the feature record
- They are non-authoritative: they describe what the code does, not what it should do
- They cannot be validated against because the implementation already exists

See `02_policies/LEGACY_SPECS_POLICY.md` for details.

---

## Migration Roles

| Role | Responsibility |
|------|---------------|
| **Migration Lead** | Drives the playbook, removes blockers, communicates progress |
| **Pilot Team** | First group to use SDD; provides feedback |
| **Tech Lead** | Approves infrastructure changes, resolves technical conflicts |
| **Product Owner** | Manages seed backlog, ensures triage happens |

---

## Common Pitfalls

### "We don't have time for specs"

**Reality**: You are already writing specs — in code comments, PR descriptions, and Slack threads. SDD just makes them explicit, reviewable, and reusable.

**Fix**: Start with one small feature. Measure if it actually takes longer.

### "Our code is too messy for SDD"

**Reality**: SDD does not require clean code. It requires clear intent. A messy codebase benefits more from specs because they isolate intent from implementation.

**Fix**: Use SDD for the next feature that touches messy code. The spec becomes the boundary.

### "SDD is too heavy for our team size"

**Reality**: SDD scales down. A solo developer can be Designer, Specifier, and Implementer. The pipeline still catches ambiguity and scope creep.

**Fix**: One person wears multiple hats. The gates (VALIDATION, VERIFY) still add value.

---

## Migration Plan Template

Use `templates/migration_plan.md` to document your specific migration.

---

## Related Documents

- `templates/migration_plan.md` — migration plan template
- `02_policies/LEGACY_SPECS_POLICY.md` — legacy spec handling
- `00_core/AGENT_DECISION_TABLE.md` — when agents can bypass full SDD
- `03_operations/pre_sdd/PRE_SDD_CONTRACT.md` — seed intake for new work
- `init-sdd.ps1` / `init-sdd.sh` — bootstrap scripts
