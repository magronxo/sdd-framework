# Spec: feat-073 — User Shadow MVP Contract (Doc-Only)

## Overview

| Field | Value |
|-------|-------|
| **Feature ID** | feat-073 |
| **Title** | User Shadow MVP Contract (Doc-Only) |
| **Type** | SYSTEM_SPEC |
| **State** | SPEC |
| **Created** | 2026-04-12 |
| **Implementation** | None (doc-only) |

## Problem Statement

El sistema no té manera de capturar i modelar els criteris de decisió de l'usuari més enllà del HITL directe. L'agent no "aprèn" de l'usuari sinó que només rep aprovacions puntuals sense entendre el raonament subjacent.

## Solution

Contracte mínim per a un sistema d'ombra observadora que aprengui patrons de decisió sense interferir, i que pugui funcionar com a conseller adversarial sota demanda explícita.

---

## Requirements

### REQ-073-1: Què és User Shadow

User Shadow és un sistema observador en modo ombra que:

1. **Observa** decisions HITL sense generar side-effects
2. **Captura** criteris de decisió com a patrons agregats (dimensions, no contingut en brut)
3. **Respon** com a conseller adversarial només quan l'usuari ho demana explícitament
4. **Respecta** els mateixos limits de superfície que qualsevol altre component

User Shadow **NO és**:
- Component de seguretat o substitut de Zero Trust
- Sistema de delegació automatitzada
- Sistema d'imitació sense consentiment
- Sistema de ML training

### REQ-073-2: Contracte de Pattern Capture (Input)

 Quan un HITL approval/denial és registrat a l'ActionLog (feat-055), User Shadow captura (sense alterar res):

```json
{
  "pattern_capture": {
    "decision_type": "approve|deny",
    "decision_velocity": "<30s|30s-5min|>5min",
    "rejection_reason_category": "unauthorized|out_of_scope|risk|other",
    "ticket_type": "string (categoria, no contingut)",
    "decision_hour_bucket": "morning|afternoon|evening|night",
    "pattern_id": "uuid"
  }
}
```

**Constraint**: Cap camp conté contingut de tickets, prompts, o respostes en text brut.

### REQ-073-3: Contracte de Pattern Query (Output — on demand)

 Quan l'usuari demana explícitament "quin patró has après?":

```json
{
  "pattern_response": {
    "pattern_id": "uuid",
    "decision_count": N,
    "decision_velocity_avg": "bucket",
    "rejection_category_distribution": { "category": count },
    "observed_since": "RFC3339"
  }
}
```

**Constraint**: No conté contingut de decisions individuals.

### REQ-073-4: Contracte d'Adversarial Suggestion (Output — on demand)

 Quan l'usuari demana explícitament alternatives o opinions:

```json
{
  "suggestion_response": {
    "suggestion_id": "uuid",
    "pattern_id": "uuid",
    "alternative": "string",
    "confidence": "low|medium|high",
    "based_on": "N decisions observades"
  }
}
```

**Constraint**: Només generat en resposta a petició explícita. No hi ha output sense petició.

### REQ-073-5: Anti-Drift Rules (Contractuals)

| Rule | Description |
|------|-------------|
| Transparency | El sistema ha de poder revelar què observa sota demanda |
| Consent | Configuració o consentiment visible abans d'observar |
| No unsolicited | No suggestions sense petició explícita |
| Abstracted only | Només dimensions agregades, mai contingut en brut |

---

## SDT Scenarios

### SDT-073-01: CAP-01 — Observation without interference

**Given** un HITL approval event està registrat a l'ActionLog  
**When** User Shadow està actiu  
**Then** el patró és capturat sense alterar cap estat del sistema  
**And** l'ActionLog conté exactament les mateixes entrades que abans  

### SDT-073-02: CAP-02 — Pattern extraction without intrusive inference

**Given** un usuari ha completat ≥3 decisions HITL en una sessió  
**When** el sistema extreu criteris de decisió  
**Then** l'output conté dimensions agregades (velocitat, frequència, categories) — no contingut en brut  

### SDT-073-03: CAP-03 — Adversarial suggestion on explicit request

**Given** User Shadow ha observat patrons  
**When** l'usuari demana explícitament "mostra'm alternatives"  
**Then** el sistema retorna almenys una sugerència basada en patrons  
**And** la resposta conté `suggestion_id`, `pattern_id`, `confidence`, `based_on`  

### SDT-073-04: CAP-04 — No suggestion without request

**Given** User Shadow té patrons acumulats  
**When** el sistema opera normalment sense petició explícita de l'usuari  
**Then** no es genera cap output d'adversarial suggestion  
**And** no hi ha events de suggestion fora de context de petició  

### SDT-073-05: CAP-05 — Pattern persistence across sessions

**Given** patrons foren capturats en sessió N  
**When** sessió N+1 comença  
**Then** els mateixos patrons son consultables sense re-observació  
**And** `pattern_id` es manté consistent entre sessions  

### SDT-073-06: CAP-06 — No sensitive data in plain text

**Given** User Shadow ha capturat una decisió involucrant contingut de ticket  
**When** els patrons son persistits  
**Then** no apareix contingut de ticket, prompt, o output d'eina en text brut  
**And** Només dimensions agregades (hash de categoria o label) son persistides  

### SDT-073-07: CAP-07 — Surface limits respected

**Given** el sistema està en mode restringit (READ_ONLY o IT_OP)  
**When** User Shadow intenta observar o registrar patrons  
**Then** respect the same surface limits as any other component  
**And** no hi ha side effects fora de les superfícies permeses  

### SDT-073-08: CAP-08 — HITL remains authoritative

**Given** User Shadow ha observat un patró de decisió  
**When** un usuari fa un HITL approval/denial  
**Then** la decisió HITL preval sobre qualsevol suggerència basada en patrons  
**And** User Shadow no apareix a la cadena d'aprovació  

### SDT-073-09: CAP-09 — Consent transparency

**Given** User Shadow està actiu en una sessió  
**When** l'usuari consulta l'estat del sistema o les capacitats  
**Then** el sistema pot revelar que l'observació està ocurrint i quines dades captura  
**And** no revela contingut en brut de decisions  

---

## Acceptance Criteria

| ID | Criteri |
|----|---------|
| AC-01 | Contracte de Pattern Capture definit amb schema JSON (sense contingut en brut) |
| AC-02 | Contracte de Pattern Query definit amb resposta estructurada |
| AC-03 | Contracte d'Adversarial Suggestion definit amb constraint de petició explícita |
| AC-04 | 4 Anti-Drift rules documentades (Transparency, Consent, No unsolicited, Abstracted only) |
| AC-05 | Out of scope explícit (ML, delegació, imitació, dades sensibles) |
| AC-06 | Dependències amb feat-055, feat-067, feat-019 identificades |
| AC-07 | SDT scenarios COVER-01..CO-09 cobreixen CAP-01..CAP-09 del dossier SEED-04 |

---

## Files

| File | Change |
|------|--------|
| `artifacts/design/feat-073-user-shadow-mvp-contract-doc-only.md` | New |

---

## Out of Scope

- Qualsevol implementació de runtime, kernel o API
- Qualsevol canvi a UI o TUI
- ML training o model fine-tuning
- Mode "imitar" sense consentiment explícit
- Captura de dades sensibles sense anonimització
- Automatització basada en patrons apresos
