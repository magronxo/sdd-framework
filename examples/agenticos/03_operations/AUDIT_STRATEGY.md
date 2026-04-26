# Auditoria: Estratègia Externa vs Interna

> **Aprovat:** 2026-03-29  
> **Estat:** Actiu  
> **Aplicable a:** Totes les fases del projecte

---

## 1. Principi Fonamental: Separació de Poders

**Ring 0 (Kernel) - EXTERN:**
- El Kernel (Go) és **immutable** i **determinista**
- **NO pot auditar-se a si mateix** (conflicte d'interessos)
- Auditoria via **skills externes** (OpenCode)
- Validació: `go vet`, `golangci-lint`, `gosec`, tests

**Ring 1+ (Departaments) - INTERN (futur):**
- Departaments poden tenir **auditor intern** (05_auditor)
- Evolucionarà amb el sistema (Fase 2+)
- Només pot auditar **altres departaments**, mai el Kernel

---

## 2. Tipus d'Auditories

### A. Auditoria Externa (Ara)

| Skill | Quan | Model | Abast | Activa |
|-------|------|-------|-------|--------|
| **sdd-audit** | Cada feature (post-verify) | GPT-5-mini | Spec ↔ Codi, tests, edge cases | Automàtica |
| **sdd-deep-audit** | Batch (5-10 features) o manual | GPT-5 | Seguretat, arquitectura, consistència global | Manual o pre-release |

**Regla:** Cap auditoria externa **no bloqueja** el flux. Genera tickets, no fa canvis.

### B. Auditoria Interna (Fase 2+)

Quan Dashboard = "Genesis IDE":
- Departament `05_auditor` (o similar)
- Audita **només** codi de Ring 1+
- Integració amb Engram per traçabilitat
- NO audita el Kernel (això sempre és extern)

---

## 3. Flux SDD amb Auditoria

```
DESIGN → SPEC → VALIDATION → TASKS → IMPLEMENTAR → VERIFY → [AUDIT] → ARCHIVE
                                              ↑
                                       sdd-audit (lleugera)
                                       ↓ si issues
                                       sdd-deep-audit (profunda)
                                       ↓
                                       Tickets generats
```

**Cadència:**
- **Soft audit:** Automàtic després de cada verify
- **Deep audit:** Manual (comanda `/audit-deep`) o automàtic cada 5 features

---

## 4. Informes d'Auditoria

**Ubicació:** `00_project_documentation/SDD/audit_reports/`

**Format:**
```markdown
# Audit Report: [Feature/Batch]
**Data:** YYYY-MM-DD  
**Tipus:** [soft/deep]  
**Estat:** [PASS/WARN/FAIL]

## Resum
- Issues trobades: N
- Crítiques: N
- Warnings: N

## Issues
| ID | Severitat | Fitxer | Descripció | Acció |
|----|-----------|--------|------------|-------|
| AUD-001 | 🔴 Alta | router.go | Race condition potencial | Crear ticket |

## Recomanacions
1. ...
2. ...
```

**Fitxers generats:**
- `audit_[feature]_YYYY-MM-DD.md` - Per feature
- `audit_batch_N_YYYY-MM-DD.md` - Per batch

---

## 5. Comandes

**Automàtiques:**
- `verify` (post-implementació) → dispara `sdd-audit` lleuger

**Manuals:**
- `/audit [feature]` - Auditoria soft d'una feature específica
- `/audit-deep` - Auditoria profunda del batch actual
- `/audit-report` - Mostra últim informe

---

## 6. Coherència amb Disseny

**01_KERNEL.md:**
- §5.1 Worker Pool implementat amb mètriques
- §11 Estat d'Implementació inclou tests

**10_OBSERVABILITY.md:**
- Dashboard mostrarà estat d'auditories
- Logs d'auditoria a `engram/audit/`

**MANIFEST:**
- Ring 0 immutable → Auditoria sempre externa
- Observabilitat radical → Tota auditoria és visible

---

## 7. Següents Passos

1. ✅ Documentar estratègia (aquest fitxer)
2. 🔄 Crear skills: `sdd-audit`, `sdd-deep-audit`
3. 🔄 Integrar al flux SDD (verify → audit → archive)
4. 🔄 Sistema d'informes simple
5. ⏳ Fase 2: Departament auditor intern (05_auditor)

---

**Aprovat per:** AgenticOS Core Team  
**Ref:** ADR-005 (Separació FastAuditor/Guardian), MANIFEST §3 (Immutabilitat)
