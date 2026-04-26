# Audit Report: feat-052-sec-0x-backpressure-wiring-real

**Date:** 2026-04-11  
**Feature:** Backpressure Wiring Real (Two-Tier: API-side observer)  
**Feature ID:** feat-052  
**Phase:** AUDIT

---

## Executive Summary

**Status:** ✅ COMPLETE — All phases executed, all gates passed.

feat-052 implements real backpressure state in `GET /api/v1/kernel/status` via an API-side `BackpressureMonitor` that observes filesystem queue signals (directory sizes + EventBus event rate). This is the correct approach for two-tier architecture where API Server and Kernel are separate processes with no shared memory.

---

## Implementation Details

### New Types
- `BackpressureState` type in `backpressure.go`: `normal | degraded | rejecting`
- `BackpressureProvider` interface with `GetState() BackpressureState`
- `BackpressureMonitor` struct with event ring buffers and periodic queue scanner
- `eventRecord` struct for sliding window tracking

### Modified Files
| File | Change |
|------|--------|
| `02_implementation/internal/api/backpressure.go` | New — BackpressureMonitor, BackpressureState, BackpressureProvider |
| `02_implementation/internal/api/backpressure_test.go` | New — 13 unit tests for state transitions + fail-safe |
| `02_implementation/internal/api/eventbus.go` | Added `Unsubscribe()` method |
| `02_implementation/internal/api/server.go` | Added `backpressureProvider` field + `SetBackpressureProvider()` |
| `02_implementation/internal/api/handlers_kernel.go` | Replaced hardcoded "normal" with `computeBackpressureState()` |
| `02_implementation/cmd/api-server/main.go` | Creates BackpressureMonitor, wires via SetBackpressureProvider() |
| `02_implementation/internal/api/handlers_kernel_test.go` | 2 new tests for API integration + 1 regression fix |

### Two-Tier Architecture
```
Kernel (separate process) → filesystem → API KernelObserver → EventBus → BackpressureMonitor → Server → handleKernelStatus
```

---

## Quality Gates

| Gate | Criterion | Result |
|------|-----------|--------|
| SPEC | Validation result = PASS | ✅ |
| TESTS | All tests pass | ✅ (15 new + all existing) |
| SPEC_ALIGNMENT | Implementation matches spec | ✅ |
| NO_SCOPE_CREEP | No persistence/recovery/HITL/ACLs | ✅ |
| TWO_TIER_CORRECT | BackpressureMonitor in API, not kernel | ✅ |
| FAIL_SAFE | nil provider → degraded (not normal/panic) | ✅ |

---

## Scope Boundaries (Not Violated)

- ❌ No IPC/channel from Kernel process (belongs in SEC-0x+1)
- ❌ No persistence of backpressure state to kernel.state.json
- ❌ No crash recovery
- ❌ No HITL
- ❌ No ACLs related to backpressure
- ❌ No changes to Kernel process internals

---

## Backpressure State Mapping

| State | Condition |
|-------|-----------|
| `normal` | incoming ≤ 5 AND processing ≤ 3 AND arrivals ≤ completions in 30s window |
| `degraded` | incoming > 5 OR processing > 3 OR arrivals > completions (fail-safe: nil provider) |
| `rejecting` | incoming ≥ 20 OR event storm (>10 arrivals in 5s window) |

---

## Observed vs Kernel-Internal Signals

This implementation observes backpressure **as seen by the API server** from filesystem queues and EventBus events. This is correct for two-tier but differs from kernel-internal signals:

| Signal | Source | Available? |
|--------|--------|-----------|
| Queue depth (incoming, processing) | Filesystem scan | ✅ Yes |
| Event rate (arrivals vs completions) | EventBus subscription | ✅ Yes |
| Event storm detection | EventBus subscription | ✅ Yes |
| LoadBalancer decisions | Kernel internal | ❌ No |
| WorkerPool saturation | Kernel internal | ❌ No |
| InferenceSemaphore timeouts | Kernel internal | ❌ No |

For true kernel-internal backpressure, see SEC-0x+1 (IPC/channel scope).

---

## Recommendation

**APPROVE FOR ARCHIVE.** Feature complete per SDD flow. Implementation matches spec. Tests pass. Two-tier architecture correctly followed. Fail-safe defaults in place. Scope not violated.
