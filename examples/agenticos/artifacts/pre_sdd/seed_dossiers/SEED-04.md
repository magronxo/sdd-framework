# SEED-04 — User Shadow / Adversarial Co-Pilot

> Dossier v1 — migrated from free-form notes

---

## Dades de referència (del PKLot)

- **ID:** `SEED-04`
- **Títol:** User Shadow / Adversarial Co-Pilot
- **Trigger:** Brainstorming sobre autonomia futura, HITL i modelatge del criteri de l'usuari
- **Idea:** Explorar un agent observador que aprengui patrons de decisió i imaginari conceptual de l'usuari. Fase inicial: ombra observadora i conseller adversarial; fases posteriors eventuals: delegació parcial limitada. No plantejar-lo com a component de seguretat ni com a substitut del Zero Trust.
- **Impacte potencial:** `workflow` / `context` / `all`
- **Risc de drift:** `alt`
- **Horizon:** `LATER`
- **Estat (PRE-SDD):** `Captured`
- **Batch ref:** (buit)
- **Destí probable:** `ADR`

---

## problem

El sistema no té manera de capturar i modelar els criteris de decisió de l'usuari més enllà del HITL directe. L'agent no "aprèn" de l'usuari sinó que només rep aprobacions puntuals.

## intent

Crear un sistema d'ombra observadora que aprengui patrons de decisió de l'usuari sense interferir en el flux operatiu, i que pugui funcionar com a conseller adversarial en futures fases.

## scope_in

- Agent observador en mode ombra (no activa res)
- Captura de criteris de decisió implícits
- Conseller adversarial (suggereix alternatives o contradiccions)
- Relació amb el flux HITL existent (MAN-03, MAN-04)

## scope_out

- Component de seguretat o substitut de Zero Trust
- Delegació automatitzada sense HITL
- Mode "imitar" sense consentiment explícit
- Anàlisi en temps real de dades sensibles sense safeguards

## capabilities

The following are **testable observable outcomes** (GIVEN/WHEN/THEN format):

### CAP-01: Observation without interference
- **GIVEN** a HITL approval event is recorded in the ActionLog
- **WHEN** the User Shadow component is active
- **THEN** the decision pattern is captured without altering any system state or tool execution
- **Observable via**: ActionLog unchanged (same entries); no new side effects in kernel or API logs

### CAP-02: Pattern extraction without intrusive inference
- **GIVEN** a user has completed ≥3 HITL decisions in a session
- **WHEN** the system extracts decision criteria patterns
- **THEN** the output contains aggregated behavioral dimensions (e.g., decision velocity, frequency of change, rejection reasons) — not raw decision content
- **Observable via**: Pattern store schema validation; no raw ticket content in output

### CAP-03: Adversarial suggestions only on explicit request
- **GIVEN** the User Shadow has observed user decision patterns
- **WHEN** the user explicitly requests "show me alternatives" or "what would you do differently?"
- **THEN** the system returns at least one adversarial suggestion based on observed patterns
- **Observable via**: Suggestion returned only after explicit user request; no proactive suggestions generated
- **Anti-drift**: If the user does NOT request → no suggestion output

### CAP-04: No suggestion without request
- **GIVEN** the User Shadow has accumulated patterns
- **WHEN** the system is in normal operation with no explicit user request
- **THEN** the adversarial suggestion capability produces zero output or is not invoked
- **Observable via**: No suggestion events logged outside explicit request context

### CAP-05: Pattern persistence across sessions
- **GIVEN** patterns were captured in session N
- **WHEN** session N+1 starts
- **THEN** the same patterns are queryable without re-observation
- **Observable via**: Pattern store returns previously captured patterns; same pattern_id across sessions

### CAP-06: No sensitive data in plain text in pattern store
- **GIVEN** the User Shadow captured a decision involving ticket content or user context
- **WHEN** patterns are persisted to the pattern store
- **THEN** no raw ticket content, user prompts, or tool outputs appear as plain text in the pattern store
- **Observable via**: Pattern store entries contain only abstracted dimensions (string hash or category labels, not raw text)

### CAP-07: Surface limits respected
- **GIVEN** the system is in a restricted surface mode (e.g., READ_ONLY or IT_OP)
- **WHEN** the User Shadow attempts to observe or record patterns
- **THEN** it respects the same surface limits as any other component
- **Observable via**: User Shadow observe/record operations produce no side effects outside allowed surfaces

### CAP-08: HITL remains authoritative
- **GIVEN** the User Shadow has observed a decision pattern
- **WHEN** a user makes a HITL approval/denial
- **THEN** the HITL decision overrides any pattern-based suggestion without the User Shadow blocking or modifying the approval
- **Observable via**: ActionLog records HITL decision as authoritative; User Shadow does not appear in approval chain

### CAP-09: Consent transparency
- **GIVEN** the User Shadow is active in a session
- **WHEN** the user queries session status or system capabilities
- **THEN** the system can disclose that observation is occurring and what data is captured
- **Observable via**: Consent manifest or status endpoint returns observation state without revealing raw content

## approach

Fase inicial: ombra purament observadora sense capacitat d'acció. L'agent captura decisions i les codifica com a patrons observables. NO fa recomanacions actives sense que l'usuari les demani. En fases posteriors, explorar com el conseller adversarial pot informar el sistema HITL sense substituir-lo.

## risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| Funcionalitat percebuda com a "espionatge" | High | Transparència total: l'usuari ha de saber que l'agent observa |
| Drift cap a substitut de l'operator sense consentiment | High | No automatitzar res sense HITL explícit |
| Model memoritzar decisions sensibles | Medium | Anonimitzar dades, no persistir contingut directe |

## success_signals

- [ ] L'agent pot observar i codificar un patró de decisió de l'usuari sense interferir
- [ ] L'usuari pot demanar "quin patró has après de mi?" i obtenir resposta coherent
- [ ] Les recomanacions adversarials no s'activen sense petició explícita
- [ ] Els patrons apresos persisteixen entre sessions sense dades sensibles en text brut

## dependencies

- `MAN-03` — HITL approval per decisions importants (el User Shadow no substitueix HITL)
- `feat-055` — Action Log (per registrar patrons observats)

## exploration_required

**`true`** — reason: ≥2 technical unknowns (com modelar criteris sense ser intrusiu? com anonimitzar patrons?)

### Exploration Notes (when required)

**Technical unknowns:**
1. Com modelar criteris de decisió de l'usuari sense ser intrusiu o crear biaix? — hipòtesi: usar patrons de comportament agregats, no decisions individuals
2. Com anonimitzar aprenentatge sense perdre valor? — hipòtesi:抽象ar a dimensions (velocitat de decisió, tipping points, frequència de canvi), no capturar contingut

**Dependency graph:**
```
User Shadow ──observes──> HITL decisions
     │                      │
     └──→ Pattern Store ←──┘
```

## entry_checklist

Before passing to triage, verify ALL:

- [x] `problem` is clear and non-circular
- [x] `intent` describes outcome, not solution
- [x] `scope_in` and `scope_out` are explicit and not empty
- [x] `capabilities` are testable (observable outcomes)
- [x] `approach` references existing patterns/artifacts where possible
- [x] Risks have severity and mitigation
- [x] `exploration_required` is set with reason if true
- [x] All dependencies reference existing artifacts
- [x] Entry checklist is complete (all 10 items above verified; capabilities converted to 9 testable GIVEN/WHEN/THEN statements)

---

## triage_notes

Aquesta línia podria evolucionar en el futur com a capa d'assessorament del flux `Mans virtuals (HITL)`, especialment en `MAN-03` i `MAN-04`. No implica merge conceptual amb `MAN-*`: el HITL continua sent el mecanisme operatiu d'aprovació/intervenció, mentre que `User Shadow / Adversarial Co-Pilot` seria només suport de criteri, contradicció i aprenentatge observacional. No s'ha de reinterpretar com a component de seguretat ni com a substitut de l'autoritat humana.

---

## batch_handoff

| Date | Batch | Decision | Feature Record |
|------|-------|----------|----------------|
| 2026-04-12 | triage_2026-04-12_addendum_02 | Adopted | feat-073 (doc-only contract) |