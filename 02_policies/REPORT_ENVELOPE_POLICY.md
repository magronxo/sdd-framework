# Policy: Report Envelope (VERIFY / AUDIT)

> **Diátaxis Mode**: Reference

## Purpose

Standardize the minimum format of **VERIFY** and **AUDIT** reports so they are:

- evidence-first (do not invent execution)
- reproducible (commands + cwd + output)
- traceable (which skill / mode / constraints)
- deterministic (verdict taxonomy and gates)

## Scope

Applies to:

- `artifacts/audit_reports/verify_*.md`
- `artifacts/audit_reports/audit_*.md`

This policy **DOES NOT** force rewriting old reports; it is a contract for new or updated reports.

## Effective date

- 2026-04-09

## Core rule (Evidence-first)

- If a command was **not executed**, write `NOT EXECUTED` + reason.
- If there is no real output (or a verify report that includes it), you **CANNOT** claim "tests pass".
- In **plan-only** environments (without execution), a VERIFY report **cannot** give `PASS`.

## Required sections (minimum)

### 1) Header (minimum)

At the beginning of the document (free format), the following must exist:

- `feature_id: feat-XXX`
- `date (UTC): YYYY-MM-DDTHH:MM:SSZ` (or clear equivalent)
- `environment_mode: execute | plan-only | unknown`
- `verification_result: PASS | PARTIAL | FAIL` (verify report) **or** `audit_result: PASS | WARN | FAIL` (audit report)

### 2) `## INVOCATIONS`

Must include:

- `audit_engine` / `verify_engine` (protocol/skill name or "inline")
- if applicable: `skill: sdd-verify | sdd-audit | ...`
- short notes on constraints (e.g. "PLAN mode → test execution forbidden")

### 3) `## EVIDENCE`

Must include:

- Files read (paths)
- Artifacts consulted (feature record, spec, tasks, previous reports)
- If a compliance matrix is done: list of SDT/requirements considered

### 4) `## COMMANDS`

For each relevant command:

- `cwd`
- `command`
- `status: EXECUTED | NOT EXECUTED`
- if `NOT EXECUTED`: `reason`
- if `EXECUTED`: `raw_output` (or sufficient excerpt + indication where to find the full output)

### 5) `## VERDICT`

Must include:

- the verdict (PASS/PARTIAL/FAIL or PASS/WARN/FAIL)
- 1–3 reasons (short)
- `next_action` (1–3 concrete steps; if needed, include commands)

### 6) `## SURFACES` (mandatory since 2026-04-10)

Must include the declaration of applicable surfaces:

```md
## SURFACES
- browser: true|false
- os_fs: true|false
- wiring: true|false
- network: true|false
- env_proxy: true|false
- notes: (optional)
```

**Default rule:** if no surface is declared, `wiring: true` applies.

For each surface set to `true`, evidence is required:

| Surface | Evidence | State |
|---------|----------|-------|
| browser | (reference to preflight/network tab) | OK / MISSING |
| wiring | (reference to test handler→core) | OK / MISSING |

## Verdict taxonomy (gates)

### VERIFY (`verification_result`)

- `PASS`
  - Critical commands EXECUTED with evidence, and pass; and
  - No critical SDT/requirement is `UNTESTED` or `UNKNOWN` (if there is, it must be justified and normally falls to `PARTIAL`).
- `PARTIAL`
  - Missing runtime evidence due to constraints (plan-only, missing runner, missing environment), or partial manual verification; and
  - No reproduced failures; and
  - Includes `next_action` for rerun in execute-capable environment.
- `FAIL`
  - Any EXECUTED command fails, or there is a mismatch with spec/SDT with evidence, or the feature record/spec does not match.

### AUDIT (`audit_result`)

- `PASS`
  - No critical deviations; coherent evidence; at least one reliable verify report or equivalent execution.
- `WARN`
  - There are non-critical verification risks/gaps (e.g. missing E2E due to constraints), or minor issues with mitigation/ticket.
- `FAIL`
  - Serious inconsistencies, insufficient evidence to claim "ready", or deviations/material mismatch.

## Notes

- This policy does not change the canonical pipeline; it only standardizes report output.
