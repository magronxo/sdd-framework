# sdd-doctor Validation Summary

**Status:** PARTIAL PASS WITH KNOWN SELF-CHECK LIMITATION

---

## Completed Features

| Feature | Status | Notes |
|---------|--------|-------|
| feat-001 Core CLI Doctor | Archived | Accepted coverage risk (60% fixture coverage, no unit tests) |
| feat-002 Governance Checks | Archived | Accepted process deviation (implementation without explicit TASKS approval) |
| feat-003 Artifact Envelope Checks | Archived | Passing unit tests (8/8) |

---

## Verification Commands

```bash
go build ./...
go test ./...
go run ./cmd/sdd-doctor check .
```

---

## Results

| Check | Result |
|-------|--------|
| `go build ./...` | PASS |
| `go test ./...` | PASS |
| `go run ./cmd/sdd-doctor check .` | 20 PASS, 1 WARN, 5 FAIL — exit status 1 |

---

## Self-Check Limitation

sdd-doctor currently treats `examples/sdd-doctor` as if it were a full framework root. It reports missing root framework directories such as `00_core`, `02_policies`, `03_projects`, `04_project_governance`, and `05_workflows`.

This is a **profile/modeling limitation**, not a failure of the completed feature artifacts.

---

## Known Limitations

- No profile mode yet (all projects are validated against full framework rules)
- Structure checks are too strict for nested examples
- feat-001 and feat-002 have limited unit test coverage
- No JSON output yet
- No CI integration yet

---

## Recommended Follow-ups

- **feat-004** Project Profile Detection
- **feat-005** Testing Hardening
- **feat-006** JSON Output

---

## Conclusion

sdd-doctor successfully demonstrates the SDD lifecycle across three archived features, but should not yet be presented as fully self-validating.
