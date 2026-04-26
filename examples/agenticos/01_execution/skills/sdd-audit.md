# Skill: sdd-audit (Auditoria Soft)

## Descripció
Auditoria lleugera i ràpida per a cada feature implementada. No bloqueja el flux, genera informe i tickets si hi ha issues.

## Report envelope (obligatori)

Els informes d'audit generats han de seguir `00_project_documentation/SDD/02_policies/REPORT_ENVELOPE_POLICY.md`.

## Trigger
Automàtic després de `verify` (post-implementació) o manual amb `/audit [feature]`

## Model
GPT-5-mini (ràpid, econòmic, suficient per auditories lleugeres)

## Contracte d'Evidència (NO inventar execució)

Aquest skill és **evidence-first**:

- Si una comanda **no s'ha executat**, s'ha d'escriure `NOT EXECUTED` + motiu.
- Si no hi ha evidència d'execució (output de tests/build), **NO** es pot afirmar "Tests passen".
- `COMPLIANT` a nivell de comportament requereix evidència runtime (tests passant o verify report amb comandes+outputs).

Nota operativa d'entorns:
- Si l'entorn és **plan-only** (no pot executar comandes), l'audit ha de marcar el resultat com `PARTIAL`/`WARN` i deixar `next_action: rerun in build/execute`.

## Integration surface gates (obligatori)

Per evitar `PASS` falsos quan el problema està en capes d'integració (browser/FS/wiring/env), l'audit ha de seguir:

- `00_project_documentation/SDD/02_policies/INTEGRATION_SURFACE_POLICY.md`

Regles:

- L'audit ha de declarar quines **surfaces** aplica (`browser`, `os_fs`, `wiring`, `network`, `env_proxy`).
- Si una surface aplica i falta evidència (p. ex. preflight `OPTIONS` per browser, o test de wiring), el veredicte **no pot ser** `PASS`.
- Si l'evidència no és executable en aquest entorn, marcar `PARTIAL/WARN` + `next_action`.

## Input
```json
{
  "feature_id": "feat-007",
  "design_path": "SDD/artifacts/design/feat-007.md",
  "spec_path": "SDD/artifacts/specs/feat-007.md",
  "task_path": "SDD/artifacts/tasks/feat-007.md",
  "implementation_files": [
    "internal/kernel/workerpool.go",
    "internal/kernel/workerpool_test.go"
  ],
  "environment_mode": "execute | plan-only | unknown",
  "verification_report_path": "SDD/audit_reports/verify_feat-007_2026-03-29.md",
  "commands_executed": [
    {
      "cwd": "02_implementation",
      "command": "go test ./internal/kernel -run TestWorkerPool",
      "status": "EXECUTED | NOT EXECUTED",
      "raw_output_excerpt": "..."
    }
  ],
  "sdt_scenarios": [
    "Worker Pool iniciat: 4 workers IDLE",
    "Ticket processat: Worker IDLE → PROCESSING → IDLE",
    ...
  ]
}
```

## Procediment

### 1. Validar Coherència Spec-Codi (30%)
- [ ] Cada goal de la spec té implementació corresponent
- [ ] Cada requirement funcional (RF-XX) està cobert
- [ ] No hi ha funcionalitat no especificada (scope creep)

### 2. Revisar Tests (30%)
- [ ] Tests existeixen per a la feature
- [ ] Tests passen **amb evidència** (output real o verify report amb comandes+resultats)
- [ ] Cobertura: si no hi ha eina de coverage o no s'ha executat, marcar `UNKNOWN` (no inventar)
- [ ] Tests d'integració presents si aplica
- [ ] SDT scenarios coberts per tests (si no hi ha test, marcar `UNTESTED` / `PARTIAL`)

#### Matriu de compliance (obligatòria)
Per cada scenario/requirement clau, marcar un estat i referenciar evidència:
- ✅ `COMPLIANT` — test existeix i ha PASSAT
- ❌ `FAILING` — test existeix però ha FALLAT
- ❌ `UNTESTED` — no hi ha test
- ⚠️ `PARTIAL` — hi ha test però no cobreix completament o no es pot executar en aquest entorn
- ➖ `UNKNOWN` — no hi ha prou evidència

#### Surface Coverage Validation (obligatòria)
L'audit ha de validar que el verify report inclou `## SURFACES` i que cada surface `true` té evidència `OK`:

| Surface | Evidència del Verify | Estat |
|---------|---------------------|-------|
| browser | (ref o MISSING) | OK / MISSING |
| wiring | (ref o MISSING) | OK / MISSING |
| os_fs | (ref o MISSING) | OK / MISSING |
| network | (ref o MISSING) | OK / MISSING |
| env_proxy | (ref o MISSING) | OK / MISSING |

**PASS gate per surfaces:** Si qualsevol surface `true` té evidència `MISSING`, `audit_result` NO pot ser `PASS`. Use `WARN` (amb next_action) o `FAIL` segons severitat.

## Skills enforcement gates (obligatori des de feat-046)

Per fer que el sistema de skills sigui traçable i no “optatiu”, l’audit ha d’enforcejar:

### 1) TASKS ha de declarar Skills
- El document `TASKS` ha de contenir `## Skills` amb una taula `Task | Skills`.
- Si falta la secció: `audit_result` **NO pot** ser `PASS`.
  - Codi: `E_TASKS_SKILLS_SECTION_MISSING`
  - Resultat recomanat: `WARN` (excepte si la feature és explícitament “skills-heavy”, llavors pot ser `FAIL`).

### 2) Skills declarades han d’existir al registry
- Registry canònic: `00_project_documentation/SDD/03_operations/skills/skills_registry.json`
- Si `TASKS` declara qualsevol skill que no existeix al registry:
  - Codi: `E_TASKS_SKILL_UNKNOWN`
  - Resultat recomanat: `FAIL` (traçabilitat trencada).

### 3) VERIFY PASS requereix evidència de Skills Doctor
Quan `TASKS` declara **almenys una** skill (GLOBAL o per-task):
- Ha d’existir evidència d’execució de:
  - `powershell -NoProfile -ExecutionPolicy Bypass -File .\\04_tools\\skills.ps1 doctor check`
- I l’exit code ha de ser `0`.

Si `verification_result = PASS` sense aquesta evidència:
- Codi: `E_VERIFY_DOCTOR_MISSING`
- `audit_result` **NO pot** ser `PASS` (mínim `WARN`; `FAIL` si el canvi és de seguretat o afecta governança).

Si l’evidència existeix però l’exit code no és `0`:
- Codi: `E_VERIFY_DOCTOR_NOT_OK`
- Resultat recomanat: `FAIL`.

### 3. Qualitat de Codi - Go (20%)
- [ ] `go vet` sense errors
- [ ] Convecions Go respectades (naming, errors, context)
- [ ] Mutexos usats correctament (si aplica)
- [ ] Goroutines amb defer/recover (si aplica)
- [ ] No hi ha imports no usats

### 4. Qualitat de Codi - Altres (10%)
- [ ] React: Hooks correctes, no infinite loops, efectes nets
- [ ] TypeScript: tipus clars, sense `any` evitable, unions/guards correctes
- [ ] Zustand: estat mínim, selectors precisos, sense prop drilling artificial
- [ ] Dockview / panells: layout estable, sense acoblaments globals estranys
- [ ] Monaco / editor: mode readonly vs build coherent, carregues asíncrones robustes
- [ ] React Flow: nodes/edges tipats, updates incrementals, sense re-render absurd
- [ ] SQL: Queries amb índexos, injecció segura
- [ ] JSON: Schema valid, camps obligatoris

### 5. Edge Cases Evidents (10%)
- [ ] Error handling present
- [ ] Timeouts configurats (si aplica xarxa)
- [ ] Graceful shutdown (si aplica)
- [ ] Valors per defecte raonables

## Output

### Informe
**Fitxer:** `SDD/audit_reports/audit_feat-007_2026-03-29.md`

```markdown
# Audit: feat-007 (Worker Pool)
**Data:** 2026-03-29  
**Tipus:** Soft  
**Resultat:** ✅ PASS / ⚠️ WARN / ❌ FAIL

## INVOCATIONS
- audit_engine: sdd-audit
- environment_mode: execute | plan-only | unknown

## EVIDENCE
- Files read: (paths)
- Verification evidence: (verify report path if any)

## COMMANDS
- (cwd) command → EXECUTED/NOT EXECUTED (reason) + output excerpt

## Resum
- Score: 92/100
- Issues: 2 warnings, 0 errors
- Tests: (executed? yes/no) + summary with evidence

## Validació Spec-Codi ✅
| Goal | Implementat | Notes |
|------|--------------|-------|
| G-01 | ✅ | Pool de 4 workers |
| G-02 | ✅ | Heartbeat implementat |
| ... | ... | ... |

## Revisió Tests
- Unit tests: 12
- Integration tests: 0
- Coverage: ~85% / UNKNOWN
- SDT coverage: 9/9 scenarios / PARTIAL / UNTESTED

## Qualitat Codi ⚠️
| Check | Estat | Nota |
|-------|-------|------|
| go vet | ✅ | Cap error |
| convencions | ✅ | Correcte |
| mutexos | ⚠️ | Revisar lectura workerpool.go:45 |

## Warnings
1. **W001** (Mitja): Mutex no utilitzat en lectura de mètriques a workerpool.go:45
   - Acció: Afegir sync.RWMutex o documentar per què és segur
   - Ticket: Opcional

## Recomanacions
- Afegir test de càrrega amb 100+ tickets
- Documentar panic threshold (3) a la spec

## Accions Generades
- [ ] Ticket AUD-001: Revisar mutex (opcional)
```

### Resultat
```json
{
  "audit_result": "PASS",
  "score": 92,
  "issues_count": 0,
  "warnings_count": 2,
  "tickets_generated": ["AUD-001"],
  "next_step": "ARCHIVE"
}
```

**Si FAIL:**
```json
{
  "audit_result": "FAIL",
  "score": 45,
  "issues_count": 3,
  "warnings_count": 5,
  "tickets_generated": ["AUD-002", "AUD-003", "AUD-004"],
  "next_step": "DEEP_AUDIT",
  "recommendation": "Executar sdd-deep-audit; no marcar com a 'verified' fins que hi hagi evidència runtime"
}
```

## Criteris de Resultat

| Resultat | Condicions | Acció Següent |
|----------|-----------|---------------|
| **PASS** | Score >= 80, 0 issues crítiques | Archive feature |
| **WARN** | Score 60-79, o 1-2 issues menors | Archive amb notes, deep audit opcional |
| **FAIL** | Score < 60, o >2 issues, o inconsistència spec-codi, o tests failing amb evidència | Deep audit recomanat; generar tickets; **no** afirmar "ready" sense re-verify |

## Regles

1. **NO bloquejar flux**: L'audit no para el pipeline per si sol; produeix evidència, recomanacions i tickets
2. **Generar tickets**: Cada issue es converteix en ticket a `SDD/artifacts/tasks/audit_fixes_[feature].md`
3. **Informe senzill**: Només taula + accions, sense gràfics
4. **Ràpid**: < 2 minuts per feature
5. **Automàtic**: Després de verify, sense intervenció humana

## Comandes Disponibles

**Automàtica:**
- Post-verify → dispara sdd-audit

**Manual:**
```
/audit feat-007
/audit --verbose feat-007
/audit --quick feat-007  # Només checks ràpids
```

## Exemple d'Ús

```bash
# Després d'implementar feat-008
$ opencode /verify feat-008
✅ Verification PASS

$ opencode /audit feat-008
🤖 Executant sdd-audit...
✅ Resultat: PASS (Score: 87/100)
⚠️  1 Warning: Cobertura tests 68% (< 70%)
📄 Informe: SDD/audit_reports/audit_feat-008_2026-03-29.md
🎫 Ticket generat: AUD-005 (millorar cobertura)
📦 Next: Archive feature
```

---

**Skill ID:** sdd-audit  
**Versió:** 1.0  
**Prioritat:** Alta (default per cada feature)  
**Cost:** Baix (GPT-5-mini)
