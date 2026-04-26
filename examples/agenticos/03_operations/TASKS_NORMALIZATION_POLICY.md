# Tasks Normalization Policy

> **Estat:** Actiu  
> **Data:** 2026-04-04  
> **Abast:** `00_project_documentation/SDD/artifacts/tasks/`

---

## 1. Propòsit

El directori `artifacts/tasks/` té avui una barreja de convencions:

- fitxers curts per `id` (`feat-001.md`, `feat-006.md`)
- fitxers amb slug (`feat-013-session-tree.md`)
- fitxers legacy (`dashboard-backend.md`)

Això dificulta:

- la traçabilitat entre `design`, `spec`, `task`
- l'automatització
- la lectura externa del flux

Aquest document fixa el model cap on s'ha d'anar.

---

## 2. Decisió Canònica

### Convenció preferida a futur

Els task files nous han de seguir:

```text
feat-XXX-nom-descriptiu.md
```

Exemples:

- `feat-001-kernel-core.md`
- `feat-006-dashboard-react.md`
- `feat-006-api-server.md`
- `feat-017-react-loop.md`

---

## 3. Estat Actual Acceptat

Mentrestant, el sistema accepta tres categories:

### A. Canònic nou

Fitxers amb `feat-XXX-slug.md`

### B. Curts però tolerats

Fitxers com:

- `feat-001.md`
- `feat-002.md`
- `feat-006.md`

Es toleren perquè ja existeixen i tenen contingut útil, però no són el model final desitjat.

### C. Legacy explícit

Fitxers com:

- `dashboard-backend.md`

Es mantenen només per compatibilitat històrica i s'han de marcar com a alias o legacy.

---

## 4. Regla de Traçabilitat

Cada task file ha de deixar clares aquestes tres coses:

1. quin `feature id` representa
2. quina `spec` canònica governa la feina
3. quin `design` canònic governa la feina

Si un task file és legacy, ho ha de dir explícitament.

---

## 5. Estratègia de Migració

### Fase 1

- no renombrar-ho tot
- documentar el model correcte
- marcar legacy i alias
- corregir referències equivocades

### Fase 2

- crear fitxers canònics nous quan calgui
- deixar redirecció o nota als fitxers antics

### Fase 3

- només quan la traçabilitat estigui clara:
  - renombrat físic
  - neteja de duplicats

---

## 6. Què NO fer

- no renombrar tots els task files en una sola passada
- no inventar task paths inexistents només per “quadrar”
- no amagar un legacy com si fos canònic

---

## 7. Decisió Operativa Actual

Des de 2026-04-04:

- el model preferit és `feat-XXX-slug.md`
- els fitxers curts continuen sent vàlids de manera transitòria
- `dashboard-backend.md` es tracta com a task alias/legacy de la part backend de `feat-006`

---

## 8. Següent Pas Recomanat

Els pròxims passos útils són:

1. corregir els task files legacy més problemàtics
2. decidir si `feat-001.md`, `feat-002.md`, `feat-003.md`, etc. es migraran o es toleraran
3. fer que els `features_for_specs` apuntin només a paths honestos
