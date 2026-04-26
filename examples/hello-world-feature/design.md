# Design: Health Check Endpoint

> **Feature**: feat-001  
> **Phase**: DESIGN  
> **Mode Diátaxis**: Explanation

---

## Problem

The system currently has no way for external monitors (load balancers, health check probes, monitoring systems) to verify that the service is alive and responding.

## Goal

Provide a lightweight HTTP endpoint that returns the system's health status.

## Constraints

- Must be **self-contained** (no external dependencies like database or cache)
- Must respond in **< 100ms** under normal load
- Must return **JSON**
- Must use HTTP **GET**

## Out of Scope

- Deep health checks (database connectivity, disk space, memory usage)
- Authentication or authorization
- Rate limiting (handled at infrastructure level)
- Historical health data or metrics

## Acceptance Criteria

- [ ] `GET /health` returns HTTP 200
- [ ] Response body is JSON: `{ "status": "ok" }`
- [ ] Response time is < 100ms under normal load
- [ ] No authentication required

## Open Questions

None. This feature is well-understood and bounded.

## Risks

| Risk | Mitigation |
|------|------------|
| Endpoint could be abused for DoS | Rate limiting at reverse proxy / load balancer |
| "ok" is too vague for production monitoring | Future feature could add `checks` array with subsystem status |

## Proposed Sub-features

None. This feature is atomic and fits within size limits (see `02_policies/DECOMPOSITION_AND_SIZE_POLICY.md`).

## Related

- `examples/hello-world-feature/spec.md` — specification
- `02_policies/DECOMPOSITION_AND_SIZE_POLICY.md` — size limits
