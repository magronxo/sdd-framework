# Spec Re-Audit Workflow

> **Estat:** Actiu  
> **Data:** 2026-04-04  
> **Abast:** Re-auditoria de specs amb flux propi + complement extern

---

## 1. Propòsit

Aquest workflow defineix com re-auditar specs existents sense:

- reescriure-les a cegues
- deixar que `gentle-ai` governi el flux
- convertir la revisió en soroll
- deixar la spec en un estat ambigu després del contrast

---

## 2. Principi Rector

La re-auditoria és un **contrast**, no una rendició.

Ordre correcte:

1. llegir spec pròpia
2. auditar amb criteri AgenticOS
3. opcionalment contrastar amb `gentle-ai`
4. incorporar només allò que encaixi

---

## 3. Workflow

### Pas 1. Lectura base

Llegir:

- spec
- design
- tasks associades
- feature record associat

### Pas 2. Auditoria interna estructural

Revisar:

- coherència interna
- inputs/outputs/errors
- edge cases
- dependències
- consistència amb el model documental actual

### Pas 3. Contraste extern amb `gentle-ai`

Fer servir `gentle-ai` per:

- buscar buits no obvis
- pressionar edge cases
- desafiar assumpcions implícites
- millorar claredat semàntica

No fer-lo servir per:

- redefinir el pipeline
- imposar un nou esquema
- substituir la font de veritat

### Pas 4. Triatge de troballes

Cada finding extern s'ha de classificar com:

- **adoptar**
- **adaptar**
- **descartar**

### Pas 5. Integració controlada

Només integrar millores que:

- respectin el Manifest
- encaixin amb l'SDD propi
- no trenquin la governança externa definida

### Pas 6. Tancament

Documentar:

- què s'ha trobat
- què s'ha adoptat
- què s'ha descartat
- per què

### Pas 7. Normalització de sortida

Quan la spec es considera tancada:

- actualitzar l'estat canònic de la spec
- alinear design, tasks i feature record amb la mateixa realitat
- marcar el report d'auditoria com a tancat o normalitzat
- separar clarament findings interns i externs
- evitar deixar referències antigues com a font de veritat activa

---

## 4. Format d'Avaluació Recomanat

Per cada spec re-auditada:

| Camp | Contingut |
|------|-----------|
| `spec_id` | feature o spec revisada |
| `audit_round` | ronda o lot |
| `internal_findings` | troballes del flux propi |
| `external_findings` | troballes de `gentle-ai` |
| `adopted` | millores incorporades |
| `rejected` | millores descartades |
| `notes` | tensions o decisions |

---

## 5. Paper de `gentle-ai`

### Rol correcte

- auditor extern
- comparador
- pressionador de qualitat

### Rol incorrecte

- coautor sobirà del model
- substitut de `SDD_GUIDE`
- font de veritat

---

## 6. Anti-Patrons

- passar la spec a `gentle-ai` i acceptar-ho tot
- fer servir la re-auditoria per redissenyar el projecte cada cop
- revisar specs superficials abans de primitives centrals
- barrejar findings interns i externs sense triatge
- deixar una spec "més o menys bé" però sense tancament documental

---

## 7. Ordre Operatiu Recomanat

Fer la re-auditoria per lots segons:

- `00_project_documentation/SDD/02_policies/SPECS_REAUDIT_PRIORITIZATION_POLICY.md`

No per disponibilitat aleatòria o preferència personal.

---

## 8. Resultat Esperat

Una bona re-auditoria:

- no obliga a reimplementar automàticament res
- sí que millora la qualitat de la font de veritat
- i prepara millor el sistema per futures integracions i audits
- deixa un estat final inequívoc: obert, normalitzat o pendent de decisions explícites
