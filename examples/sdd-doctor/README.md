# sdd-doctor

A deterministic CLI diagnostic tool for validating SDD framework projects. Built as a medium-scope example of the framework itself.

## What it does

sdd-doctor scans a target directory and reports whether the project follows SDD framework conventions.

## What it validates

- **Core structure**: `sdd.config.json`, required directories, artifact directories
- **Governance**: feature records, validation gates (`validation_result: PASS` before TASKS)
- **Artifact envelopes**: required sections in specs, validation reports, and audit reports

## How it demonstrates the SDD pipeline

This example was built using the full SDD lifecycle:

```
SEED → DESIGN → SPEC → VALIDATION → TASKS → IMPLEMENT → VERIFY → AUDIT → ARCHIVE
```

Three features were completed end-to-end:

| Feature | Scope | Status |
|---------|-------|--------|
| feat-001 | Core CLI Doctor | Archived |
| feat-002 | Governance Checks | Archived |
| feat-003 | Artifact Envelope Checks | Archived |

## How to run

```bash
cd examples/sdd-doctor

# Build
go build ./...

# Test
go test ./...

# Run against a project
go run ./cmd/sdd-doctor check <path>
```

## Current validation status

| Check | Result |
|-------|--------|
| `go build ./...` | PASS |
| `go test ./...` | PASS |
| `go run ./cmd/sdd-doctor check .` | Known limitation |

Self-checking against `examples/sdd-doctor` reports missing root framework directories (`00_core`, `02_policies`, etc.) because there is no profile mode yet. This is a modeling limitation, not a feature defect.

## Known limitations

- No profile mode yet (all projects are validated against full framework rules)
- No JSON output yet
- feat-001 and feat-002 have limited unit test coverage

## Recommended future features

- **feat-004** Project Profile Detection
- **feat-005** Testing Hardening
- **feat-006** JSON Output

## License

Same as the parent project: Apache License 2.0.
