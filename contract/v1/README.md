# Canonical SDD Model v1

## Machine-readable authority

- `feature-record.schema.json` defines feature-record fields, types, enums, aliases, paths, and invariants.
- `sdd-protocol.json` defines lifecycle, transitions, gates, blockers, regressions, compatibility interpretation, and conditional checkpoints.

Markdown summaries do not override these files.

## Distribution contract

`install-manifest.json` is the versioned, declarative inventory for a Canonical SDD v1 installation. It maps repository sources to destinations below `docs/sdd/`, declares element types and executable flags, and records runtime dependencies without duplicating lifecycle enums or gate rules.

The installed validator dependency is pinned in `requirements-validator.txt`:

```bash
python -m pip install -r docs/sdd/contract/v1/requirements-validator.txt
```

The installer performs no dependency installation and no network access.

## Install

```bash
python tools/sdd_install.py --target /path/to/product-repo
```

Dry-run:

```bash
python tools/sdd_install.py --target /path/to/product-repo --dry-run --format json
```

The target must exist and must not already contain `docs/sdd/`. Upgrade, overwrite, migration, and uninstall are unsupported.

## Installed self-check

From the product repository root:

```bash
python docs/sdd/tools/sdd_validate.py \
  --schema docs/sdd/contract/v1/feature-record.schema.json \
  --protocol docs/sdd/contract/v1/sdd-protocol.json \
  --self-check \
  --format json
```

## Validation and gates

Tolerant read is the default. Canonical write validation uses `--mode write`.

Historical validation `PASS_WITH_FOLLOWUP` has effective validation `PASS` only when blocking-open-question checks also pass. It is not a verification result.

Active verification `PARTIAL` is invalid. Archived verification `PARTIAL` is a tolerant historical read with effective result `null` and migration review required; the validator never changes the record.

`TASKS -> IMPLEMENT` evaluates semantic prerequisites. An externally resolved policy may request the `TASKS_TO_IMPLEMENT` checkpoint through `--require-approval`; the core does not resolve profiles.

An owner waiver applies only to `AUDIT -> ARCHIVE`.

## Installer exit codes

- `0`: installation or dry-run succeeded.
- `2`: command-line usage error.
- `3`: invalid target or existing installation.
- `4`: invalid or unsafe manifest.
- `5`: missing, mismatched, or unsafe source.
- `6`: copy or finalization failure.

## Repository validation

```bash
python3 -m compileall -q tools tests
python3 -m json.tool contract/v1/feature-record.schema.json
python3 -m json.tool contract/v1/sdd-protocol.json
python3 -m json.tool contract/v1/install-manifest.json
python3 tools/sdd_validate.py --self-check --format json
python3 tools/sdd_conformance.py --format json
python3 -m unittest discover -s tests -v
```
