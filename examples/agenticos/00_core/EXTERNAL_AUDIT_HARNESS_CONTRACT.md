# External Audit Harness Contract

> **Estat:** Actiu  
> **Data:** 2026-04-05  
> **Abast:** Contracte mínim per a auditories externes de specs i artefactes SDD

---

## 1. Propòsit

Aquest document defineix el contracte mínim perquè una eina externa d'auditoria
(com `gentle-ai` via OpenCode o un altre harness equivalent) pugui intervenir en
AgenticOS **sense contaminar la governança pròpia** ni forçar canvis dins del
Kernel.

La regla és simple:

**L'auditor extern contrasta, pressiona i informa. No governa ni implementa.**

---

## 2. Principi Rector

El harness extern és una **eina de contrast** dins de la capa de
desenvolupament extern del Kernel.

Per tant:

- no substitueix el flux SDD propi
- no és font de veritat
- no retorna codi com a primera sortida
- no toca Ring 0
- no fusiona memòria de desenvolupament amb memòria runtime

---

## 3. Punt d'Intervenció Autoritzat

### 3.1 Intervenció principal

El harness extern entra a:

- **AUDIT**
- **audit-deep**
- re-auditories documentals de specs existents

### 3.2 Intervenció no autoritzada

El harness extern **no** entra a:

- DESIGN com a autoritat
- SPEC com a font base
- IMPLEMENT com a executor
- VERIFY com a substitut de tests o verificació pròpia
- Kernel runtime

---

## 4. Inputs Obligatoris

Qualsevol auditoria externa ha de rebre només el context mínim necessari.

### 4.1 Context fix

- `00_project_documentation/01_MANIFEST.md`
- `00_project_documentation/SDD/FRAMEWORK_INTEGRATION_MAP.md`
- `00_project_documentation/SDD/GENTLE_AI_ADOPTION_POLICY.md`

### 4.2 Context de la feature o spec auditada

- `00_project_documentation/SDD/artifacts/design/feat-XXX*.md`
- `00_project_documentation/SDD/artifacts/specs/feat-XXX*.md` 

### 4.3 Context opcional

- `00_project_documentation/SDD/artifacts/tasks/feat-XXX*.md`
- report d'auditoria interna prèvia
- feature record associat

### 4.4 Regla de mínim context

No s'ha d'injectar el repo sencer per defecte.

**Primer contracte. Després corpus.**

---

## 5. Output ObligatorI

L'auditor extern ha de retornar un **report estructurat** i res més.

### 5.1 Format mínim per finding

Cada troballa ha d'incloure:

- `finding`
- `severity`: `COMPLIANT | WARN | FAIL`
- `scope`: `design | spec | tasks | traceability`
- `violated_rule`
- `recommendation`
- `classification`: `adoptar | adaptar | descartar | aparcar`

### 5.2 Ubicació

El resultat s'ha de desar a:

- `00_project_documentation/SDD/audit_reports/`

### 5.3 Nomenclatura recomanada

- `audit_external_[feature]_[YYYY-MM-DD].md`
- `audit_external_batch_[n]_[YYYY-MM-DD].md`

---

## 6. Límits Durs del Harness

### 6.1 Prohibicions

L'auditor extern no pot:

- retornar pegats de codi com a output principal
- reescriure la spec per autoritat pròpia
- redefinir el pipeline SDD base
- imposar taxonomia aliena de prompts o skills
- tocar el Kernel o forçar canvis de runtime
- unir `engram` extern i `engram` runtime

### 6.2 Restriccions semàntiques

L'auditor extern ha d'acceptar la nomenclatura pròpia d'AgenticOS, incloent:

- `Engram Runtime`
- `Worker`
- `Router`
- `.ticket.json`
- fases SDD pròpies

No ha de "corregir" el sistema perquè s'assembli a un framework extern.

---

## 7. Criteris d'Avaluació

El harness extern ha de pressiónar especialment:

- buits d'edge cases
- ambigüitat operativa
- consistència entre design, spec i tasks
- compatibilitat amb el Manifest
- límits hardware i timeouts
- riscos de memòria, context i orquestració
- absència de traçabilitat documental

No ha de gastar el focus principal en:

- estil de redacció superficial
- refactors interns no demanats
- preferències de framework extern

---

## 8. Regla de Triatge

Cap finding extern entra directament al sistema.

Tot finding s'ha de classificar com:

- **adoptar**: encaixa directament
- **adaptar**: aporta valor però necessita traducció al model AgenticOS
- **descartar**: conflicte amb el Manifest, l'SDD o el runtime
- **aparcar**: té valor potencial però no toca ara

La classificació final sempre és responsabilitat del flux propi d'AgenticOS.

---

## 9. Decisió Operativa

### `COMPLIANT`

- no hi ha troballes materials
- el cas pot tancar-se documentalment

### `WARN`

- hi ha millores recomanades
- no obliga a tocar runtime
- es pot continuar si el report queda registrat

### `FAIL`

- hi ha conflicte real amb Manifest, SDD o límits físics
- cal correcció documental abans de considerar canvis d'implementació

---

## 10. Relació amb el Flux SDD

Aquest contracte complementa:

- `AUDIT_STRATEGY.md`
- `SPEC_REAUDIT_WORKFLOW.md`
- `FRAMEWORK_INTEGRATION_MAP.md`

Ordre correcte:

1. lectura pròpia
2. auditoria interna
3. contrast extern
4. triatge `adoptar / adaptar / descartar / aparcar`
5. tancament documental

**Mai al revés.**

---

## 11. Política de Models

El contracte del harness ha de ser prou clar perquè el pugui seguir més d'un model.

Però això **no** vol dir assumir que qualsevol model:

- entendrà igual de bé el Manifest
- mantindrà igual de bé els límits
- o produirà triatge fiable sense supervisió

Per tant:

- models més forts serveixen per definir i calibrar el contracte
- models més barats o heterogenis serveixen per provar si el contracte és prou robust
- cap model extern passa a ser autoritat per si sol

---

## 12. Criteri d'Èxit

El harness extern està ben integrat quan:

- detecta buits reals sense governar el flux
- produeix reports comparables entre models o eines
- no obliga a tocar Ring 0
- reforça la qualitat del SDD extern
- permet contrast extern sense pèrdua d'identitat arquitectònica

---

## 13. Decisió Operativa Actual

Des de 2026-04-05:

- el harness extern s'autoritza només com a complement d'auditoria
- la seva sortida és sempre un report, no un patch
- `gentle-ai` és un cas vàlid d'aquest contracte, no el seu propietari
- qualsevol integració futura s'ha de validar contra aquest document abans d'entrar al flux
