# Policy: Report Envelope (VERIFY / AUDIT)

> **Diátaxis Mode**: Reference

## Purpose

Standardize VERIFY and AUDIT reports so they are evidence-first, reproducible, traceable, and consistent with Canonical SDD Model v1.

## Scope

Applies to new or updated reports under:

- `docs/sdd/artifacts/audit_reports/verify_*.md`
- `docs/sdd/artifacts/audit_reports/audit_*.md`

This policy does not rewrite historical reports and does not override the feature-record schema or protocol.

## Core rule: evidence first

- If a command was not executed, write `NOT EXECUTED` and the reason.
- Without direct evidence, a VERIFY report cannot claim PASS.
- A report is supplementary evidence. The standard Verifier or Auditor owns the corresponding canonical feature-record update.

## Required sections

### 1. Header

Include:

- `feature_id: feat-XXX`
- `date (UTC): YYYY-MM-DDTHH:MM:SSZ` or clear equivalent
- `environment_mode: execute | plan-only | unknown`
- for an executed VERIFY decision: `verification_result: PASS | FAIL`
- when required verification could not execute: `verification_status: NOT EXECUTED`
- for AUDIT: `audit_result: PASS | WARN | FAIL`

`verification_status` is report-local. It is not a feature-record field or canonical verification result.

### 2. `## INVOCATIONS`

Include:

- `audit_engine` or `verify_engine` (protocol/skill name or `inline`);
- applicable skill name;
- relevant execution constraints.

### 3. `## EVIDENCE`

Include:

- files read;
- feature record, spec, tasks, and prior reports consulted;
- SDT scenarios and requirements considered.

### 4. `## COMMANDS`

For each relevant command include:

- `cwd`;
- `command`;
- `status: EXECUTED | NOT EXECUTED`;
- reason when not executed;
- raw output or a sufficient referenced excerpt when executed.

### 5. `## VERDICT`

Include:

- VERIFY: `PASS`, `FAIL`, or report-local `NOT EXECUTED`;
- AUDIT: `PASS`, `WARN`, or `FAIL`;
- one to three concise reasons;
- concrete `next_action` items.

### 6. `## SURFACES`

```md
## SURFACES
- browser: true|false
- os_fs: true|false
- wiring: true|false
- network: true|false
- env_proxy: true|false
- notes: (optional report-local prose)
```

If no surface is declared, `wiring: true` applies. Every applicable surface requires direct evidence.

## VERIFY taxonomy and feature-record projection

### PASS

Use only when all required checks executed, conform, and have evidence.

Canonical feature-record PATCH requirements:

```json
{
  "state": "AUDIT",
  "verification_result": "PASS",
  "verified_at": "<ISO8601>",
  "verification_details": "Executed: <commands and evidence>.",
  "updated_at": "<ISO8601>"
}
```

### FAIL

Use when an executed check fails or evidence demonstrates a spec/SDT mismatch.

Canonical feature-record PATCH requirements:

```json
{
  "state": "IMPLEMENT",
  "verification_result": "FAIL",
  "verified_at": "<ISO8601>",
  "verification_details": "Failed: <specific mismatch and evidence>.",
  "updated_at": "<ISO8601>"
}
```

### NOT EXECUTED

Use when required checks cannot run because the environment, runner, or evidence capability is unavailable.

Report header:

```text
verification_status: NOT EXECUTED
```

Canonical feature-record PATCH requirements:

```json
{
  "state": "VERIFY",
  "verification_details": "NOT EXECUTED: <constraint and commands still required>.",
  "updated_at": "<ISO8601>"
}
```

Leave `verification_result` and `verified_at` absent. The record remains in VERIFY and the gate is DENY with blocker `VERIFICATION_NOT_EXECUTED`.

## AUDIT taxonomy

- `PASS`: no critical deviations and reliable verification evidence exists.
- `WARN`: non-critical residual risk exists with an explicit mitigation or follow-up.
- `FAIL`: material inconsistency, insufficient evidence, or serious deviation exists.

AUDIT WARN is separate from VERIFY semantics. AUDIT FAIL blocks `AUDIT -> ARCHIVE` without a valid owner waiver, and v1 selects no automatic repair state.

## Notes

- Report-local fields such as `notes` do not belong to the canonical feature record.
- This policy standardizes report output; it creates no lifecycle state, transition, result, or external-operation authority.
