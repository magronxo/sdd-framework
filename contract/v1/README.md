# Canonical SDD Model v1

This directory is the machine-readable authority for Phase 1 of the Canonical SDD Model.

- `feature-record.schema.json` defines feature-record fields, types, enums, legacy reads, paths, timestamps, open questions, results, audit waiver, and internal record invariants.
- `sdd-protocol.json` defines lifecycle, transitions, gates, conditional human checkpoints, regressions, blockers, compatibility policy, and gate-result semantics.

Human-facing documents may summarize these rules but do not override them.

## Install development dependency

```bash
python -m pip install -r requirements-dev.txt
```

## Validate a record

Tolerant legacy-read mode is the default:

```bash
python tools/sdd_validate.py path/to/feature-record.json
```

Strict canonical-write validation:

```bash
python tools/sdd_validate.py path/to/feature-record.json --mode write
```

Machine-readable output:

```bash
python tools/sdd_validate.py path/to/feature-record.json --format json
```

## Evaluate a transition

Core semantic prerequisites only:

```bash
python tools/sdd_validate.py path/to/feature-record.json \
  --transition TASKS:IMPLEMENT \
  --format json
```

When an already-resolved project, risk, or external governance profile requires approval:

```bash
python tools/sdd_validate.py path/to/feature-record.json \
  --transition TASKS:IMPLEMENT \
  --require-approval TASKS_TO_IMPLEMENT \
  --approval TASKS_TO_IMPLEMENT \
  --format json
```

The core does not resolve profiles and does not integrate with Baranes Tècniques or wrappers in this phase.

## Validation legacy read: `PASS_WITH_FOLLOWUP`

`PASS_WITH_FOLLOWUP` belongs only to `validation_result`.

In tolerant-read mode:

- it emits `LEGACY_PASS_WITH_FOLLOWUP`;
- its effective validation result is `PASS`;
- `VALIDATION -> TASKS` may return `ALLOW` only when no open question is blocking.

In canonical-write mode it produces `NON_CANONICAL_WRITE`.

`verification_result: PASS_WITH_FOLLOWUP` is invalid.

## Verification legacy read: `PARTIAL`

For an active feature, including `state: VERIFY`:

- the record is invalid;
- it produces `VERIFICATION_NOT_EXECUTED`;
- `VERIFY -> AUDIT` returns `DENY`.

For `ARCHIVE`, `DONE`, or `ARCHIVED` in tolerant-read mode:

- the record remains unchanged;
- it emits `LEGACY_PARTIAL_AMBIGUOUS`;
- effective verification is `null`;
- `migration_review_required` is `true`.

Canonical writes reject `PARTIAL` with `NON_CANONICAL_WRITE`.

## Artifact paths

Canonical paths start with:

```text
docs/sdd/artifacts/
```

Tolerant reads accept `artifacts/...` with `LEGACY_ARTIFACT_PATH`.

Any exact path segment equal to `..` is invalid, including immediately after either prefix.

## Exit codes

- `0`: valid record and gate `ALLOW`, or contract self-check passed.
- `1`: invalid record or gate `DENY`.
- `2`: invocation, input, schema, or protocol error.
- `3`: gate `HUMAN_REQUIRED`.

## Compatibility behavior

Canonical writes require `id`, `ARCHIVE`, `task_path`, canonical result values, and canonical artifact paths.

Tolerant reads recognize:

- `feature_id`;
- `DONE` and `ARCHIVED`;
- `tasks_path`;
- `artifacts/...`;
- validation `PASS_WITH_FOLLOWUP`;
- archived verification `PARTIAL`.

No legacy input is silently normalized or rewritten.

## Tests

```bash
python3 -m compileall -q tools tests
python3 -m json.tool contract/v1/feature-record.schema.json
python3 -m json.tool contract/v1/sdd-protocol.json
python3 tools/sdd_validate.py --self-check --format json
python3 -m unittest discover -s tests -v
```

The fixture suite is stored in `tests/fixtures/v1/feature-record-cases.json`.

## Read-only guarantee

The validator reads the record, schema, and protocol and writes only to standard output and standard error. Tests compare inspected file bytes, SHA-256 digest, and modification timestamp before and after validation. Historical `PARTIAL` records are reported for migration review but are not modified, reopened, or migrated.
