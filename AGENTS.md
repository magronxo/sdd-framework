# AGENTS.md — Installed SDD entrypoint

## Purpose

This file is the execution entrypoint for agents operating in an installed SDD instance under `docs/sdd/`. It summarizes authority and bounded operating rules; it does not redefine the v1 contracts.

## Authority Order

When sources conflict, apply this order:

1. Validated feature spec for the active feature.
2. `docs/sdd/contract/v1/feature-record.schema.json`
3. `docs/sdd/contract/v1/sdd-protocol.json`
4. `docs/sdd/00_core/SDD_RUNTIME.md`
5. `docs/sdd/00_core/SDD_HANDOFF_CONTRACT.md`
6. `docs/sdd/00_core/SDD_READING_CONTRACT.md`
7. `docs/sdd/02_policies/*.md`
8. `docs/sdd/04_project_governance/*.md`
9. Examples and legacy material, which are non-authoritative unless explicitly promoted.

The schema governs feature-record shape. The protocol governs workflow and gates. Human-readable documents may summarize but never override them.

## Minimal reading

- the active validated feature spec;
- `docs/sdd/contract/v1/feature-record.schema.json`;
- `docs/sdd/contract/v1/sdd-protocol.json`;
- `docs/sdd/00_core/SDD_RUNTIME.md`;
- `docs/sdd/00_core/SDD_HANDOFF_CONTRACT.md`;
- `docs/sdd/sdd.config.json`.

## Persistent lifecycle

`SEED` and `INTAKE` occur before the feature record.

```text
DESIGN -> SPEC -> VALIDATION -> TASKS -> IMPLEMENT -> VERIFY -> AUDIT -> ARCHIVE
```

## Hard rules

- No effective validation `PASS` means no transition to `TASKS` or `IMPLEMENT`.
- Effective validation may come from canonical `PASS` or a tolerated historical read defined by the protocol.
- Blocking open questions remain an independent gate.
- Do not skip states, mix roles, silently normalize legacy input, or expand feature scope.
- `TASKS -> IMPLEMENT` uses core semantic prerequisites. Human approval is required only when an active external policy requests the declared checkpoint.
- The core does not resolve project or risk profiles and does not activate external enforcement.
- An owner waiver affects only `AUDIT -> ARCHIVE`; it has no authority over external operations.

## Verification

- `PASS` permits the protocol-defined handoff to audit.
- `FAIL` permits the protocol-defined regression to implementation.
- When checks cannot be executed, remain in `VERIFY`, leave `verification_result` absent, and record `verification_details` beginning with `NOT EXECUTED:`.
- Never claim execution evidence that does not exist.

## Scope and paths

Product code is outside `docs/sdd/`. Generated framework artifacts use canonical repository-relative paths below `docs/sdd/artifacts/`.

Use minimal context and direct file reads. External systems supply input but are not SDD authority.
