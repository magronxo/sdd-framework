# Design: feat-073 — User Shadow MVP Contract (Doc-Only)

## 1. Context

SEED-04 (User Shadow / Adversarial Co-Pilot) has passed PRE-SDD triage. Entry checklist is 11/11, with 9 testable GIVEN/WHEN/THEN capabilities (CAP-01 to CAP-09) verified.

This is a **doc-only MVP** — no runtime/kernel changes, no UI changes, no implementation.

## 2. Què és User Shadow (i què NO és)

### Què ÉS

- **Observer**: Un component en modo ombra que capturant criteris de decisió de l'usuari a través del HITL sense interferir en el flux operatiu.
- **Shadow** perquè no activa res, no bloqueja res, no recomana res sense que l'ho demanin.
- **Conseller adversarial sota demanda**: Quan l'usuari explícitament pregunta "què faries diferent?" o "mostra'm alternatives", el sistema pot respondre basant-se en els patrons apresos.

### Què NO ÉS

- **No és un component de seguretat**: No substitueix Zero Trust ni Guardian.
- **No és delegació**: No automatitza res sense HITL explícit.
- **No és "imitar"**: No copia estils o decisions sense consentiment explícit.
- **No és ML training**: No genera models ni fine-tunes res.
- **No és observador de dades sensibles**: No captura contingut en brut — només dimensions agregades de comportament.

## 3. Contracte d'Inputs/Outputs

### Input: Decision Pattern Capture

**Trigger**: Quan un HITL approval o denial és registrat a l'ActionLog (feat-055).

**Dades capturades** (abstracted — NO raw content):
- `decision_type`: approve | deny
- `decision_velocity`: temps entre request i decisió (buckets: <30s, 30s-5min, >5min)
- `rejection_reason_category`: categorització del rebuig (no autoritzat, fora scope, risc, etc.) — no el text del rebuig
- `ticket_type`: tipus de ticket involucrat (sense contingut)
- `decision_hour_bucket`: hora del dia (matí|tarda|vespre|nit) — agregat, no timestamp exacte
- `pattern_id`: identificador únic del patró après

**Constraint**: Cap camp conté contingut de tickets, prompts d'usuari, o dades identificables en text brut.

### Output: Adversarial Suggestion (on demand)

**Trigger**: Query explícita de l'usuari demanant alternatives o opinions.

**Resposta**:
```json
{
  "suggestion_id": "uuid",
  "pattern_id": "uuid",
  "alternative": "descripció d'alternativa basada en patrons",
  "confidence": "low|medium|high",
  "based_on": "N decisions observades"
}
```

**Constraint**: Només generat quan l'usuari ho demana explícitament. No hi ha output si no hi ha petició.

### Output: Pattern Query (on demand)

**Trigger**: Query explícita de l'usuari demanant "quin patró has après?".

**Resposta**:
```json
{
  "pattern_id": "uuid",
  "decision_count": N,
  "decision_velocity_avg": "bucket",
  "rejection_category_distribution": { "categoria": count },
  "observed_since": "RFC3339"
}
```

**Constraint**: No conté contingut de decisions individuals.

## 4. Anti-Drift Rules

### ADR-01: Transparencymandatory

El sistema ha de poder revelar que està observant i quines dades capture — sota demanda de l'usuari.

### ADR-02: Consents explicit

Cap captura de patrons sense que l'usuari sàpiga que el sistema observa decisions HITL. Configuració explícita o consentiment visible.

### ADR-03: No unsolicited recommendations

El sistema NO genera suggestions sense una petició explícita de l'usuari. Això és un hard constraint — una implementació que ignori això és un violation del contracte.

### ADR-04: Abstracted dimensions only

Les dades capturades son sempre dimensions agregades, no contingut en brut. No es persistix text de decisions, prompts, o respostes.

## 5. Arquitectura (sense implementació)

```
HITL Approval/Denial → ActionLog (feat-055)
                              │
                              ▼
                    User Shadow (observes only)
                              │
                              ▼
                    Pattern Store (abstracted dimensions only)
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
    Query: "what patterns?"          Query: "suggest alternatives?"
              │                               │
              ▼                               ▼
    Pattern summary response       Adversarial suggestion (on demand)
```

El Pattern Store és un contracte, no una implementació. El schema és el que es documenta.

## 6. Dependències

| Dependency | Rol |
|-----------|-----|
| feat-055 (Action Log MVP) | Font de decisions HITL a observar |
| feat-067 (Approvals Backend MVP) | Referència de HITL existent |
| feat-019 (Ticket Runtime Contract) | Schema mínim de ticket (per categorització) |

## 7. Out of Scope (explícit)

- Qualsevol implementació de runtime o kernel
- Qualsevol canvi a UI o TUI
- ML training o fine-tuning de models
- Mode "imitar" sense consentiment explícit
- Captura de dades sensibles sense anonimització
- Automatització basada en patrons apresos

## 8. Relació amb MAN-03 / MAN-04 (HITL)

User Shadow és **suport** al HITL, no un substitut. HITL (MAN-03, MAN-04) continua sent el mecanisme operatiu d'aprovació/intervenció. User Shadow només ofereix:
1. Transparència sobre patrons de decisió observats
2. Conseller adversarial sota demanda explícita

## 9. Risk Posture

| Risk | Severity | Mitigation |
|------|----------|------------|
| Espionatge percebut | High | Transparènciamandatory + consent explícit |
| Drift cap a substitut de l'operator | High | No automatitzar sense HITL explícit (ADR-03) |
| Memoritzar decisions sensibles | Medium | Abstracted dimensions only (ADR-04) |

## 10. Resultat esperat

- `validation_result`: PASS (spec coherent, capabilities testables)
- `verification_result`: PASS (doc-only — sense codi a verificar)
- `audit_result`: PASS (contract complet i coherent)
- Feature archived com doc-only MVP
