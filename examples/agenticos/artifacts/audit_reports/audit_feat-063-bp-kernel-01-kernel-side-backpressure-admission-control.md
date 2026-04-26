# Audit Report: feat-063 — BP-KERNEL-01 Kernel-side Backpressure Admission Control

**Feature**: feat-063-bp-kernel-01-kernel-side-backpressure-admission-control
**Classification**: BP-KERNEL-01 (Backpressure Kernel-side)
**Audit Date**: 2026-04-12
**Status**: ARCHIVED

---

## Architecture Decision Record

### ADR-063: Kernel-side Backpressure Loop Closure

**Context**: API monitoritzava backpressure i exportava estat, però kernel continuava acceptant tickets sense coneixement de l'estat del sistema.

**Decision**: Kernel llegeix backpressure_state.json (escrit per API) i rebutja tickets quan fused state = rejecting.

**Consequences**:
- Positive: Loop tancat - kernel ara sap l'estat global
- Positive: Rejection happens at kernel level, not just API
- Negative: Polling interval (10s) pot introduir delay
- Negative: File-based IPC (no real-time)

---

## Implementation Quality

| Aspect | Rating | Notes |
|--------|--------|-------|
| Correctness | ✅ EXCELLENT | Tests passen, worst() function correct |
| Security | ✅ ADEQUATE | File written by trusted API, fail-safe degraded |
| Robustness | ✅ GOOD | Stale threshold, no crash on errors |
| Maintainability | ✅ GOOD | Simple, small footprint |

---

## Backpressure Loop Closure

**Before feat-063**:
```
API observa FS queues → backpressure_state=rejecting
                                        ↓
                              API rebutja HTTP POST /tickets
                                        ↓
                     Kernel processa tickets (NO SABIA res)
```

**After feat-063**:
```
API observa FS queues → backpressure_state=rejecting
                                        ↓
                              Kernel llegeix backpressure_state.json
                                        ↓
                              fused = worst(internal, external) = rejecting
                                        ↓
                              Kernel rebutja ticket (E_KERNEL_OVERLOADED)
```

---

## Test Coverage

| Test | Purpose | Status |
|------|---------|--------|
| TestBackpressureReader_FusedRejecting | API rejecting → kernel rejecting | ✅ PASS |
| TestBackpressureReader_FusedDegraded | API degraded → kernel degraded | ✅ PASS |
| TestBackpressureReader_FusedNormal | API normal → kernel normal | ✅ PASS |
| TestBackpressureReader_StaleThresholdDegraded | Stale file treated as degraded | ✅ PASS |
| TestWorstFunction | worst() function (6 scenarios) | ✅ PASS |
| TestBackpressureReader_NoFileDegraded | Missing file fail-safe | ✅ PASS |
| TestBackpressureReader_MalformedJSONDegraded | Malformed JSON fail-safe | ✅ PASS |

---

## Dependencies

- feat-052/053 (API backpressure monitoring) - ✅ Generates backpressure_state.json
- feat-054 (WorkerPool metrics) - ✅ GetMetrics() used for internal signals
- feat-055 (Action Log) - ✅ BACKPRESSURE_REJECT event exists

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| API down but kernel still processing | VERY LOW | MEDIUM | backpressure_state missing → degraded (fail-safe) |
| Polling delay (>10s) before rejection | LOW | MEDIUM | Acceptable for non-real-time workloads |
| File lock on Windows | LOW | LOW | 10s poll interval reduces contention |

---

## Recommendations

1. **Future**: Considerar real-time IPC (chanels) si latency és problema
2. **Future**: Afegir mètriques de rejections a telemetry
3. **Monitoring**: Alertar quan E_KERNEL_OVERLOADED en kernel_events.json

---

## Conclusion

**APPROVED FOR PRODUCTION**

El loop de backpressure ara està tancat. El kernel opera amb coneixement de l'estat global del sistema (API + internal signals). La implementació és simple, robusta, i segueix el principi de fail-safe (stale/missing → degraded).