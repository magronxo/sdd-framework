# Migration Plan

## Project Info

- **Project name**: `{PROJECT_NAME}`
- **Current methodology**: `{none | ad-hoc | agile | other}`
- **Migration start date**: `{YYYY-MM-DD}`
- **Migration lead**: `{NAME}`
- **Target state**: `SDD is the default for all new features`

---

## Current State Assessment

### Codebase

- **Language(s)**: `{LANGS}`
- **Framework(s)**: `{FRAMEWORKS}`
- **Lines of code (approx)**: `{N}`
- **Test coverage**: `{percentage | unknown}`
- **Existing specs/docs**: `{none | some | extensive}`

### Team

- **Team size**: `{N}`
- **SDD experience**: `{none | some | expert}`
- **Buy-in level**: `{resistant | neutral | enthusiastic}`

### Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| `{RISK_1}` | `{high/medium/low}` | `{ACTION}` |
| `{RISK_2}` | `{high/medium/low}` | `{ACTION}` |

---

## Migration Phases

### Phase 1: Embed (Week 1)

| Task | Owner | Status |
|------|-------|--------|
| Run init script | `{NAME}` | `{pending/done}` |
| Customize `sdd.config.json` | `{NAME}` | `{pending/done}` |
| Fill `PROJECT_MANIFEST.md` | `{NAME}` | `{pending/done}` |
| Fill `GLOSSARY.md` | `{NAME}` | `{pending/done}` |
| Announce migration to team | `{NAME}` | `{pending/done}` |

### Phase 2: Pilot (Weeks 2-4)

| Task | Owner | Status |
|------|-------|--------|
| Select pilot feature | `{NAME}` | `{pending/done}` |
| Create seed → feature | `{NAME}` | `{pending/done}` |
| Run full SDD pipeline | `{NAME}` | `{pending/done}` |
| Document lessons learned | `{NAME}` | `{pending/done}` |

**Pilot feature**: `{feat-XXX-description}`

### Phase 3: Expand (Months 2-3)

| Goal | Target | Status |
|------|--------|--------|
| SDD adoption rate | `50% of new features` | `{pending/in-progress/done}` |
| Triage sessions | `Weekly` | `{pending/in-progress/done}` |
| Team training | `1 session per month` | `{pending/in-progress/done}` |

### Phase 4: Consolidate (Months 4-6)

| Goal | Target | Status |
|------|--------|--------|
| SDD default | `All new features` | `{pending/done}` |
| Legacy boundaries | `Clear` | `{pending/done}` |
| Audit coverage | `All features + critical legacy` | `{pending/done}` |

---

## Rollback Plan

If SDD adoption causes critical blockages:

1. **Pause**: Stop requiring SDD for new features
2. **Preserve**: Keep the SDD infrastructure (docs, templates, config)
3. **Analyze**: Identify why it failed (too heavy? wrong feature? resistance?)
4. **Adjust**: Fix the root cause
5. **Retry**: Re-enter at Phase 2 with a smaller pilot

**Rollback trigger**: `{DEFINE CRITERIA}`

---

## Success Metrics

| Metric | Baseline | Target | Measured At |
|--------|----------|--------|-------------|
| Features completed with SDD | `0%` | `100% (new)` | Monthly |
| Spec validation pass rate | `N/A` | `> 80%` | Per feature |
| Time from seed to ARCHIVE | `N/A` | `{TARGET}` | Per feature |
| Team satisfaction | `{BASELINE}` | `{TARGET}` | Quarterly survey |

---

## Change Log

| Date | Change | Reason |
|------|--------|--------|
| `{DATE}` | `{DESCRIPTION}` | `{REASON}` |

---

## Related Documents

- `03_operations/MIGRATION_PLAYBOOK.md` — full migration guidance
- `02_policies/LEGACY_SPECS_POLICY.md` — handling legacy code
- `04_project_governance/PROJECT_MANIFEST.md` — project constraints
