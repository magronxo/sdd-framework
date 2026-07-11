# sdd-framework

**Agent-first Spec-Driven Development with explicit, machine-readable contracts.**

## Canonical authority

The Canonical SDD Model v1 has two machine-readable authorities:

1. `contract/v1/feature-record.schema.json` — feature-record fields, types, enums, aliases, paths, and record invariants.
2. `contract/v1/sdd-protocol.json` — lifecycle, transitions, gates, blockers, regressions, and conditional checkpoints.

Markdown documents summarize these contracts. They do not override or redefine them.

A validated feature specification governs the behavior of its active feature. The schema and protocol govern the record and workflow surfaces respectively.

## Lifecycle

`SEED` and `INTAKE` are activities before a persistent feature record exists.

The persistent lifecycle is:

```text
DESIGN -> SPEC -> VALIDATION -> TASKS -> IMPLEMENT -> VERIFY -> AUDIT -> ARCHIVE
```

Progression uses the effective validation result. Canonical writes use `PASS` or `FAIL`; tolerant reads may interpret historical validation `PASS_WITH_FOLLOWUP` as effective `PASS` when no open question is blocking.

`TASKS -> IMPLEMENT` has no universal human-approval requirement. A project, risk, or external-governance policy may activate the `TASKS_TO_IMPLEMENT` checkpoint. Profile resolution and external enforcement are outside the core.

An owner waiver can only permit the documentary transition `AUDIT -> ARCHIVE` after `AUDIT FAIL`. It does not authorize merge, release, deploy, push, or any other external operation.

## Installed layout

The framework is distributed into product repositories exclusively under `docs/sdd/`:

```text
repo/
  docs/
    sdd/
      AGENTS.md
      contract/v1/
        install-manifest.json
        feature-record.schema.json
        sdd-protocol.json
        README.md
        requirements-validator.txt
      tools/sdd_validate.py
      00_core/
      01_execution/
      02_policies/
      03_operations/
      04_project_governance/
      templates/
      init-sdd.sh
      init-sdd.ps1
      sdd.config.json
```

The versioned distribution declaration is `contract/v1/install-manifest.json`. It is the only installation inventory consumed by the installer.

## Install

From a checkout of `sdd-framework`:

```bash
python tools/sdd_install.py --target /path/to/product-repo
```

Preview every destination without writing:

```bash
python tools/sdd_install.py \
  --target /path/to/product-repo \
  --dry-run \
  --format json
```

The target must already exist. The installer refuses a target where `docs/sdd/` already exists. It does not update, migrate, overwrite, uninstall, or write outside the explicit target.

Install the validator dependency in the product environment:

```bash
python -m pip install -r docs/sdd/contract/v1/requirements-validator.txt
```

## Installed smoke test

From the product repository root:

```bash
python docs/sdd/tools/sdd_validate.py \
  --schema docs/sdd/contract/v1/feature-record.schema.json \
  --protocol docs/sdd/contract/v1/sdd-protocol.json \
  --self-check \
  --format json
```

Validate a feature record in tolerant-read mode:

```bash
python docs/sdd/tools/sdd_validate.py \
  docs/sdd/artifacts/features_for_specs/feat-001-example.json \
  --schema docs/sdd/contract/v1/feature-record.schema.json \
  --protocol docs/sdd/contract/v1/sdd-protocol.json \
  --format json
```

Canonical writes use `--mode write`.

## Initialize artifact directories

After installation, review `docs/sdd/sdd.config.json`, then run one initializer from the product repository root:

```bash
bash docs/sdd/init-sdd.sh
```

```powershell
.\docs\sdd\init-sdd.ps1
```

Generated SDD artifacts use repository-relative paths under `docs/sdd/artifacts/`. Product source code remains outside `docs/sdd/`.

## Development validation

```bash
python3 -m compileall -q tools tests
python3 -m json.tool contract/v1/feature-record.schema.json
python3 -m json.tool contract/v1/sdd-protocol.json
python3 -m json.tool contract/v1/install-manifest.json
python3 tools/sdd_validate.py --self-check --format json
python3 tools/sdd_conformance.py --format json
python3 -m unittest discover -s tests -v
```
