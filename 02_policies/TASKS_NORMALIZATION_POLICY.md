# Tasks Normalization Policy

> **Estat:** Actiu
> **Data:** 2026-04-04
> **Abast:** `artifacts/tasks/`

---

## 1. Propòsit

El directori `artifacts/tasks/` pot tenir una barreja de convencions:

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

Format: `feat-XXX-nom-descriptiu.md`

- ✅ Preferit per a tota feina nova
- ✅ Automatitzable
- ✅ Traçable directament des del feature record

### B. Canònic antic (id sol)

Format: `feat-XXX.md`

- ⚠️ Acceptat per a specs existents
- ⚠️ Recomanable renombrar quan es re-auditi

### C. Legacy / no normalitzat

Format: qualsevol altre (`dashboard-backend.md`, `old-spec-v1.md`, etc.)

- ❌ NO acceptat per a feina nova
- ✅ Pot quedar com a referència històrica a `90_transitional/`

---

## 4. Migració

### Quan renombrar?

- Si un fitxer canvia d'estat (es re-obre per implementació)
- Si un fitxer es re-audita
- Si un fitxer es referencia des d'un altre document nou

### Com renombrar?

1. Crear nou fitxer amb nom canònic
2. Copiar contingut rellevant
3. Actualitzar `task_path` al feature record
4. Moure l'antic a `90_transitional/` o eliminar-lo

---

## 5. Relació amb altres artefactes

| Artefacte | Convenció | Exemple |
|-----------|-----------|---------|
| Design | `feat-XXX-nom.md` | `feat-013-session-tree.md` |
| Spec | `feat-XXX-nom.md` | `feat-013-session-tree.md` |
| Tasks | `feat-XXX-nom.md` | `feat-013-session-tree.md` |
| Feature Record | `feat-XXX.json` | `feat-013.json` |

**Nota:** El `feature_id` al JSON ha de coincidir amb el prefix del `.md`.

---

## 6. Anti-Patrons

- crear `feat-013-tasks.md` quan ja existeix `feat-013.md`
- deixar dos task files per la mateixa feature
- usar noms genèrics (`fix.md`, `update.md`) sense `feat-XXX`

---

## 7. Decisió Operativa

Des de 2026-04-04:

- tota feina nova usa `feat-XXX-nom-descriptiu.md`
- els fitxers antics es mantenen fins que es re-auditen
- no es fa neteja massiva sense un pla de re-auditoria
