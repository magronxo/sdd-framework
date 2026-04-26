# Design: feat-077 — sdd-audit-lint Security Controls Map Gate

## Overview

Afegeix el check `E_SEC_CONTROLS_MAP_REQUIRED` a `sdd-audit-lint.ps1` per detectar quan un feature toca codi de seguretat i verificar que `SECURITY_CONTROLS_MAP.md` ha estat consultat/actualitzat.

## Architecture

### Detection Flow

```
┌─────────────────────────────────────────────────────┐
│  1. -ImplementationFiles (explicit, determinista)  │ ← prioritat màxima
└─────────────────────────────────────────────────────┘
                          ↓ (si no)
┌─────────────────────────────────────────────────────┐
│  2. implementation_files del feature record JSON     │
└─────────────────────────────────────────────────────┘
                          ↓ (si no, i -UseGitDiff)
┌─────────────────────────────────────────────────────┐
│  3. git diff --name-only HEAD~1...HEAD             │ ← PRO, SKIP si falla
└─────────────────────────────────────────────────────┘
                          ↓ (cap base de dades)
                    SKIP (no es pot determinar)
```

### Security-Critical Path Detection

Cada path d'implementació es compara amb els patterns de seguretat. Si algun path conté algun pattern, el check aplica.

```
guardian.go     → security-critical ✅
handlers_api.go → NO ❌
executor.go     → security-critical ✅
```

### Evidence Detection

El check cerca en 3 llocs (verify report, audit report, TASKS) per:
- Referència directa a `SECURITY_CONTROLS_MAP.md`
- Línia TASKS amb patró: `DOC: SECURITY_CONTROLS_MAP.md reviewed`

## Changes to sdd-audit-lint.ps1

### New Parameters

```powershell
[string[]]$ImplementationFiles = @()   # nova
[switch]$UseGitDiff                   # nova
```

### New Functions

```powershell
function Get-SecurityCriticalPaths {
    param([string[]]$Paths, [string[]]$Patterns)
    # retorna paths que matchen algún pattern
}

function Test-SecurityControlsMapEvidence {
    param([string]$VerifyContent, [string]$AuditContent, [string]$TasksContent)
    # cerca evidencia en 3 llocs
}

function Get-GitDiffPaths {
    param([string]$RepoRoot, [string]$Base)
    # git diff --name-only base...HEAD
    # SKIP si falla (no error)
}
```

### New Check Block

Al final de tots els checks existents, afegir block per E_SEC_CONTROLS_MAP_REQUIRED.

## Fixtures

Crear estructura de fixtures:
```
04_tools/sdd-audit-lint/
  fixtures/
    pass/
      feat-mock-sec.json
      verify_mock.md
      audit_mock.md
      TASKS.md
    fail/
      feat-mock-sec.json
      verify_mock.md
      audit_mock.md
      TASKS.md
    skip/
      feat-mock-normal.json
      verify_mock.md
```

## Risk Assessment

| Aspect | Risk | Mitigation |
|--------|------|------------|
| git diff failure | False positive FAIL | SKIP si git falla (no bloqueja) |
| Path matching false positive | False FAIL | Només match substring, no regex completa |
| Feature record sense implementation_files | SKIP | Comportament expected — documentat |

## No Breaking Changes

- 7 checks existents no es modifiquen
- Exit codes similars (0/1/2)
- Output format JSON igual
- Funcionalitat existent no afectada
