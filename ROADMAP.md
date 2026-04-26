# Roadmap: SDD Framework

> **Mode Diátaxis**: Reference
> **Status**: Active (updated 2026-04-26)
> **Format**: Based on `03_operations/ROADMAP_TEMPLATE.md`

---

## Vision

By Q3 2026, the SDD framework is a validated, documented, and optionally publishable spec-driven development system suitable for any software project.

---

## Time Horizons

| Horizon | Timeframe | Content |
|---------|-----------|---------|
| **Now** | April 2026 | Framework base (A+B+C+D) completed, under retrospective review |
| **Next** | May–June 2026 | Practical validation (HF), competitive analysis applied, open-source preparation |
| **Later** | Q3 2026 | Public release, community feedback, iteration to v0.2.0 |

---

## Completed Milestones

| Milestone | Date | Evidence |
|-----------|------|----------|
| M1 — Genericization | 2026-04-23 | `ROADMAP_GENERICIZATION.md` completed (see `artifacts/legacy/`) |
| M2 — Governance Layer | 2026-04-23 | Fase A: `04_project_governance/` + `03_operations/pre_sdd/` created |
| M3 — Onboarding & Visuals | 2026-04-23 | Fase B: `docs/GETTING_STARTED.md`, `SDD_PIPELINE_VISUAL.md`, `PROJECT_TOUR.md` |
| M4 — Enterprise Policies | 2026-04-23 | Fase C: `EXTERNAL_FRAMEWORK_POLICY.md`, `VALIDATION_BOUNDARIES_POLICY.md`, `ROADMAP_TEMPLATE.md` |
| M5 — Migration Support | 2026-04-23 | Fase D: `MIGRATION_PLAYBOOK.md`, `migration_plan.md`, `hello-world-skill.md` |
| M7 — Competitive Analysis Applied | 2026-04-26 | Diátaxis tags applied to 18+ documents, Invariants section added to spec template, competitive analysis published |

---

## Upcoming Milestones

| Milestone | Target Date | Success Criteria | Dependencies |
|-----------|-------------|------------------|--------------|
| M6 — Practical Validation | 2026-05-15 | HF project uses SDD for at least 2 features with full pipeline | User availability |
| M8 — Open-Source Preparation | 2026-06-15 | LICENSE chosen, README professional, CONTRIBUTING.md, CHANGELOG.md | M6 completed |
| M9 — Public Beta | 2026-07-01 | Repo public with `v0.1.0-beta` tag, announcement post | M8 completed |

---

## Feature Mapping

| Feature / Task | Milestone | Status | Owner |
|----------------|-----------|--------|-------|
| Fase A — Project Governance | M2 | ✅ ARCHIVED | Framework team |
| Fase B — Onboarding & Visuals | M3 | ✅ ARCHIVED | Framework team |
| Fase C — Enterprise Policies | M4 | ✅ ARCHIVED | Framework team |
| Fase D — Migration Playbook | M5 | ✅ ARCHIVED | Framework team |
| Retrospectives A + C/D | M2-M5 | ✅ DONE | Framework team |
| Apply Diátaxis + Invariants | M7 | ✅ ARCHIVED | Framework team |
| Resolve retrospective issues (10) | M2-M5 | ✅ DONE | Framework team |
| Full framework translation (EN) | M7 | ✅ DONE | Framework team |
| HF validation | M6 | ⏳ PENDING | User |
| Open-source prep (LICENSE, README, CONTRIBUTING, CHANGELOG) | M8 | 🔄 IN PROGRESS | Framework team |
| Public beta release | M9 | ⏳ PENDING | TBD |

---

## Reserved for Future Evaluation

These ideas are captured but not committed to the roadmap until M6 is complete:

| Idea | Source | Evaluation Trigger |
|------|--------|-------------------|
| Executable SDT bridge (Gherkin → automated tests) | BDD analysis | After HF validation |
| Optional DISCUSSION phase before DESIGN | Rust RFC analysis | If team size > 3 |
| Seed type `process` for methodology changes | Python PEP analysis | When governance changes arise |
| Architecture layer mapping (surfaces → Clean Architecture) | Clean Architecture analysis | When refactoring HF |
| Agent execution loop within IMPLEMENT | ChatGPT analysis | After AgenticOS research |

---

## Risk Register

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| HF validation reveals framework is too heavy for small features | High | Medium | `DECOMPOSITION_AND_SIZE_POLICY.md` + code adjustment path |
| Open-source release attracts no users | Low | High | Focus on solving a real pain (spec drift) vs marketing |
| AgenticOS concepts leak into generic | Medium | Low | Strict `grep` validation on every commit |
| User abandons HF validation | High | Medium | Keep session notes; partial validation is still evidence |

---

## Reality Check Log

| Date | Milestone | Planned | Actual | Variance | Action |
|------|-----------|---------|--------|----------|--------|
| 2026-04-23 | M2-M5 | Complete Fases A-D | ✅ Completed + 2 retrospectives | +20% time (retrospectives) | Retrospectives are worth the time |
| 2026-04-26 | M7 + issues | Apply Diátaxis + fix 10 retrospective issues + translate all docs | ✅ Completed | On track | All framework docs now in English; issues resolved |

---

## Change Log

| Date | Change | Reason |
|------|--------|--------|
| 2026-04-23 | Created from `ROADMAP_TEMPLATE.md` | Replaced completed genericization roadmap |
| 2026-04-23 | Added M7 (Competitive Analysis Applied) | Analysis completed in this session |
| 2026-04-26 | M7 marked complete, M8 in progress, all retrospective issues resolved | Framework translation and issue cleanup completed |

---

## Related Documents

- `artifacts/legacy/ROADMAP_GENERICIZATION.md` — completed genericization roadmap (legacy)
- `03_operations/ROADMAP_TEMPLATE.md` — template for this document
- `04_project_governance/PROJECT_MANIFEST.md` — project vision and constraints
- `docs/COMPETITIVE_ANALYSIS.md` — competitive analysis that informed M7
