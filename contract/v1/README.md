# Canonical SDD Model v1

This directory is the machine-readable authority for Phase 1 of the Canonical SDD Model.

- `feature-record.schema.json` defines the feature-record fields, types, enums, legacy read aliases, paths, timestamps, open questions, results, audit waiver, and internal record invariants.
- `sdd-protocol.json` defines the persistent lifecycle, transitions, gates, human checkpoints, regressions, blockers, compatibility policy, and gate result semantics.

Human-facing documents may summarize these rules, but they do not override these files.

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

Evaluate a transition:

```bash
python tools/sdd_validate.py path/to/feature-record.json \
  --transition TASKS:IMPLEMENT \
  --approval TASKS_TO_IMPLEMENT \
  --format json
```

Validate the schema and protocol themselves:

```bash
python tools/sdd_validate.py --self-check --format json
```

## Exit codes

- `0`: record valid and gate `ALLOW`, or contract self-check passed. Warnings may be present in tolerant read mode.
- `1`: invalid record or gate `DENY`.
- `2`: invocation, input, schema, or protocol loading error.
- `3`: gate `HUMAN_REQUIRED`.

## Compatibility behavior

Canonical writes require `id`, `ARCHIVE`, `task_path`, canonical results, and paths rooted at `docs/sdd/artifacts/`.

Tolerant reads recognize these legacy forms and emit explicit warnings without changing the input:

- `feature_id`
- `DONE` and `ARCHIVED`
- `tasks_path`
- `artifacts/...`
- `PASS_WITH_FOLLOWUP`, interpreted as `PASS` only while follow-up questions are non-blocking

`PARTIAL` is not accepted as completed verification. It produces `VERIFICATION_NOT_EXECUTED`.

## Tests

```bash
python -m compileall -q tools tests
python -m unittest discover -s tests -v
python -m json.tool contract/v1/feature-record.schema.json >/dev/null
python -m json.tool contract/v1/sdd-protocol.json >/dev/null
```

The fixture suite is stored in `tests/fixtures/v1/feature-record-cases.json` and covers the sixteen required cases plus explicit `ARCHIVED` and `tasks_path` compatibility cases.

## Read-only guarantee

The validator reads the record, schema, and protocol and writes only to standard output and standard error. Tests compare the inspected file bytes, SHA-256 digest, and modification timestamp before and after validation.
