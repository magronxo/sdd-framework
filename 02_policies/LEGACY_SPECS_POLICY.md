# Legacy Specs Policy

## Purpose

Preserve historical specification material for traceability without allowing it to govern active implementation until explicitly promoted.

## Authority boundaries

- `docs/sdd/contract/v1/feature-record.schema.json` governs feature-record shape.
- `docs/sdd/contract/v1/sdd-protocol.json` governs workflow and gates.
- A validated feature spec under `docs/sdd/artifacts/specs/` governs the behavior promised for its active feature.
- Product code is implementation evidence. It does not silently override a validated feature spec.

## Definitions

A canonical spec is a validated specification recorded through the canonical feature record and stored under `docs/sdd/artifacts/specs/`.

Legacy content is any spec-like material that is unvalidated, stale, outside the canonical path, or explicitly marked historical. It is informative and read-only, not active authority.

## Rules

1. No validated canonical spec means no implementation justified by legacy material.
2. Legacy material may inform discovery, comparison, or a new design/spec cycle.
3. Promotion requires an explicit canonical feature workflow and the protocol-defined gates; file relocation alone is not promotion.
4. When code and a validated spec disagree, agents report the mismatch and follow the active feature workflow. They do not declare that either surface silently wins.
5. Corrective work may update implementation to satisfy the validated spec or reopen specification through the declared workflow when the intended behavior has changed.
6. Historical documents are not mass-rewritten, auto-promoted, or auto-migrated.

## Operational handling

- Resolve active specs under `docs/sdd/artifacts/specs/`.
- Store audit/alignment reports under `docs/sdd/artifacts/audit_reports/`.
- Stop when validation or authority is ambiguous.
- Keep legacy material as traceability until an explicit project-owner decision promotes it through the canonical process.
