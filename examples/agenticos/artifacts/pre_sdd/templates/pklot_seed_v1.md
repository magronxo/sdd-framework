# PKLot Seed Template v1

> Use this template when capturing a new seed in the Parking Lot.
> For detailed analysis (seed needs >10 lines), create a Seed Dossier at `artifacts/pre_sdd/seed_dossiers/SEED-NN.md`.

---

## seed_id

`SEED-{NN}` — next available number

## title

{Short descriptive title (1-5 words)}

## problem

{One-liner: what problem does this seed address?}

## proposed_solution

{Brief proposed approach (1-3 sentences). If detailed analysis is needed, create a Seed Dossier and link from `batch_ref`.}

## scope_in

- {Explicitly in-scope item}
- {Explicitly in-scope item}

## scope_out

- {Explicitly out-of-scope item}
- {Explicitly out-of-scope item}

## success_signals

- [ ] {Signal 1 — observable, measurable}
- [ ] {Signal 2 — observable, measurable}

## unknowns

- {Technical uncertainty 1}
- {Technical uncertainty 2}

## dependencies

- `{feat-XXX}` — {what it provides and why needed}
- {Other dependency} — {description}

## exploration_required

**`true` / `false`**

If `true`, reason: {estimation >2 days / ≥2 technical unknowns / affects invariants/kernel/security}

## entry_checklist

Before passing to triage, verify ALL:

- [ ] `problem` is clear and non-circular
- [ ] `proposed_solution` is brief and non-circular
- [ ] `scope_in` and `scope_out` are explicit and not empty
- [ ] `success_signals` are observable and measurable
- [ ] `unknowns` are listed (if any)
- [ ] `exploration_required` is set with reason if true
- [ ] `dependencies` reference existing artifacts
- [ ] `entry_checklist` is complete (all items checked)

## horizon

{`NOW` / `NEXT` / `LATER`}

## status_pre_sdd

{`Captured` / `Explored` / `Triaged` / `Adopted` / `Deferred`}

## batch_ref

{Link to `seed_dossiers/SEED-NN.md` or `triage_batches/triage_YYYY-MM-DD.md` when applicable}

---

**Regla d'or de les seeds**
- Si encara és inspiració, va al `parking lot`.
- Si ja hi ha decisió arquitectònica, va a `ADR`.
- Si canvia comportament observable, va a `spec` i `tasks`.
- Si només és un apunt d'implementació, queda com a `task`.

**Per anàlisi detallada (més de ~10 línies)**
 quan una seed necessita anàlisi detallada, crear un Seed Dossier v1 a `artifacts/pre_sdd/seed_dossiers/SEED-NN.md` i referenciar-lo des del camp `batch_ref`.