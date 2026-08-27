# Spec: {{feature_name}}

**Version:** 1.0
**Status:** Draft
**Reference Design:** `docs/sdd/artifacts/design/{{feature}}.md`

---

## Context
<!-- Why does this specification exist? What need does it solve? -->

---

## Goals
- [ ] Goal 1: measurable
- [ ] Goal 2: measurable

---

## Non-Goals
- ❌ Does not include X
- ❌ Does not integrate with Y

---

## Requirements

### Functional
**RF-01:** The system MUST [behavior] when [condition].
**RF-02:** The system MAY [optional behavior] if [condition].
**RF-03:** The system MUST NOT [prohibited behavior].

### Non-Functional
**NFR-01 (Performance):** Response MUST be < X ms under load Y.
**NFR-02 (Security):** All credentials MUST be stored encrypted.
**NFR-03 (Reliability):** The system MUST recover from transient failures in X attempts.

---

## Type Definitions

Define the data types specific to this feature (structs, enums, unions):

```
Type: ModelStatus
  Values: PENDING | DOWNLOADING | READY | FAILED | ARCHIVED

Type: DownloadConfig
  Fields:
    - model_id: string (format: "org/model-name")
    - quantization: string | null
    - max_workers: int (default: 1, max: 8)
    - resume: boolean (default: true)
```

---

## Inputs

| Field | Type | Source | Validation | Example |
|-------|------|--------|------------|---------|
| `user_id` | `string (UUID)` | HTTP Header | UUID format, non-empty | `"550e8400-..."` |
| `action` | `enum` | JSON Body | Values: `[start, stop]` | `"start"` |

---

## Outputs

| Field | Type | Emission Condition | Example |
|-------|------|-------------------|---------|
| `status` | `string` | Success | `"ok"` |
| `error` | `object` | Any error | `{"code": "E001", "message": "..."}` |

---

## Concurrency Model (Optional)

Fill this section if the feature involves more than one execution thread.

| Aspect | Decision |
|--------|----------|
| **Model** | [sequential / parallel / actor / CSP / async-await / thread-pool] |
| **Max parallelism** | X workers / goroutines / threads |
| **Shared state** | [What is shared and how it is protected: mutex, channel, atomics, etc.] |
| **Ordering guarantees** | [FIFO / LIFO / unordered / priority queue] |
| **Cancellation** | [How ongoing tasks are cancelled: context, signals, etc.] |

---

## Performance Budget (Optional)

Fill this section if the feature has strict performance requirements.

| Metric | Limit | How it is measured |
|--------|-------|-------------------|
| **Latency (p50)** | < X ms | [Benchmark / unit test / endpoint] |
| **Latency (p99)** | < X ms | [Benchmark / unit test / endpoint] |
| **Throughput** | > X req/s | [Load test] |
| **Memory (steady)** | < X MB | [pprof / runtime metric] |
| **Memory (peak)** | < X MB | [pprof / runtime metric] |
| **CPU (steady)** | < X% core | [perf / runtime metric] |

---

## Invariants (Optional)

> **Inspired by TLA+**: properties that must always be true, regardless of execution path.

Fill this section if the feature has properties that must never be broken.

| ID | Invariant | How it is verified |
|----|-----------|-------------------|
| **INV-01** | `[Property that is always true]` | `[Test / assert / monitor]` |
| **INV-02** | `[Property that is always true]` | `[Test / assert / monitor]` |

**Examples**:
- "A user can never have negative balance"
- "The system always responds in < 100ms"
- "There cannot be two active processes with the same ID"

---

## Errors

| Code | Condition | Log message | System action | Notify? |
|------|-----------|-------------|---------------|---------|
| `E001` | Invalid input | `"Invalid action: <value>"` | Return 400, do not persist | ❌ |
| `E002` | External timeout | `"Timeout after Xms"` | Retry 3x, degraded fallback mode | ⚠️ |

---

## Edge Cases

- **Network failure:** The system MUST retry 3 times with exponential backoff. Then, mark as `FAILED` and notify.
- **Unexpected input:** If the response does not match the schema, the system MUST retry 3 times. If it still fails, mark as `FAILED`.
- **Unexpected restart:** The system MUST recover previous state from persistent state and reprocess active tasks.

---

## Acceptance Criteria (Gherkin)

```gherkin
Scenario: <Main case name>
  Given <initial state>
  When  <action>
  Then  <observable result>

Scenario: Error E001 – Invalid input
  Given a request with empty `action` field
  When  the system validates input
  Then  returns error 400 with code E001
  And   does not persist any change
```

---

## Dependencies

- [Dependency 1]
- [Dependency 2]

---

**SDT Scenarios:**
- Happy Path: [description]
- Edge Case: [description]
- Failure Mode: [description]
