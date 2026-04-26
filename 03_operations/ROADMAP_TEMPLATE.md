# Roadmap Template

## Purpose

Plan and track the project's direction at a **macro level**.

This is not a task list. It is a **strategic document** that answers:
- Where are we going?
- What are the major milestones?
- How do we know if the plan is still valid?

---

## Roadmap Structure

### 1. Vision

One sentence describing the desired end state.

> Example: "By Q4 2026, the system supports 10k concurrent users with sub-100ms latency."

### 2. Time Horizons

Divide work into three horizons:

| Horizon | Timeframe | Content | Example |
|---------|-----------|---------|---------|
| **Now** | Current quarter | Committed features in SDD pipeline | "feat-001 to feat-005" |
| **Next** | Next quarter | Prioritized seeds ready for promotion | "Dark mode, API v2" |
| **Later** | Beyond next quarter | Strategic directions, not yet seeded | "Multi-region deployment" |

### 3. Milestones

| Milestone | Target Date | Success Criteria | Dependencies |
|-----------|-------------|------------------|--------------|
| `{M1}` | `{DATE}` | `{CRITERION}` | `{DEPS}` |
| `{M2}` | `{DATE}` | `{CRITERION}` | `{DEPS}` |

### 4. Feature Mapping

Map active and planned features to milestones:

| Feature | Milestone | Status | Owner |
|---------|-----------|--------|-------|
| `feat-001` | M1 | DESIGN | Alice |
| `feat-002` | M1 | SPEC | Bob |
| `feat-003` | M2 | PENDING | TBD |

> Note: `PENDING` means the seed has been promoted to a feature but has not yet entered the SDD pipeline. Seeds that are not yet promoted do not appear in this table.

### 5. Capacity Plan

| Role | Capacity (features/cycle) | Notes |
|------|---------------------------|-------|
| Designers | `{N}` | |
| Specifiers | `{N}` | |
| Implementers | `{N}` | |
| Auditors | `{N}` | |

### 6. Risk Register

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| `{RISK}` | `{high/medium/low}` | `{high/medium/low}` | `{ACTION}` |

---

## Roadmap Reality Check

Every quarter (or after every major milestone), conduct a **Reality Check**:

### Questions

1. **Did we hit the milestone?** If not, why?
2. **Did the features deliver the expected value?** If not, what was missing?
3. **Did our capacity assumptions hold?** If not, adjust.
4. **Did new risks emerge?** Add to the register.
5. **Did the vision change?** Update the roadmap.

### Output

Create a `ROADMAP_REALITY_CHECK_YYYY-MM-DD.md` with:
- What was planned
- What actually happened
- Variance analysis (planned vs actual)
- Updated roadmap (if changes needed)
- Lessons learned

---

## Change Policy

### How to Update the Roadmap

1. Capture the change reason as a seed or ADR
2. Update the relevant sections
3. Record the change in the changelog
4. If the vision changes, require `{DECISION_MAKER_ROLE}` approval

### Changelog

| Date | Change | Reason | Approved By |
|------|--------|--------|-------------|
| `{DATE}` | `{DESCRIPTION}` | `{REASON}` | `{NAME}` |

---

## Related Documents

- `04_project_governance/PROJECT_MANIFEST.md` — vision and constraints
- `03_operations/pre_sdd/PRE_SDD_CONTRACT.md` — seed triage and promotion
- `02_policies/ADR_POLICY.md` — when a roadmap change requires an ADR
- `03_operations/WORKFLOW.md` — how features flow through the pipeline
