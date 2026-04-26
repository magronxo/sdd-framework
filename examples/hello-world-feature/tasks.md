# Tasks: Health Check Endpoint

> **Feature**: feat-001  
> **Phase**: TASKS  
> **Source Spec**: `spec.md` (validated)

---

## T1 — Create route handler

**Owner**: Implementer
**Input**: Validated spec (RF-01, RF-02, RF-03)
**Output**: Route handler code

Implement `GET /health` that returns:
- Status: 200
- Content-Type: `application/json`
- Body: `{"status": "ok"}`

**Acceptance**:
- [ ] Handler responds to `GET /health`
- [ ] Returns correct status, headers, and body

## T2 — Add unit test for response status

**Owner**: Implementer
**Input**: Spec (RF-02)
**Output**: Test code

Test that `GET /health` returns HTTP 200.

**Acceptance**:
- [ ] Test passes
- [ ] Test fails if handler returns non-200

## T3 — Add unit test for response body

**Owner**: Implementer
**Input**: Spec (RF-03)
**Output**: Test code

Test that response body is exactly `{"status": "ok"}` with correct Content-Type.

**Acceptance**:
- [ ] Test passes
- [ ] Test fails if body or Content-Type is incorrect

## T4 — Add performance assertion

**Owner**: Implementer
**Input**: Spec (RF-04, Performance Budget)
**Output**: Test code

Test that response time is < 100ms under normal conditions.

**Acceptance**:
- [ ] Test passes
- [ ] Note: this may be a mock/clock-based test in unit tests

## T5 — Run full test suite

**Owner**: Verifier
**Input**: Code + tests from T1-T4
**Output**: Verification result

Execute all tests. Verify no regressions in existing tests.

**Acceptance**:
- [ ] All new tests pass
- [ ] All existing tests still pass
- [ ] Coverage report shows health check is covered

## Task Dependencies

```
T1 → T2 → T5
T1 → T3 → T5
T1 → T4 → T5
```

T2, T3, T4 can be done in parallel after T1.
T5 must be last.

## Related

- `examples/hello-world-feature/spec.md` — source spec
- `examples/hello-world-feature/audit.md` — audit report (after VERIFY)
