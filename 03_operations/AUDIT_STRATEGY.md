# Audit Strategy

> **Aprovat:** 2026-03-29
> **Estat:** Actiu
> **Aplicable a:** Totes les fases del projecte

---

## 1. Principi Fonamental: Separació de Poders

**Core Runtime - EXTERN:**
- El nucli crític del sistema hauria d'auditar-se via mecanismes externs
- **NO pot auditar-se a si mateix** (conflicte d'interessos)
- Validació: tests, lint, anàlisi estàtica (segons stack del projecte)

**Departaments/Components - INTERN (opcional):**
- Equips o departaments poden tenir **auditor intern**
- Només pot auditar **altres components**, mai el nucli crític

---

## 2. Tipus d'Auditories

### A. Auditoria Externa (recomanada)

| Skill | Quan | Model | Abast | Activa |
|-------|------|-------|-------|--------|
| **sdd-audit** | Cada feature (post-verify) | Ràpid, econòmic | Spec ↔ Codi, tests, edge cases | Automàtica |
| **sdd-deep-audit** | Batch (N features) o manual | Exhaustiu | Seguretat, arquitectura, consistència global | Manual o pre-release |

**Regla:** Cap auditoria externa **no bloqueja** el flux. Genera tickets, no fa canvis.

### B. Auditoria Interna (opcional)

Quan el projecte té estructura departamental:
- Departament o rol d'auditor intern
- Audita **només** codi no-crític
- Integració amb memòria del projecte per traçabilitat
- NO audita el nucli crític (això sempre és extern)

---

## 3. Flux SDD amb Auditoria

```
DESIGN → SPEC → VALIDATION → TASKS → IMPLEMENTAR → VERIFY → [AUDIT] → ARCHIVE
                                              ↑
                                       sdd-audit (lleugera)
```

---

## 4. Criteris d'Auditoria

### sdd-audit (Lleugera)

- **Coherència Spec-Codi:** Cada RF té implementació?
- **Tests:** Existeixen i passen?
- **Edge Cases:** Errors, timeouts, fallades coberts?
- **Qualitat:** Segons stack del projecte (lint, types, conventions)

### sdd-deep-audit (Profunda)

- **Seguretat:** SQL injection, XSS, race conditions, secrets
- **Arquitectura:** Acoblament, escalabilitat, leaks
- **Consistència Global:** Totes les specs tenen implementació? No-goals respectats?

---

## 5. Regles d'Auditoria

1. **Evidència-first:** Si no s'ha executat → `NOT EXECUTED`
2. **No bloqueig:** L'audit genera tickets, no atura el flux
3. **Extern > Intern:** El nucli crític sempre audita externament
4. **Report estructurat:** Seguir `02_policies/REPORT_ENVELOPE_POLICY.md`

---

## 6. Eines d'Auditoria

El projecte configura les seves pròpies eines segons stack:

- **Go:** `go vet`, `golangci-lint`, `gosec`, `go test`
- **TypeScript/React:** `tsc`, `eslint`, `jest`, `cypress`
- **Python:** `pylint`, `mypy`, `pytest`, `bandit`
- **Altres:** Adaptar al stack declarat a `sdd.config.json`

---

## 7. Integració amb SDD

L'auditoria és una **fase obligatòria** del pipeline:

```
[VERIFY] → [AUDIT] → [ARCHIVE]
    ↓           ↓
  Tests    Report + Tickets
```

Si AUDIT = FAIL:
- Generar tickets
- Decidir: deep audit o rework
- No marcar com a ARCHIVE fins PASS/WARN

---

**Històric:** Versió genèrica del framework.
