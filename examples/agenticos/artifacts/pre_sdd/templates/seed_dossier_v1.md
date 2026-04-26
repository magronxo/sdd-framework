# SEED-{NN} — {Title}

> Replace `{NN}` with seed number, `{Title}` with short descriptive title.

---

## Dades de referència (del PKLot)

- **ID:** `SEED-{NN}`
- **Títol:** {Title}
- **Trigger:** {What prompted this seed}
- **Idea:** {The core idea in 1-2 sentences}
- **Impacte potencial:** {`dashboard` / `kernel` / `workflow` / `context` / `all`}
- **Risc de drift:** {`baix` / `mitjà` / `alt`}
- **Horizon:** {`NOW` / `NEXT` / `LATER`}
- **Estat (PRE-SDD):** `Captured` → update as processed
- **Batch ref:** {`triage_YYYY-MM-DD.md` when triaged}
- **Destí probable:** {`feat-XXX` / `ADR` / `Deferred`}

---

## problem

{One-liner: what problem does this seed address?}

## intent

{What outcome do we want? Not a solution — the desired state.}

## scope_in

- {Explicitly in-scope item}
- {Explicitly in-scope item}

## scope_out

- {Explicitly out-of-scope item}
- {Explicitly out-of-scope item}

## capabilities

- {What the feature MUST provide — testable statements}
- {What the feature MUST provide}

## approach

{How we plan to solve it. Brief — not a full spec. Reference external inspirations if any.}

## risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| {Risk description} | {High/Medium/Low} | {How we reduce it} |

## success_signals

- [ ] {Signal 1 — observable, measurable}
- [ ] {Signal 2 — observable, measurable}

## dependencies

- `{feat-XXX}` — {what it provides and why needed}
- `{feat-YYY}` — {what it provides and why needed}
- {Other dependency} — {description}

## exploration_required

**`true` / `false`**

If `true`, explain why:

> {Reason: estimation >2 days / ≥2 technical unknowns / affects invariants/kernel/security}

### Exploration Notes (when required)

**Technical unknowns:**
1. {Unknown 1} — {initial hypothesis}
2. {Unknown 2} — {initial hypothesis}

**Dependency graph:**
```
{Component A} ──requires──> {Component B}
```

## entry_checklist

Before passing to triage, verify ALL:

- [ ] `problem` is clear and non-circular
- [ ] `intent` describes outcome, not solution
- [ ] `scope_in` and `scope_out` are explicit and not empty
- [ ] All `capabilities` are testable (observable outcomes)
- [ ] `approach` references existing patterns/artifacts where possible
- [ ] Risks have severity and mitigation
- [ ] `exploration_required` is set with reason if true
- [ ] All dependencies reference existing artifacts (feat-XXX, ADR-NN, etc.)
- [ ] Entry checklist is complete (all items checked)

---

## triage_notes

{Long-form analysis notes — what was previously in PKLot. This section is the living document that grows over time.}

---

## batch_handoff

| Date | Batch | Decision | Feature Record |
|------|-------|----------|----------------|
| {YYYY-MM-DD} | `{batch-id}` | `Adopted` / `Deferred` / `Discarded` | `{feat-XXX.json}` / `ADR-NNNN.md` / `-` |