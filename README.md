# SDD Framework

**Agent-first Spec-Driven Development with explicit, machine-readable contracts.**

SDD Framework is an open-source workflow layer for repositories where humans and AI agents collaborate on software changes. It turns feature work into a controlled lifecycle with validated specifications, explicit gates, traceable artifacts, and defined regression paths.

The framework installs inside a product repository under `docs/sdd/`. Product source code remains outside the framework tree.

## Why it exists

AI-assisted development can move quickly while losing scope, evidence, and handoff clarity. SDD makes those boundaries explicit:

- implementation requires an effective validation `PASS` and no blocking open questions;
- lifecycle transitions, gates, blockers, regressions, and checkpoints are machine-readable;
- failed validation and verification return work to a defined earlier phase;
- canonical contracts are separated from their human-readable summaries;
- archival waivers cannot authorize merge, release, deploy, push, or other external operations.

The goal is not unrestricted agent autonomy. The goal is work that is explicit, bounded, reviewable, and reproducible.

## What is included

- **Feature-record schema** — fields, types, enums, paths, aliases, and record invariants.
- **SDD protocol** — lifecycle states, transitions, gates, blockers, regressions, and conditional checkpoints.
- **Validator** — validates records and protocol semantics in tolerant-read or canonical-write mode.
- **Manifest-driven installer** — installs a deterministic SDD layout into an existing repository.
- **Operational documentation** — runtime, handoff, reading, execution, policy, and project-governance material.
- **Templates and initializers** — project configuration and artifact-directory setup for Bash and PowerShell.
- **Conformance tests and CI** — contract, distribution, installer, validator, and internal-consistency checks.

## Lifecycle

`SEED` and `INTAKE` are pre-record activities. The persistent feature lifecycle is:

```text
DESIGN -> SPEC -> VALIDATION -> TASKS -> IMPLEMENT -> VERIFY -> AUDIT -> ARCHIVE
```

Canonical validation and verification results are `PASS` or `FAIL`. Audit results are `PASS`, `WARN`, or `FAIL`.

## Quick start

### Requirements

- Python 3.11 or newer.
- An existing target repository.
- No existing `docs/sdd/` installation in that target.

### Install

Clone the framework and install it into a product repository:

```bash
git clone https://github.com/CollSalvia-Org/sdd-framework.git
cd sdd-framework
python tools/sdd_install.py --target /path/to/product-repo
```

Preview every destination without writing:

```bash
python tools/sdd_install.py \
  --target /path/to/product-repo \
  --dry-run \
  --format json
```

The installer writes only below the explicit target, performs no network access, and refuses to overwrite an existing `docs/sdd/` installation.

### Install the validator dependency

From the product environment:

```bash
python -m pip install -r docs/sdd/contract/v1/requirements-validator.txt
```

### Run the installed self-check

From the product repository root:

```bash
python docs/sdd/tools/sdd_validate.py \
  --schema docs/sdd/contract/v1/feature-record.schema.json \
  --protocol docs/sdd/contract/v1/sdd-protocol.json \
  --self-check \
  --format json
```

### Initialize artifact directories

Review `docs/sdd/sdd.config.json`, then run one initializer from the product repository root:

```bash
bash docs/sdd/init-sdd.sh
```

```powershell
.\docs\sdd\init-sdd.ps1
```

Generated artifacts use repository-relative paths below `docs/sdd/artifacts/`.

## Validate a feature record

Tolerant read is the default:

```bash
python docs/sdd/tools/sdd_validate.py \
  docs/sdd/artifacts/features_for_specs/feat-001-example.json \
  --schema docs/sdd/contract/v1/feature-record.schema.json \
  --protocol docs/sdd/contract/v1/sdd-protocol.json \
  --format json
```

Use canonical-write validation for records that will be persisted:

```bash
python docs/sdd/tools/sdd_validate.py \
  docs/sdd/artifacts/features_for_specs/feat-001-example.json \
  --schema docs/sdd/contract/v1/feature-record.schema.json \
  --protocol docs/sdd/contract/v1/sdd-protocol.json \
  --mode write \
  --format json
```

## Authority model

The two machine-readable authorities are:

1. [`contract/v1/feature-record.schema.json`](contract/v1/feature-record.schema.json) for feature-record shape and invariants.
2. [`contract/v1/sdd-protocol.json`](contract/v1/sdd-protocol.json) for workflow behavior and gates.

A validated feature specification governs the behavior of its active feature. Markdown documents summarize and operationalize the contracts; they do not override them.

See [`AGENTS.md`](AGENTS.md) for the complete authority order and minimal reading set.

## Installed layout

```text
product-repo/
  docs/
    sdd/
      AGENTS.md
      contract/v1/
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
      artifacts/
```

The versioned installation inventory is [`contract/v1/install-manifest.json`](contract/v1/install-manifest.json). It is the only installation inventory consumed by the installer.

## Current scope

Canonical SDD Model v1 currently supports fresh installation into an existing repository.

The installer does **not** update, migrate, overwrite, uninstall, or modify files outside the explicit target. The core protocol also does not resolve project or risk profiles, integrate external wrappers, or grant authority over external systems.

## Development validation

Run from the framework source checkout:

```bash
python3 -m compileall -q tools tests
python3 -m json.tool contract/v1/feature-record.schema.json
python3 -m json.tool contract/v1/sdd-protocol.json
python3 -m json.tool contract/v1/install-manifest.json
python3 tools/sdd_validate.py --self-check --format json
python3 tools/sdd_conformance.py --format json
python3 -m unittest discover -s tests -v
```

The GitHub Actions workflow runs contract validation, conformance checks, installer dry-run, fresh installation, installed self-check, and the unit-test suite.

## Documentation

- [Canonical SDD Model v1](contract/v1/README.md)
- [Agent entrypoint and authority order](AGENTS.md)
- [Runtime contract](00_core/SDD_RUNTIME.md)
- [Handoff contract](00_core/SDD_HANDOFF_CONTRACT.md)
- [Reading contract](00_core/SDD_READING_CONTRACT.md)

## License

Licensed under the [Apache License 2.0](LICENSE).