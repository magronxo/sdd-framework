# Specification: Health Check Endpoint

> **Feature**: feat-001  
> **Phase**: SPEC  
> **Mode Diátaxis**: Reference

---

## Context

This specification formalizes the design from `design.md` into an implementable contract.

## Goals

- [ ] Expose `GET /health` that returns system status
- [ ] Response is deterministic and fast
- [ ] No side effects (safe to call repeatedly)

## Non-Goals

- ❌ Database connectivity check
- ❌ Authentication
- ❌ Metrics or telemetry collection
- ❌ Historical status

## Requirements

### Functional

**RF-01**: The system SHALL expose `GET /health`.

**RF-02**: The endpoint SHALL return HTTP status 200 when the service is operational.

**RF-03**: The response body SHALL be JSON with the following structure:
```json
{
  "status": "ok"
}
```

**RF-04**: The endpoint SHALL respond in < 100ms under normal load (p50 latency).

### Non-Functional

**RNF-01**: The endpoint SHALL not depend on external services (database, cache, third-party APIs).

**RNF-02**: The endpoint SHALL require no authentication.

**RNF-03**: The endpoint SHALL be idempotent (multiple identical requests produce identical responses with no side effects).

## Interface

### Request

```
GET /health
```

No request body. No query parameters. No headers required.

### Response

```
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 15

{"status": "ok"}
```

### Error Handling

This endpoint has no error cases under normal operation. If the service cannot respond, the HTTP layer (or reverse proxy) will return a 502/503 before reaching this endpoint.

## SDT Scenarios

```gherkin
Scenario: Health check returns ok
  When I send GET /health
  Then the response status is 200
  And the response Content-Type is application/json
  And the response body is {"status": "ok"}
  And the response time is < 100ms

Scenario: Health check is idempotent
  Given I have called GET /health
  When I call GET /health again
  Then both responses are identical
  And the response body is {"status": "ok"}
```

## Invariants

- **INV-01**: The endpoint never triggers side effects (no state changes, no logging at error level, no external calls).

## Dependencies

None.

## Type Definitions

None required.

## Performance Budget

| Metric | Limit | Measurement |
|--------|-------|-------------|
| Latency (p50) | < 100ms | Unit test with mocked clock |
| Latency (p99) | < 200ms | Load test (future) |
| Memory | Negligible | Static string response |

## Concurrency Model

Not applicable. This is a stateless, synchronous endpoint with no shared resources.

## Related

- `examples/hello-world-feature/design.md` — design document
- `examples/hello-world-feature/tasks.md` — task breakdown
- `examples/hello-world-feature/validation.md` — validation decision
