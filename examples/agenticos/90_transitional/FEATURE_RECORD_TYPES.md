STATUS: TRANSITIONAL
AUTHORITY: NON-CANONICAL

# Redirect (archived)
**STATUS:** ARCHIVED (redirect header)
**AUTHORITY:** NON-CANONICAL
**ARCHIVED_AT:** 2026-04-09

Canonical format reference: `00_project_documentation/SDD/00_core/SDD_FEATURE_FORMAT.md`
Archived copy (with archive header): `00_project_documentation/SDD/90_transitional/archive/FEATURE_RECORD_TYPES.md`

---

This document is transitional context. It is not a source of truth for the SDD pipeline.
If it conflicts with `00_core/SDD_RUNTIME.md` (execution contract) or validated specs/ADRs, those win.

---

# Feature Record Types

> **Estat:** Actiu  
> **Data:** 2026-04-04  
> **Abast:** Model documental per casos especials a `features_for_specs/`

---

## 1. Propòsit

No totes les features del repositori encaixen en un únic patró simple.

Aquest document defineix tres primitives documentals per evitar que els casos especials es converteixin en caos:

- **composite feature**
- **legacy record**
- **subfeature**

---

## 2. Model Base

El model canònic per defecte continua sent:

- `SYSTEM_SPEC`
- una feature = un design principal + una spec principal + una línia de tasks principal

Qualsevol desviació s'ha de declarar explícitament.

---

## 3. Composite Feature

### Definició

Una **composite feature** és una feature que agrupa dues o més línies de treball fortament vinculades sota un mateix `feature id`.

### Quan s'ha d'usar

Només quan:

- el valor funcional és un de sol
- però hi ha subparts documentals clarament separades
- i té sentit històric o operatiu mantenir-les sota el mateix `id`

### Camps recomanats

```json
{
  "record_type": "composite_feature",
  "subrecords": [
    {
      "name": "frontend",
      "design_path": "...",
      "spec_path": "...",
      "task_path": "..."
    },
    {
      "name": "backend",
      "design_path": "...",
      "spec_path": "...",
      "task_path": "..."
    }
  ]
}
```

### Exemple actual

- `feat-006`

### Regla

Una composite feature **no** ha d'inventar camps ad hoc indefinidament.  
Si hi ha subparts, s'han d'explicitar com a subrecords.

---

## 4. Legacy Record

### Definició

Un **legacy record** és un registre mantingut per traçabilitat històrica que ja no compleix el model canònic actual.

### Quan s'ha d'usar

Quan:

- reflecteix una etapa real del projecte
- no es vol perdre
- però no s'ha de presentar com a exemple normatiu

### Camps recomanats

```json
{
  "record_type": "legacy_record",
  "legacy_reason": "Apunta a un design consolidat fora d'SDD/design",
  "canonical_successor": null
}
```

### Exemple actual

- `feat-009`

### Regla

Un legacy record es conserva, però no governa el model futur.

---

## 5. Subfeature

### Definició

Una **subfeature** és una unitat funcional que depèn semànticament d'una feature pare, però té prou identitat per tenir la seva pròpia spec/tasks.

### Quan s'ha d'usar

Quan:

- no és només un detall intern
- té comportament, validació o tasques pròpies
- però forma part d'una línia major

### Camps recomanats

```json
{
  "record_type": "subfeature",
  "parent_feature": "feat-XXX",
  "subfeature_of": "feat-XXX",
  "subfeature_slug": "..."
}
```

### Exemple actual probable

- `feat-017-react-loop` podria acabar modelat així respecte a una feature més gran de ticket cognition/processament LLM

### Regla

Una subfeature no ha de duplicar confusament l'`id` sense declarar relació amb la feature pare.

---

## 6. Criteris de Decisió

### Si una feature té dues línies principals sota el mateix valor funcional

-> **composite feature**

### Si una feature és només històrica i fora de model

-> **legacy record**

### Si una peça té vida pròpia però depèn d'una feature més gran

-> **subfeature**

---

## 7. Aplicació Inicial al Repo

| Cas | Tipus recomanat |
|-----|------------------|
| `feat-006` | `composite_feature` |
| `feat-009` | `legacy_record` |
| `feat-017-react-loop` | `subfeature` probable |
| `feat-017` | `legacy_record` o registre transitori fora d'esquema |

---

## 8. Regla d'Implementació

No cal migrar tots els JSONs avui mateix.

L'ordre correcte és:

1. definir el model
2. marcar els casos evidents
3. només després enriquir el JSON si cal

---

## 9. Relació amb el Flux

Aquest model no canvia el pipeline SDD.

Només canvia:

- com es representa documentalment un cas especial
- com es manté la traçabilitat
- com es redueix el soroll per a auditories i eines externes

---

## 10. Següent Pas Recomanat

Després d'aquest document, el següent pas útil és decidir si es vol:

1. marcar formalment `feat-006`, `feat-009` i `feat-017*` amb `record_type`
2. o deixar-ho documentat i aplicar-ho només a partir d'ara
