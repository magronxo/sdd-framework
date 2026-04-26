# Skill: sdd-deep-audit (Auditoria Profunda)

## Descripció
Auditoria exhaustiva de seguretat, arquitectura i consistència global. Per a batches de features o abans de releases.

## Trigger
Manual amb `/audit-deep` o automàtic cada 5 features completades

## Model
GPT-5 (complet, més car, necessari per anàlisi profund)

## Input
```json
{
  "audit_type": "batch",
  "features_audited": ["feat-005", "feat-006", "feat-007", "feat-008", "feat-009"],
  "scope": "fullstack",
  "focus_areas": ["security", "architecture", "consistency"],
  "codebase_stats": {
    "total_files": 45,
    "total_lines": 8500,
    "test_coverage": "78%"
  }
}
```

## Procediment

### 1. Anàlisi de Seguretat (25%)

#### Go Backend
- [ ] `gosec` analisi completa
- [ ] SQL injection vectors
- [ ] Path traversal protections
- [ ] Race conditions (goroutines, channels)
- [ ] Secrets management (cap a text pla)
- [ ] Auth/AuthZ correcte

#### Frontend React
- [ ] XSS protections
- [ ] Input sanitization
- [ ] CORS configuration
- [ ] Token storage security
- [ ] TypeScript strictness i absència d'`any` innecessari
- [ ] Zustand selectors i granuralitat de subscripcions
- [ ] Dockview lifecycle (mount/unmount, tabs, resizing) sense memory leaks
- [ ] Monaco lifecycle (editor disposal, model reuse, readonly/build mode)
- [ ] React Flow performance (nodes/edges, custom nodes, pan/zoom sense jank)
- [ ] react-arborist virtualització i coherència d'identificadors del file tree

#### API/WebSocket
- [ ] Rate limiting
- [ ] JWT validation
- [ ] Payload size limits
- [ ] Error information leakage

### 2. Anàlisi d'Arquitectura (25%)

#### Coherència entre Mòduls
- [ ] Interfaces ben definides
- [ ] No acoblament ocult
- [ ] Dependency injection correcte
- [ ] Single Responsibility Principle
- [ ] Protocol WebSocket coherent entre frontend (`useAgentSocket`) i backend (`/ws`)
- [ ] REST payloads coherents entre FileTree, Editor, Chat i Metrics

#### Flux de Dades
- [ ] Ticket lifecycle correcte
- [ ] State management (Worker Pool vs Kernel)
- [ ] Async/await patterns
- [ ] Error propagation

#### Escalabilitat
- [ ] Bottlenecks identificats
- [ ] Resource leaks (goroutines, file handles)
- [ ] Memory usage patterns

### 3. Consistència Global (25%)

#### Specs vs Implementació
- [ ] Totes les features tenen specs
- [ ] Goals vs Reality match
- [ ] Non-goals respectats

#### Tests
- [ ] Tests existeixen per a tota feature
- [ ] No tests flaky
- [ ] Mock usage correcte
- [ ] Integration tests on pertoca

#### Documentació
- [ ] README actualitzat
- [ ] API documentation
- [ ] ADRs per decisions importants
- [ ] CHANGELOG

### 4. Performance & Fiabilitat (15%)

#### Performance
- [ ] Memory allocations (poc eficients)
- [ ] CPU hotspots
- [ ] Database queries (N+1, missing indexes)
- [ ] Caching strategy

#### Fiabilitat
- [ ] Timeout handling
- [ ] Retry logic
- [ ] Circuit breaker pattern
- [ ] Graceful degradation

### 5. Qualitat de Codi Avançada (10%)

#### Go Idioms
- [ ] Proper error wrapping
- [ ] Context propagation
- [ ] Interface segregation
- [ ] Composition over inheritance

#### Clean Code
- [ ] Function length (< 50 lines)
- [ ] Cyclomatic complexity (< 10)
- [ ] Naming clarity
- [ ] Comments on "why", not "what"

## Output

### Informe
**Fitxer:** `SDD/audit_reports/audit_batch_5_2026-03-29.md`

```markdown
# Deep Audit: Batch #5 (Features 5-9)
**Data:** 2026-03-29  
**Auditor:** sdd-deep-audit (GPT-5)  
**Durada:** ~15 minuts  
**Scope:** 5 features, 45 fitxers, 8500 línies

## Resum Executiu
**Resultat Global:** ⚠️ WARN  
**Score:** 72/100  
**Features Aprovades:** 4/5  
**Issues Crítiques:** 1  
**Issues Altes:** 3  
**Warnings:** 12

## 🚨 Issues Crítiques (Atenció Imediata)

### CRIT-001: Race Condition a Worker Pool
**Fitxer:** `internal/kernel/workerpool.go:175-185`  
**Descripció:** Access concurrent a worker.state sense mutex a checkWorkersHealth()  
**Impacte:** Data race potencial, comportament indefinit  
**Reproducció:** Test de càrrega amb 1000+ tickets  
**Solució:** Afegir wp.mu.RLock() abans de iterar workers  
**Ticket:** CRIT-001-001 (PRIORITAT: CRÍTICA)

## 🔴 Issues Altes (Resoldre Abans de Release)

### HIGH-001: SQL Injection Vector
**Fitxer:** `internal/engram/store.go:45`  
**Descripció:** Query construïda amb fmt.Sprintf() enlloc de prepared statements  
**Impacte:** Vulnerabilitat de seguretat  
**Solució:** Usar ? placeholders + db.Query()  
**Ticket:** HIGH-001-001

### HIGH-002: Memory Leak a WebSocket
**Fitxer:** `internal/api/websocket.go:89`  
**Descripció:** Connexions no es tancades correctament quan client desconnecta  
**Impacte:** Goroutines orfes acumulades  
**Solució:** Defer ws.Close() + timeout  
**Ticket:** HIGH-002-001

### HIGH-003: Inconsistència Spec-Codi
**Feature:** feat-006  
**Descripció:** Spec menciona "rate limiting" però no implementat a l'API  
**Impacte:** Non-goal violat o missing feature  
**Acció:** Actualitzar spec (si és non-goal) o implementar rate limiting  
**Ticket:** HIGH-003-001

## ⚠️ Warnings (Millorar quan sigui possible)

### WARN-001 a WARN-012
[Lista de warnings amb fitxer, línia, descripció breu, prioritat]

## Anàlisi per Feature

| Feature | Estat | Score | Issues | Acció |
|---------|-------|-------|--------|-------|
| feat-005 | ✅ PASS | 85 | 1 warn | Archive |
| feat-006 | ⚠️ WARN | 72 | 1 high, 3 warns | Fix HIGH-003, després archive |
| feat-007 | ✅ PASS | 88 | 2 warns | Archive |
| feat-008 | ✅ PASS | 90 | 0 issues | Archive |
| feat-009 | ❌ FAIL | 45 | 1 crit, 2 highs | NO archive, deep refactor |

## Anàlisi d'Arquitectura

### Punts Forts
- Separació clara Kernel/Departaments
- Worker Pool ben dissenyat (excepte race condition)
- API REST consistent

### Àrees de Millora
- Millorar gestió d'errors entre mòduls
- Afegir més tests d'integració
- Documentar API amb OpenAPI/Swagger

## Recomanacions Estratègiques

1. **Immediat:** Corregir CRIT-001 (race condition)
2. **Abans Release:** Resoldre HIGH-001, HIGH-002, HIGH-003
3. **Deute Tècnic:** Addressar warnings de performance
4. **Proper Batch:** Millorar cobertura de tests (objectiu: 85%)

## Tickets Generats
| ID | Prioritat | Assignat | Descripció |
|----|-----------|----------|------------|
| CRIT-001-001 | 🔴 Crítica | TBD | Fix race condition Worker Pool |
| HIGH-001-001 | 🔴 Alta | TBD | SQL injection fix |
| HIGH-002-001 | 🔴 Alta | TBD | WebSocket memory leak |
| HIGH-003-001 | 🔴 Alta | TBD | Rate limiting o update spec |
| ... | ... | ... | ... |

## Següents Passos
1. [ ] Assignar tickets CRÍTICS i ALTS immediatament
2. [ ] Re-auditar feat-009 després de fixes
3. [ ] Schedule proper deep audit abans de v0.3 release

---
**Auditor:** sdd-deep-audit  
**Model:** GPT-5  
**Context:** Full codebase + specs + tests  
**Metodologia:** Manual review + Static analysis
```

### Dashboard/Metriques
```json
{
  "audit_summary": {
    "batch_id": 5,
    "features_count": 5,
    "global_score": 72,
    "result": "WARN",
    "critical_issues": 1,
    "high_issues": 3,
    "warnings": 12,
    "pass_features": 4,
    "fail_features": 1
  },
  "top_issues": [
    {
      "id": "CRIT-001",
      "severity": "CRITICAL",
      "file": "workerpool.go",
      "description": "Race condition in worker state access"
    }
  ]
}
```

## Criteris de Resultat

| Resultat | Condicions | Acció Requerida |
|----------|-----------|-----------------|
| **PASS** | Score >= 80, 0 issues crítiques/altes | Release aprovada |
| **WARN** | Score 60-79, o 1-3 issues altes | Fix issues altes abans release |
| **FAIL** | Score < 60, o >3 issues altes, o >=1 crítica | NO release, refactor necessari |

## Regles

1. **Bloqueig potencial:** Si >=1 crítica, recomanar NO release
2. **Generar tickets:** Tota issue es converteix en ticket amb prioritat
3. **Informe detallat:** Però estructurat (títol, descripció, solució, ticket)
4. **Temps:** ~15-30 minuts per batch de 5 features
5. **Context ampli:** Necessita accés a tot el codebase, no només la feature

## Comandes

**Manual:**
```
/audit-deep                    # Auditar batch actual (últimes 5 features)
/audit-deep --all             # Auditar tot el codebase
/audit-deep feat-007          # Auditar feature específica a fons
/audit-deep --focus security   # Només seguretat
/audit-deep --focus perf      # Només performance
```

## Exemple d'Ús

```bash
# Després de completar 5 features
$ opencode /audit-deep
🤖 Executant sdd-deep-audit... (pot trigar ~15 minuts)
📊 Analitzant 5 features, 45 fitxers...
🔍 Escanejant seguretat...
🔍 Analitzant arquitectura...
🔍 Revisant consistència...

⚠️  Resultat: WARN (Score: 72/100)
🚨 1 Issue Crítica
🔴 3 Issues Altes  
⚠️ 12 Warnings

📄 Informe complet: SDD/audit_reports/audit_batch_5_2026-03-29.md

🚨 CRÍTIC: Race condition a workerpool.go:175
   Acció immediata requerida!

🎫 Tickets generats: 16 (1 crit, 3 high, 12 warn)
```

---

## Comparativa: sdd-audit vs sdd-deep-audit

| Aspecte | sdd-audit | sdd-deep-audit |
|---------|-----------|----------------|
| **Quan** | Cada feature | Batch (5-10) o manual |
| **Trigger** | Automàtic (post-verify) | Manual o cada 5 features |
| **Model** | GPT-5-mini | GPT-5 |
| **Temps** | < 2 minuts | 15-30 minuts |
| **Abast** | Feature individual | Batch / Global |
| **Focus** | Spec-codi, tests | Seguretat, arquitectura, consistència |
| **Bloqueig** | No | Pot recomanar NO release |
| **Cost** | Baix | Mig |
| **Profunditat** | Lleugera | Exhaustiva |

## Integració al Flux

```
[IMPLEMENT] → [VERIFY] → [sdd-audit] → [ARCHIVE]
                              ↓ (si FAIL o cada 5)
                    [sdd-deep-audit] → [Fixes] → [Re-audit] → [ARCHIVE]
```

---

**Skill ID:** sdd-deep-audit  
**Versió:** 1.0  
**Prioritat:** Mitja-Alta (no default, però crítica abans releases)  
**Cost:** Mig (GPT-5)
