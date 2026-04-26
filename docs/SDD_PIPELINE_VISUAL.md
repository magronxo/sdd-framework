# SDD Pipeline Visual Overview

> **Mode Diátaxis**: Reference

## Purpose

Provide **diagrams** for the SDD pipeline, handoffs, and state machines.

Use these diagrams to:
- Understand the flow at a glance
- Onboard new team members
- Debug "where are we stuck?"

---

## Canonical Pipeline

```mermaid
flowchart LR
    D[DESIGN] --> S[SPEC]
    S --> V[VALIDATION]
    V -->|PASS| T[TASKS]
    V -->|FAIL| S
    T --> I[IMPLEMENT]
    I --> VE[VERIFY]
    VE -->|PASS| A[AUDIT]
    VE -->|FAIL| I
    A --> AR[ARCHIVE]

    style D fill:#e1f5fe
    style S fill:#e1f5fe
    style V fill:#fff3e0
    style T fill:#e1f5fe
    style I fill:#e1f5fe
    style VE fill:#fff3e0
    style A fill:#fff3e0
    style AR fill:#e8f5e9
```

**Legend**:
- 🟦 **Blue**: Production phase (creates artifacts or code)
- 🟨 **Orange**: Gate phase (decision: PASS/FAIL)
- 🟩 **Green**: Terminal phase

---

## Role Handoffs

```mermaid
sequenceDiagram
    participant D as Designer
    participant Sp as Specifier
    participant V as Validator
    participant P as Planner
    participant I as Implementer
    participant Ve as Verifier
    participant A as Auditor
    participant Ar as Archiver

    D->>Sp: Design doc
    Note over D,Sp: Gate: DESIGN complete?

    Sp->>V: Spec doc
    Note over Sp,V: Gate: SPEC complete?

    V->>P: validation_result: PASS
    Note over V,P: Gate: VALIDATION passed?
    V-->>Sp: validation_result: FAIL

    P->>I: Tasks doc
    Note over P,I: Gate: Tasks generated?

    I->>Ve: Code + tests
    Note over I,Ve: Gate: Implementation done?

    Ve->>A: verification_result: PASS
    Note over Ve,A: Gate: Tests pass?
    Ve-->>I: verification_result: FAIL

    A->>Ar: Audit report
    Note over A,Ar: Gate: Audit complete?

    Ar->>Ar: state: ARCHIVE
    Note over Ar: Feature closed
```

---

## Pre-SDD State Machine

```mermaid
stateDiagram-v2
    [*] --> CAPTURED
    CAPTURED --> CLASSIFIED
    CLASSIFIED --> TRIAGED

    TRIAGED --> PROMOTED
    TRIAGED --> DEFERRED
    TRIAGED --> REJECTED
    TRIAGED --> MERGED
    TRIAGED --> SPIKED

    PROMOTED --> PRIORITIZED
    PRIORITIZED --> REFINED
    REFINED --> TRANSITIONED
    TRANSITIONED --> SDD_PIPELINE

    DEFERRED --> [*]
    REJECTED --> [*]
    MERGED --> [*]
    SPIKED --> [*]

    note right of TRIAGED
        Decision gate:
        PROMOTE | DEFER | REJECT | MERGE | SPIKE
    end note

    note right of REFINED
        Size check:
        See DECOMPOSITION_AND_SIZE_POLICY.md
    end note
```

---

## Where Does My Idea Go?

```mermaid
flowchart TD
    IDEA[I have an idea/bug/request]

    IDEA --> SEED{Is it well-understood<br/>and has provenance?}
    SEED -->|No| MORE_INFO[Request more info]
    SEED -->|Yes| CAPTURE[Create seed dossier]

    CAPTURE --> CLASSIFY[Classify seed]
    CLASSIFY --> TRIAGE{Triage}

    TRIAGE -->|PROMOTE| REFINE[Refine seed]
    REFINE --> TRANSITION[Create feature record]
    TRANSITION --> DESIGN[Enter SDD pipeline<br/>DESIGN phase]

    TRIAGE -->|DEFER| DEFERRED[Move to seeds/deferred/]
    TRIAGE -->|REJECT| REJECTED[Move to seeds/rejected/]
    TRIAGE -->|MERGE| MERGED[Move to seeds/merged/]
    TRIAGE -->|SPIKE| SPIKED[Create spike feature]

    MORE_INFO --> SEED
    DEFERRED -->|Review date| TRIAGE
```

---

## Feature Record State Machine

```mermaid
stateDiagram-v2
    [*] --> DESIGN
    DESIGN --> SPEC
    SPEC --> VALIDATION

    VALIDATION --> TASKS: PASS
    VALIDATION --> SPEC: FAIL

    TASKS --> IMPLEMENT
    IMPLEMENT --> VERIFY

    VERIFY --> AUDIT: PASS
    VERIFY --> IMPLEMENT: FAIL

    AUDIT --> ARCHIVE
    ARCHIVE --> [*]

    note right of VALIDATION
        validation_result: PASS/FAIL
        recorded in feature record
    end note

    note right of VERIFY
        verification_result: PASS/FAIL
        recorded in feature record
    end note
```

---

## Role Boundaries

```mermaid
flowchart LR
    subgraph WHAT[WHAT]
        D[Designer]
    end

    subgraph HOW[HOW]
        S[Specifier]
    end

    subgraph GATE1[GATE]
        V[Validator]
    end

    subgraph PLAN[PLAN]
        P[Planner]
    end

    subgraph BUILD[BUILD]
        I[Implementer]
    end

    subgraph GATE2[GATE]
        VE[Verifier]
    end

    subgraph REVIEW[REVIEW]
        A[Auditor]
    end

    subgraph CLOSE[CLOSE]
        AR[Archiver]
    end

    D --> S --> V --> P --> I --> VE --> A --> AR

    style V fill:#fff3e0
    style VE fill:#fff3e0
    style A fill:#fff3e0
```

**Rules**:
- No role may produce artifacts owned by another role
- Gates (Validator, Verifier, Auditor) cannot modify artifacts they review
- The Archiver cannot rewrite specs retroactively

---

## Related Documents

- `docs/GETTING_STARTED.md` — step-by-step tutorial
- `docs/PROJECT_TOUR.md` — repository visual tour
- `00_core/SDD_RUNTIME.md` — execution contract
- `00_core/SDD_HANDOFF_CONTRACT.md` — handoff rules
- `03_operations/pre_sdd/PRE_SDD_RUNTIME.md` — Pre-SDD workflow
- `03_operations/WORKFLOW.md` — operational workflow
