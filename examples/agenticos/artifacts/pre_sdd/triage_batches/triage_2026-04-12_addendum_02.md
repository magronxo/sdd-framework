# PRE-SDD Triage Batch — triage_2026-04-12_addendum_02

date: 2026-04-12  
scope: SEED-04 adoption decision + handoff to SDD  
triage_lead: agentic-os-sdd (post-batch completion of entry_checklist)  

## 1) Context

- Base batch: `00_project_documentation/SDD/artifacts/pre_sdd/triage_batches/triage_2026-04-12.md`
- Since that batch, `SEED-04` has completed its `entry_checklist` (11/11) by converting capabilities to 9 testable GIVEN/WHEN/THEN observable statements.
- Previous addendum (addendum_01) adopted SEED-05 → feat-068.

## 2) Selected (Adopted)

- **SEED-04** — User Shadow / Adversarial Co-Pilot → **Adopted**

## 3) TRIAGE contract (minimal)

- **problem**: El sistema no modela els criteris de decisió de l'usuari; només rep aprovacions puntuals HITL sense capturar patrons de raonament.
- **objective**: Crear un sistema d'ombra observadora que aprengui patrons de decisió sense interferir, i que pugui respondre com a conseller adversarial sota demanda explícita.
- **scope** (candidates to spec — SDD):
  - User Shadow observador en mode ombra (zero side effects)
  - Captura de criteris de decisió implícits com a patrons agregats (no contingut en brut)
  - Conseller adversarial (suggerir alternatives quan es demana explícitament)
  - Relació amb HITL (MAN-03, MAN-04) sense substituir l'aprovació humana
  - Transparència/consentiment: l'usuari ha de poder saber que s'està observant
- **non-scope**:
  - Component de seguretat o substitut de Zero Trust
  - Delegació automatitzada sense HITL explícit
  - Mode "imitar" sense consentiment explícit
  - Anàlisi en temps real de dades sensibles sense anonimització
  - ML training o model fine-tuning
- **impact**:
  - workflow: enriquiment del HITL amb aprenentatge observacional
  - context: patrons de decisió consultables
  - all:tot el sistema si s'integra bé sense drift
- **risks**:
  - Funcionalitat percebuda com a "espionatge" → mitigat amb transparència total
  - Drift cap a substitut de l'operator sense consentiment → mitigat amb no automatitzar sense HITL
  - Model memoritzar decisions sensibles → mitigat amb anonimitzar dades (dimensions, no contingut)
- **success_signal** (9 CAP-* testable statements):
  - CAP-01: Observation without interference (no side effects)
  - CAP-02: Pattern extraction without intrusive inference (abstracted dimensions)
  - CAP-03: Adversarial suggestions only on explicit request
  - CAP-04: No suggestion without request (anti-drift)
  - CAP-05: Pattern persistence across sessions
  - CAP-06: No sensitive data in plain text in pattern store
  - CAP-07: Surface limits respected
  - CAP-08: HITL remains authoritative
  - CAP-09: Consent transparency

## 4) DECOMPOSE

- decision: 1 feature (doc-only MVP)
- proposed feature:
  - `feat-073` — User Shadow MVP Contract (doc-only)
- dependencies/order:
  1. `feat-055` (exists): Action Log — base per registre de decisions HITL
  2. `feat-067` (exists): Approvals Backend — referència HITL existent
  3. `feat-073` (new): User Shadow MVP Contract (doc-only)

## 5) HANDOFF (created paths)

- feature_records_created:
  - `00_project_documentation/SDD/artifacts/features_for_specs/feat-073-user-shadow-mvp-contract-doc-only.json`
- notes:
  - SEED-04 dossier updated to `Adopted` and references this addendum.
  - `pre_sdd_selected_to_handoff.md` updated.
  - PKLot entry updated to `Explored`.

## 6) Post-batch update (2026-04-12)

- SEED-04 entry_checklist completat (11/11).
- Capabilities convertides a 9 testable GIVEN/WHEN/THEN statements (CAP-01 a CAP-09).
- Encoding fix: `替代` → `substitut` al risk del dossier.
- SEED-04 passat a `Explored` al PKLot.
- Handoff a feat-073 (doc-only, sense implementació).
