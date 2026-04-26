# Policy: Report Envelope (VERIFY / AUDIT)

## Purpose

Estandarditzar el format mínim dels reports de **VERIFY** i **AUDIT** perquè siguin:

- evidence-first (no inventar execució)
- reproduïbles (comandes + cwd + output)
- traçables (quina skill / mode / constraints)
- deterministes (taxonomia de veredicte i gates)

## Scope

Aplica a:

- `00_project_documentation/SDD/audit_reports/verify_*.md`
- `00_project_documentation/SDD/audit_reports/audit_*.md`

Aquest policy **NO** obliga a reescriure reports antics; és un contracte per reports nous o actualitzats.

## Effective date

- 2026-04-09

## Core rule (Evidence-first)

- Si una comanda **no s'ha executat**, cal escriure `NOT EXECUTED` + motiu.
- Si no hi ha output real (o un verify report que l'inclogui), **NO** es pot afirmar “tests passen”.
- En entorns **plan-only** (sense execució), un report de VERIFY **no pot** donar `PASS`.

## Required sections (mínim)

### 1) Header (mínim)

Al principi del document (format lliure), ha d'existir com a mínim:

- `feature_id: feat-XXX`
- `date (UTC): YYYY-MM-DDTHH:MM:SSZ` (o equivalent clar)
- `environment_mode: execute | plan-only | unknown`
- `verification_result: PASS | PARTIAL | FAIL` (verify report) **o** `audit_result: PASS | WARN | FAIL` (audit report)

### 2) `## INVOCATIONS`

Ha d'incloure:

- `audit_engine` / `verify_engine` (nom del protocol/skill o “inline”)
- si aplica: `skill: sdd-verify | sdd-audit | ...`
- notes curtes sobre constraints (p.ex. “PLAN mode → test execution forbidden”)

### 3) `## EVIDENCE`

Ha d'incloure:

- Fitxers llegits (paths)
- Artefactes consultats (feature record, spec, tasks, reports previs)
- Si es fa compliance matrix: llista d'SDT/requirements considerats

### 4) `## COMMANDS`

Per cada comanda rellevant:

- `cwd`
- `command`
- `status: EXECUTED | NOT EXECUTED`
- si `NOT EXECUTED`: `reason`
- si `EXECUTED`: `raw_output` (o excerpt suficient + indicació on trobar el complet)

### 5) `## VERDICT`

Ha d'incloure:

- el veredicte (PASS/PARTIAL/FAIL o PASS/WARN/FAIL)
- 1–3 raons (curtes)
- `next_action` (1–3 passos concrets; si cal, incloure comandes)

### 6) `## SURFACES` (obligatori des de 2026-04-10)

Ha d'incloure la declaració de surfaces aplicables:

```md
## SURFACES
- browser: true|false
- os_fs: true|false
- wiring: true|false
- network: true|false
- env_proxy: true|false
- notes: (opcional)
```

**Regla per defecte:** si cap surface es declara, `wiring: true` s'aplica.

Per cada surface `true`, cal evidència:

| Surface | Evidència | Estat |
|---------|-----------|-------|
| browser | (referència a preflight/network tab) | OK / MISSING |
| wiring | (referència a test handler→core) | OK / MISSING |

## Verdict taxonomy (gates)

### VERIFY (`verification_result`)

- `PASS`
  - Comandes crítiques EXECUTED amb evidència, i passen; i
  - No hi ha cap SDT/requirement crític `UNTESTED` o `UNKNOWN` (si n'hi ha, ha de justificar-se i normalment cau a `PARTIAL`).
- `PARTIAL`
  - Falta evidència runtime per constraints (plan-only, manca runner, manca entorn), o hi ha verificació manual parcial; i
  - No hi ha fallades reproduïdes; i
  - Inclou `next_action` per rerun en execute-capable.
- `FAIL`
  - Qualsevol comanda EXECUTED falla, o hi ha mismatch amb spec/SDT amb evidència, o el feature record/spec no quadra.

### AUDIT (`audit_result`)

- `PASS`
  - Sense desviacions crítiques; evidència coherent; com a mínim un verify report fiable o execució equivalent.
- `WARN`
  - Hi ha riscos/forats de verificació no-crítics (p.ex. manca E2E per constraints), o issues menors amb mitigació/ticket.
- `FAIL`
  - Inconsistències greus, evidència insuficient per afirmar “ready”, o desviacions/material mismatch.

## Notes

- Aquest policy no canvia el pipeline canònic; només estandarditza l’output dels reports.
