# Policy: Feature Decomposition and Size Limits

> **Mode Diátaxis**: Reference
> **Estat:** Actiu
> **Data:** 2026-04-23
> **Abast:** Totes les features SDD

---

## 1. Propòsit

Evitar dues patologies extremes:

1. **Features gegants**: Una sola feature que abraça múltiples capacitats, resultant en specs de 500+ línies, tasks interminables, i audits que no acaben mai.
2. **Features microscòpiques**: Cada canvi de línia és una feature nova, generant overhead burocràtic que supera el valor del canvi.

Aquesta política defineix criteris objectius per decidir quan descompondre i quan consolidar.

---

## 2. Límits de Mida

### 2.1 Límit Superior (Decomposition Trigger)

Una feature **HA DE** descompondre's si compleix **qualsevol** d'aquests criteris:

| Mètrica | Límit | Què comptem |
|---------|-------|-------------|
| **Spec lines** | > 300 línies | Tot el fitxer `specs/<feature>.md` |
| **RF count** | > 15 requisits funcionals | RF-01, RF-02, ... |
| **Task count** | > 12 tasques | Totes les T1, T2, ... al `tasks/<feature>.md` |
| **Component count** | > 5 components nous | A la secció "Components" del design |
| **Surface count** | > 3 surfaces actives | browser + os_fs + wiring + network + env_proxy |
| **Implementation files** | > 8 fitxers nous/modificats | Estimació al design |
| **Estimated duration** | > 5 dies de treball continu | Càlcul del Planner |

**Acció:** Si un límit se supera, el Planner ha de proposar la descomposició abans de generar tasks.

### 2.2 Límit Inferi (Consolidation Trigger)

Una feature **NO HA DE** ser independent si compleix **TOTS** aquests criteris:

| Mètrica | Límit | Què comptem |
|---------|-------|-------------|
| **Spec lines** | < 50 línies | Tot el fitxer |
| **RF count** | ≤ 2 requisits | |
| **Task count** | ≤ 2 tasques | |
| **Surface count** | 1 surface (wiring) | |
| **Estimated duration** | < 2 hores | |

**Acció:** Consolidar com a sub-tasca d'una feature més gran, o tractar com a "code adjustment" (veure `AGENT_DECISION_TABLE.md`).

---

## 3. Criteris de Decomposició

Quan una feature supera el límit superior, aplicar aquests criteris per tallar:

### 3.1 Per Capa (Layer)
Separar per capes independents:
- API / Handler (surface: wiring)
- Lògica de negoci / Core (surface: os_fs o cap)
- Persistència / Storage (surface: os_fs)
- Client / UI (surface: browser)

### 3.2 Per Surface
Separar per superfície d'integració:
- Feature A: backend (wiring + os_fs)
- Feature B: frontend (browser)
- Feature C: networking (network)

### 3.3 Per Estat (State Machine)
Separar per estats independents del lifecycle:
- Feature A: Creació i validació
- Feature B: Processament
- Feature C: Arxivat i neteja

### 3.4 Per Actor
Separar per rol que interactua:
- Feature A: Operador humà (HITL)
- Feature B: Sistema automàtic
- Feature C: Auditoria externa

---

## 4. Regles de Descomposició

1. **Dependencies first**: La feature base (que altres necessiten) es fa primer.
2. **No circular deps**: Si A depèn de B i B depèn de A, el tall és incorrecte.
3. **Preserve contract**: Cada sub-feature té la seva pròpia spec completa (no es pot deixar una spec "a mitges").
4. **Shared design**: Les sub-features poden compartir un design doc pare si es crea un `feat-XXX-parent-design.md`.
5. **Sequential IDs**: Les sub-features usen suffixos: `feat-007-a`, `feat-007-b`, o seqüència nova `feat-008`, `feat-009`.

---

## 5. Anti-Patrons

- **Decomposició prematura**: Tallar una feature de 200 línies "per si de cas" → overhead innecessari
- **Decomposició per capes artificials**: Crear "feature API" i "feature core" quan realment són inseparables
- **Consolidació per mandra**: Ajuntar 3 features independents per "estalviar temps" → specs massa grans

---

## 6. Decisió Operativa

Des de 2026-04-23:

- El Planner és responsable de detectar límit de mida i proposar descomposició
- El Designer pot anticipar la descomposició al design doc (secció "Proposed Sub-features")
- El Validator verifica que les sub-features no tenen dependencies circulars
- No es penalitza una feature de 320 línies si té una justificació explícita al design (però requereix aprovació)
