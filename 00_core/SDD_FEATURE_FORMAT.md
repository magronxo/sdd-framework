# SDD Feature Format

Cada funcionalitat es representa amb un document de tipus `SYSTEM_SPEC`. Aquest document és l'única font de veritat per al progrés de la feature.

## Camps obligatoris

```json
{
  "id": "feat-<seq>",                 // ex: feat-001
  "type": "SYSTEM_SPEC",
  "state": "DESIGN",                  // estats canònics: DESIGN, SPEC, VALIDATION, TASKS, IMPLEMENT, VERIFY, AUDIT, ARCHIVE (DONE = legacy alias)
  "title": "Breu descripció",
  "created_at": "2026-03-28T10:00:00Z",
  "updated_at": "2026-03-28T10:00:00Z"
}
```

## Estats canònics

| Estat | Significat |
|-------|------------|
| **DESIGN** | Feature definida a nivell de QUÈ, però encara no especificada |
| **SPEC** | Spec redactada; encara pot tenir feedback de validació pendent |
| **VALIDATION** | Fase de revisió de completesa i determinisme |
| **TASKS** | Desglossament de treball mínim i ordenat (derivat d'una spec validada) |
| **IMPLEMENT** | Implementació en curs o preparada per iniciar |
| **VERIFY** | Verificació de compliment respecte a spec i SDT |
| **AUDIT** | Auditoria externa de qualitat, coherència i risc |
| **ARCHIVE** | Tancament documental i consolidació |

**Legacy:** `DONE` existeix en feature records antics. Tractar-lo com a **alias legacy de `ARCHIVE`**. No usar-lo en feina nova.

## Camps opcionals segons l'estat

| Estat | Camps addicionals |
|-------|------------------|
| **DESIGN** | `design_path` (string), `open_questions` (array) |
| **SPEC** | `spec_path` (string), `acceptance_criteria` (array Gherkin) |
| **VALIDATION** | `validation_result` (PASS/FAIL), `validated_at` (ISO8601), `validation_issues` (array, only if FAIL), `validation_details` (string, legacy/freeform) |
| **TASKS** | `task_path` (string), `task_list` (array) |
| **IMPLEMENT** | `implementation_notes` (string) |
| **VERIFY** | `verification_result` (PASS/FAIL), `verification_details` (string) |
| **AUDIT** | `audit_result` (PASS/WARN/FAIL), `audit_reasons` (array) |
| **ARCHIVE** | `archived_at` (ISO8601), `archive_notes` (string) |

## Camps transversals permesos

Aquests camps poden aparèixer en més d'un estat si aporten traçabilitat:

- `design_path`
- `spec_path`
- `task_path`
- `task_list`
- `sdt_scenarios`
- `dependencies`
- `audit_result`
- `validation_result`

## Exemple complet

```json
{
  "id": "feat-001",
  "type": "SYSTEM_SPEC",
  "state": "ARCHIVE",
  "title": "Implementar validació de paths",
  "created_at": "2026-03-28T10:00:00Z",
  "updated_at": "2026-03-28T14:30:00Z",
  "design_path": "artifacts/design/feat-001-path-validation.md",
  "spec_path": "artifacts/specs/feat-001-path-validation.md",
  "sdt_scenarios": [
    {
      "scenario": "Path traversal amb ..",
      "expected_behavior": "Rebutjar amb E_PATH_TRAVERSAL"
    }
  ],
  "task_path": "artifacts/tasks/feat-001-path-validation.md",
  "task_list": [
    "Implementar validador de paths",
    "Afegir test unitari",
    "Documentar error E_PATH_TRAVERSAL"
  ],
  "validation_result": "PASS",
  "verification_result": "PASS",
  "audit_result": "PASS",
  "archived_at": "2026-03-28T14:00:00Z",
  "archive_notes": "Feature completada i consolidada."
}
```

## Nomenclatura de Fitxers (OBLIGATORI)

Tots els fitxers de feature HAN DE seguir el format:

```
feat-{NNN}-{short-name}.md
```

**Exemples:**
- `feat-001-kernel-core.md`
- `feat-006-api-server.md`
- `feat-007-worker-pool.md`
- `feat-012-kernel-status-api.md`

**Cada fitxer JSON ha d'apuntar als paths actuals mitjançant:**
```json
{
  "design_path": "artifacts/design/feat-NNN-short-name.md",
  "spec_path": "artifacts/specs/feat-NNN-short-name.md"
}
```

**Legacy (allowed only for traceability during migration):**
```json
{
  "design_path": "/SDD/artifacts/design/feat-NNN-short-name.md",
  "spec_path": "/SDD/artifacts/specs/feat-NNN-short-name.md"
}
```

## Notes

- El camp `id` ha de ser únic i seqüencial dins del projecte.
- El camp `state` només pot contenir valors de l'enumeració definida.
- Els documents es guarden a `artifacts/features_for_specs/` (o el path configurat a `sdd.config.json`).
- Si hi ha casos legacy o compostos, s'han de marcar explícitament. No s'han de normalitzar via excepcions silencioses.
