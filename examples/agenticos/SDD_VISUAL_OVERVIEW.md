# SDD Visual Overview (No canònic) — Mermaid Reference

> **Objectiu**: representació gràfica dels fluxos SDD per a referència ràpida, formació i “project tour”.
>
> **No canònic**: aquest document és per humans. La font d’autoritat continua sent:
> - `00_project_documentation/SDD/00_core/SDD_RUNTIME.md`
> - `00_project_documentation/SDD/00_core/SDD_GUIDE.md`
> - Policies SDD (p. ex. `REPORT_ENVELOPE_POLICY.md`, `INTEGRATION_SURFACE_POLICY.md`)
> - ADRs (`00_project_documentation/05_ADR_DECISION_LOG.md`)

---

## 1) Canonical Pipeline (Flux principal)

```mermaid
flowchart TD
    %% Colors
    classDef gate fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef role fill:#f3e5f5,stroke:#4a148c,stroke-width:1px
    classDef artifact fill:#fff8e1,stroke:#ff6f00,stroke-width:1px
    classDef decision fill:#ffebee,stroke:#b71c1c,stroke-width:2px

    %% Start
    START([Parking Lot<br/>Seeds]) --> PRE_SDD

    %% Pre-SDD
    subgraph PRE_SDD ["PRE-SDD (Intake)"]
        direction TB
        PS1[Capture seed] --> PS2[Classify: feature/spec/gap]
        PS2 --> PS3[Short Analysis]
        PS3 --> PS4{Select<br/>for SDD?}
        PS4 -->|No| PARK[Park]
        PS4 -->|Yes| PS5[Triage + Decompose]
        PS5 --> PS6[Human Approval]
        PS6 --> FR[Feature Record<br/>state: DESIGN]
    end

    %% Canonical Pipeline
    FR --> D[DESIGN]
    D -->|Design doc| D_OUT[design doc]

    D_OUT --> SP[SPEC]
    SP -->|Spec doc| SP_OUT[spec doc]

    SP_OUT --> V[VALIDATION]
    V -->|Spec validated| V_PASS{PASS?}
    V_PASS -->|FAIL| SP
    V_PASS -->|PASS| T[TASKS]

    T -->|Task list| T_OUT[tasks doc]

    T_OUT --> IM[IMPLEMENT]
    IM -->|Code + Tests| IM_OUT[implementation]

    IM_OUT --> VE[VERIFY]
    VE -->|Verify report| VE_OUT[verify report]
    VE_OUT --> VE_RES{Result?}
    VE_RES -->|FAIL| IM
    VE_RES -->|PASS/PARTIAL| AU[AUDIT]

    AU -->|Audit report| AU_RES{Audit Result?}
    AU_RES -->|WARN| ARCH[ARCHIVE]
    AU_RES -->|PASS| ARCH
    AU_RES -->|FAIL| DAU[DEEP AUDIT]

    ARCH --> END([ARCHIVE<br/>DONE])

    style START fill:#c8e6c9,stroke:#2e7d32
    style END fill:#c8e6c9,stroke:#2e7d32
    style PARK fill:#fff9c4,stroke:#f9a825
```

---

## 2) Feature Record State Machine

```mermaid
stateDiagram-v2
    [*] --> DESIGN: Create from seed
    DESIGN --> SPEC: Design doc created
    SPEC --> VALIDATION: Spec doc created
    VALIDATION --> TASKS: validation_result = PASS
    VALIDATION --> SPEC: validation_result = FAIL
    TASKS --> IMPLEMENT: Task list created
    IMPLEMENT --> VERIFY: Code + tests written
    VERIFY --> AUDIT: verification_result = PASS/PARTIAL
    VERIFY --> IMPLEMENT: verification_result = FAIL
    AUDIT --> ARCHIVE: audit_result = PASS/WARN
    AUDIT --> DEEP_AUDIT: audit_result = FAIL
    DEEP_AUDIT --> ARCHIVE: Issues resolved
    ARCHIVE --> [*]
```

---

## 3) PRE-SDD Intake Flow

```mermaid
flowchart LR
    subgraph INPUT ["Input"]
        SEED[Seed from<br/>parking lot]
    end

    subgraph PROCESS ["PRE-SDD Process"]
        CAPTURE[Capture] --> CLASSIFY[Classify]
        CLASSIFY --> ANALYSIS[Short Analysis]
        ANALYSIS --> SELECT{Selected?}
        SELECT -->|No| PARK[Park]
        SELECT -->|Yes| TRIAGE[Triage + Decompose]
        TRIAGE --> APPROVAL{Human<br/>Approval?}
        APPROVAL -->|No| BACK[Back to<br/>Queue]
        APPROVAL -->|Yes| HANDOFF[Handoff]
    end

    subgraph OUTPUT ["Output"]
        HANDOFF --> FR[Feature Record<br/>state: DESIGN]
    end

    style INPUT fill:#bbdefb,stroke:#1976d2
    style OUTPUT fill:#c8e6c9,stroke:#2e7d32
    style PARK fill:#fff9c4,stroke:#f9a825
    style BACK fill:#ffcdd2,stroke:#d32f2f
```

---

## 4) Rols i responsabilitats (no barrejar rols)

```mermaid
flowchart TD
    subgraph ROLES ["Role Matrix"]
        direction LR
        DESIGNER[Designer<br/>WHAT] --> SPECIFIER[Specifier<br/>HOW]
        SPECIFIER --> VALIDATOR[Validator<br/>Complete?]
        VALIDATOR --> PLANNER[Planner<br/>Tasks]
        PLANNER --> IMPLEMENTER[Implementer<br/>Code]
        IMPLEMENTER --> VERIFIER[Verifier<br/>Tests]
        VERIFIER --> AUDITOR[Auditor<br/>Report]
        AUDITOR --> ARCHIVER[Archiver<br/>Close]
    end
```

---

## 5) Gates i decision points

```mermaid
flowchart TD
    G1{Gate 1:<br/>Design Complete?}
    G2{Gate 2:<br/>Spec Valid?}
    G3{Gate 3:<br/>Tasks Defined?}
    G4{Gate 4:<br/>Code Ready?}
    G5{Gate 5:<br/>Verify PASS/PARTIAL?}
    G6{Gate 6:<br/>Audit PASS/WARN?}

    G1 -->|No| STOP1[STOP<br/>Complete design]
    G2 -->|No| STOP2[STOP<br/>Fix spec]
    G3 -->|No| STOP3[STOP<br/>Define tasks]
    G4 -->|No| STOP4[STOP<br/>Implement]
    G5 -->|FAIL| GOTO_IM[Return to<br/>IMPLEMENT]
    G6 -->|FAIL| DEEP[Deep Audit<br/>Required]

    G1 -->|Yes| G2
    G2 -->|Yes| G3
    G3 -->|Yes| G4
    G4 -->|Yes| G5
    G5 -->|PASS/PARTIAL| G6
    G6 -->|PASS/WARN| ARCHIVE[Archive]

    style STOP1 fill:#ffcdd2,stroke:#d32f2f
    style STOP2 fill:#ffcdd2,stroke:#d32f2f
    style STOP3 fill:#ffcdd2,stroke:#d32f2f
    style STOP4 fill:#ffcdd2,stroke:#d32f2f
    style GOTO_IM fill:#ffcdd2,stroke:#d32f2f
    style DEEP fill:#fff9c4,stroke:#f9a825
    style ARCHIVE fill:#c8e6c9,stroke:#2e7d32
```

---

## 6) VERIFY/AUDIT Report Envelope (seccions obligatòries)

```mermaid
flowchart TD
    subgraph REPORT["Report Envelope (Mandatory Sections)"]
        HDR["Header\nfeature_id\ndate (UTC)\nenvironment_mode\nresult"]
        INV["INVOCATIONS\nengine\nskill\nconstraints"]
        EVD["EVIDENCE\nfiles read\nartifacts consulted"]
        CMD["COMMANDS\ncwd\ncommand\nstatus\noutput"]
        SFC["SURFACES\nbrowser / os_fs / wiring / network / env_proxy\n+ evidence OK / MISSING"]
        VDT["VERDICT\nresult\nreasons\nnext_action"]
    end

    HDR --> INV --> EVD --> CMD --> SFC --> VDT
```

---

## 7) Integration Surfaces (Surface Gates)

```mermaid
flowchart TD
    SFCS["Surface Declaration\nRequired in reports"]
    
    SFCS --> BROWSER{"browser?"}
    SFCS --> OSFS{"os_fs?"}
    SFCS --> WIRING{"wiring?"}
    SFCS --> NETWORK{"network?"}
    SFCS --> ENV{"env_proxy?"}

    BROWSER -->|true| E_BROWSER{"Evidence\nOK?"}
    OSFS -->|true| E_OSFS{"Evidence\nOK?"}
    WIRING -->|true| E_WIRING{"Evidence\nOK?"}
    NETWORK -->|true| E_NETWORK{"Evidence\nOK?"}
    ENV -->|true| E_ENV{"Evidence\nOK?"}

    E_BROWSER -->|MISSING| FAIL1["Cannot be PASS"]
    E_OSFS -->|MISSING| FAIL2["Cannot be PASS"]
    E_WIRING -->|MISSING| FAIL3["Cannot be PASS"]
    E_NETWORK -->|MISSING| FAIL4["Cannot be PASS"]
    E_ENV -->|MISSING| FAIL5["Cannot be PASS"]

    E_BROWSER -->|OK| OK_GATE["May be PASS / PARTIAL\n(per constraints)"]
    E_OSFS -->|OK| OK_GATE
    E_WIRING -->|OK| OK_GATE
    E_NETWORK -->|OK| OK_GATE
    E_ENV -->|OK| OK_GATE

    classDef failStyle fill:#ffcdd2,stroke:#d32f2f,stroke-width:2px
    class FAIL1,FAIL2,FAIL3,FAIL4,FAIL5 failStyle
```

---

## 8) Artefactes SDD (carpetes)

```mermaid
flowchart TD
    FR[Feature record<br/>features_for_specs/*.json]

    subgraph ARTIFACTS ["SDD/artifacts/"]
        D[design/]
        SP[specs/]
        T[tasks/]
    end

    subgraph REPORTS ["SDD/audit_reports/"]
        V_R[verify_*.md]
        A_R[audit_*.md]
    end

    FR -->|state: DESIGN| D
    FR -->|state: SPEC| SP
    FR -->|state: TASKS| T
    FR -->|state: VERIFY| V_R
    FR -->|state: AUDIT| A_R
```

---

## 9) Verdict taxonomy (resum)

```mermaid
flowchart TD
    subgraph VERIFY ["VERIFY Result"]
        V_PASS[PASS<br/>Commands EXECUTED + evidence<br/>No critical UNKNOWN]
        V_PARTIAL[PARTIAL<br/>Constraints / missing evidence<br/>Next action: rerun]
        V_FAIL[FAIL<br/>Mismatch / executed failure<br/>Return to IMPLEMENT]
    end

    subgraph AUDIT ["AUDIT Result"]
        A_PASS[PASS<br/>No critical deviations]
        A_WARN[WARN<br/>Gaps/risks with mitigation]
        A_FAIL[FAIL<br/>Inconsistencies / insufficient evidence]
    end

    V_PASS --> A_PASS
    V_PASS --> A_WARN
    V_PARTIAL --> A_WARN
    V_PARTIAL --> A_FAIL
    V_FAIL --> GOTO_IM[→ IMPLEMENT]

    style V_PASS fill:#c8e6c9,stroke:#2e7d32
    style V_PARTIAL fill:#fff9c4,stroke:#f9a825
    style V_FAIL fill:#ffcdd2,stroke:#d32f2f
    style A_PASS fill:#c8e6c9,stroke:#2e7d32
    style A_WARN fill:#fff9c4,stroke:#f9a825
    style A_FAIL fill:#ffcdd2,stroke:#d32f2f
    style GOTO_IM fill:#ffcdd2,stroke:#d32f2f
```

---

## 10) Context Engine (quan usar-lo)

```mermaid
flowchart TD
    DECISION{"Need Context\nEngine?"}
    
    DECISION -->|Large change\n>3 files| CE_YES["Use Context Engine\nDiscovery mode"]
    DECISION -->|Small change\nKnown location| CE_NO["Use direct reading\n(rg/search + file open)"]
    
    CE_YES --> RESULT_CE["Context + Artifacts"]
    CE_NO --> RESULT_DIR["Direct file read"]
```

---

## 11) Change classification (Agent Decision Table)

```mermaid
flowchart TD
    CHANGE{Type of Change?}
    CHANGE -->|Code adjustment| CA[Fix implementation<br/>Keep narrow scope<br/>Update tests]
    CHANGE -->|Contract change| CC[Stop<br/>Update design/spec first]
    CHANGE -->|Parking lot gap| PLG[Record as backlog<br/>Not ready for SDD]
    CHANGE -->|New capability| NC[Full SDD flow<br/>Clear scope<br/>Validation required]

    style CA fill:#c8e6c9,stroke:#2e7d32
    style CC fill:#ffcdd2,stroke:#d32f2f
    style PLG fill:#fff9c4,stroke:#f9a825
    style NC fill:#bbdefb,stroke:#1976d2
```

---

## 12) Chat execution modes (ADR 026)

```mermaid
flowchart TD
    U[User message] --> UI{UI requested_mode?}
    UI -->|interactive| K[Kernel policy]
    UI -->|ticketed| K
    UI -->|none| K

    K -->|interactive allowed| I[Interactive execution<br/>No ticket]
    K -->|must be ticketed| T[Ticketed execution<br/>Create/route ticket]

    I -->|read-only tools only| R1[Immediate response]
    T -->|side effects / long / audit| R2[Return ticket_id + follow]

    note1[[Kernel is authority<br/>Policy is deterministic]] --> K
```

---

## 13) Ticket runtime mínim (ADR 024/025 + feat-019)

```mermaid
flowchart TD
    IN[incoming/<id>.json] --> ACQ[AcquireTicket<br/>atomic move]
    ACQ --> PR[processing/<id>.json]

    PR --> P1[PROCESSING]
    P1 --> P2[AUDITING<br/>Guardian validates]
    P2 -->|ok| P3[EXECUTING<br/>Executor runs]
    P2 -->|reject| FAIL[FAILED<br/>error.code/message]
    P3 -->|ok| OK[COMPLETED<br/>result]
    P3 -->|err| FAIL

    OK --> OUT1[success/<id>.json]
    FAIL --> OUT2[failed/<id>.json]
```

---

## Key takeaways

| Concepte | Regla |
|----------|-------|
| **No validated spec** | No implementation |
| **Validation gate** | `validation_result: PASS` abans de TASKS/IMPLEMENT |
| **Surface gates** | No `PASS` si `surface=true` i evidència MISSING |
| **Evidence-first** | Si no s’ha executat → `NOT EXECUTED` + reason |
| **Plan-only** | VERIFY no pot donar `PASS` |
| **Role separation** | No barrejar rols |
| **Kernel authority** | El Kernel decideix `interactive` vs `ticketed` (ADR 026) |

---

*Generated for human reference — `K:\AgenticOsGen\00_project_documentation`*



