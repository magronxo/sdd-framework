# Competitive Analysis: SDD Framework

> **Mode Diátaxis**: Explanation
> **Purpose**: Understand where the SDD framework sits in the landscape of development methodologies and governance systems.

---

## Executive Summary

The SDD framework occupies a unique position: it is a **governance layer** for spec-driven development, not an execution engine. Unlike AI agent frameworks (bmat, MetaGPT) that focus on "how to build fast," SDD focuses on **"how to build correctly."**

This analysis compares SDD against methodologies (BDD, TLA+, Clean Architecture) and governance systems (Diátaxis, Rust RFC, Python PEP) to identify strengths, gaps, and opportunities.

---

## Nivell B: Development Methodologies

### 1. BDD (Behavior-Driven Development) — Cucumber / Gherkin

**What it does best**: Executable specifications with ubiquitous language. Business, dev, and test share the same vocabulary.

**What SDD does better**:
- **Separation of DESIGN and SPEC**: BDD skips the "WHAT" phase and goes directly to scenarios. SDD forces explicit design before specification.
- **Independent VALIDATION**: In BDD, the same person often writes Gherkin and implements it. SDD has a dedicated Validator role that cannot modify the spec.
- **External AUDIT**: BDD ends when tests pass. SDD has a post-implementation audit phase.

**What SDD can learn**:
- Make SDT scenarios explicitly executable (link each Gherkin scenario to an automated test).
- Adopt BDD's "ubiquitous language" discipline more formally (already partially done via `GLOSSARY.md`).

**Verdict**: BDD is a **subset** of SDD. SDD subsumes BDD's scenario-writing but adds governance layers above it.

---

### 2. TLA+ (Temporal Logic of Actions) — Leslie Lamport

**What it does best**: Mathematical rigor for concurrent and distributed systems. Model checking finds bugs that tests never would.

**What SDD does better**:
- **Accessibility**: TLA+ requires temporal logic and set theory. SDD specs are written in natural language with structured sections.
- **Product features**: TLA+ is for algorithms (consensus, transactions, locks), not product features ("add dark mode").
- **Delivery pipeline**: TLA+ is an analysis tool, not a methodology. It has no concept of tasks, implementation, or audit.

**What SDD can learn**:
- Adopt the concept of **invariants**: properties that must always hold true, regardless of execution path.
- Use TLA+ (or lightweight alternatives) for critical core algorithms within an SDD feature.

**Verdict**: TLA+ is a **complement** for high-risk systems (financial, medical, distributed). Not direct competition.

---

### 3. Alloy — Daniel Jackson

**What it does best**: Lightweight modeling for data structures and relationships. Finds counterexamples automatically.

**What SDD does better**: Everything outside of data structure modeling. Alloy is academic and niche.

**What SDD can learn**:
- The concept of **automatic counterexample detection** could inspire the Validator to think in "what could go wrong" mode (failure mode analysis).

**Verdict**: Not competitive. Interesting concept but low applicability.

---

### 4. Clean Architecture / Hexagonal / Onion

**What it does best**: Code structure with clear dependency direction (inward-pointing). Framework independence and testability.

**What SDD does better**:
- **Methodology, not just architecture**: Clean Architecture tells you how to structure code, not how to write specs, validate them, or audit them.
- **Document pipeline**: Clean Architecture has no concept of design docs, specs, or feature records.

**What SDD can learn**:
- Explicitly link integration surfaces (`browser`, `wiring`, `os_fs`) to architectural layers (adapters, ports, domain).
- Recommend (not require) architecture diagrams in design documents.

**Verdict**: **Complementary**. Clean Architecture is the target structure; SDD is the process to get there with traceability.

---

## Nivell C: Governance and Documentation

### 1. Diátaxis — Divio

**What it does best**: Classifies documentation into four modes by purpose:
- **Tutorials**: "Learn by doing" (`GETTING_STARTED.md`)
- **How-To Guides**: "Solve a specific problem" (`MIGRATION_PLAYBOOK.md`)
- **Explanation**: "Understand why" (`SDD_GUIDE.md`, this document)
- **Reference**: "Look up facts" (`SDD_RUNTIME.md`, `GLOSSARY.md`)

**What SDD does better**:
- SDD already follows Diátaxis patterns **implicitly**. The framework's documents naturally fall into these categories.
- SDD goes further by adding **authority states** (authoritative vs proposed vs legacy) and **role-based ownership**.

**What SDD can learn**:
- Make Diátaxis modes **explicit** by tagging each document. This helps readers know what to expect.
- Diátaxis does not address document lifecycle (draft → validated → archived). SDD already has this via the pipeline.

**Verdict**: **High-value adoption recommended**. Zero risk, immediate clarity.

---

### 2. Rust RFC Process

**What it does best**:
- Public discussion before implementation
- Explicit states (Proposed, Accepted, Implemented, Stabilized)
- Complete traceability (every language change has an RFC number)

**What SDD does better**:
- **Speed**: RFCs can take years. SDD is designed for product agility while maintaining rigor.
- **Role separation**: RFCs rely on community discussion. SDD has defined roles (Designer, Specifier, Validator).

**What SDD can learn**:
- Add an optional **DISCUSSION phase** before DESIGN for seeds that need community/team input.
- The state machine (Proposed → Accepted → Implemented) is similar to SDD's pipeline but slower.

**Verdict**: **Partial inspiration**. The "discussion before commitment" idea is valuable but optional.

---

### 3. Python PEP (Python Enhancement Proposals)

**What it does best**:
- Sequential numbering (PEP-8, PEP-20, PEP-484) makes referencing easy
- Clear types: Standards Track, Informational, Process
- BDFL Delegation prevents deadlock

**What SDD does better**:
- **Operational pipeline**: PEPs are proposals. SDD is a full delivery pipeline from idea to archive.
- **Agent integration**: PEPs are human-only. SDD is designed for human-AI collaboration.

**What SDD can learn**:
- The concept of **seed types** (`idea`, `bug`, `debt`, `spike`, `risk`) could be extended with `process` for methodology changes.
- Sequential IDs (`feat-001`) already mimic PEP numbering but could be reinforced as a convention.

**Verdict**: **Partial inspiration**. Good governance patterns but different scope.

---

## Comparative Matrix

| Framework | Scope | Pipeline | Validation | Audit | Traceability | Best For |
|-----------|-------|----------|------------|-------|--------------|----------|
| **SDD** | Full delivery (idea → archive) | 8 phases | Independent Validator | External Auditor | Feature records + specs | Human-AI collaborative engineering |
| **BDD** | Testing/specification | 2 phases (spec → test) | Implicit (tests pass) | None | Scenario files | Executable requirements |
| **TLA+** | Algorithm verification | Analysis only | Model checker | None | Spec files | Distributed/concurrent systems |
| **Clean Arch** | Code structure | None | Code review | None | Code organization | Long-lived maintainable systems |
| **Diátaxis** | Documentation structure | None | None | None | Doc taxonomy | Technical documentation |
| **Rust RFC** | Language changes | 4 phases (propose → discuss → accept → implement) | Community review | Core team | RFC repository | Governance of standards |
| **Python PEP** | Language changes | 3 phases (draft → accepted → implemented) | BDFL delegate | None | PEP index | Language evolution |

---

## Key Insight

> **SDD does not compete with these frameworks. It orchestrates them.**

- Use **BDD** for executable acceptance criteria (within SDT scenarios).
- Use **TLA+** for critical algorithm verification (within IMPLEMENT phase).
- Use **Clean Architecture** as the target code structure (within design constraints).
- Use **Diátaxis** to classify all project documentation.
- Use **RFC/PEP patterns** for governance of methodology changes.

SDD is the **meta-layer** that ensures each of these tools is used at the right time, by the right role, with traceability.

---

## Actionable Recommendations

### Adopted in this framework

1. ✅ **Diátaxis mode tags**: Added to all core documents.
2. ✅ **Invariants section**: Added to spec template (inspired by TLA+).

### Reserved for future evaluation

3. 🔲 **Executable SDT bridge**: Link Gherkin scenarios to automated tests per stack.
4. 🔲 **Optional DISCUSSION phase**: Pre-DESIGN team discussion for complex seeds.
5. 🔲 **Seed type `process`**: For methodology changes (requires ADR).
6. 🔲 **Architecture layer mapping**: Link integration surfaces to Clean Architecture layers.

---

## Related Documents

- `docs/GETTING_STARTED.md` — Tutorial mode (Diátaxis)
- `00_core/SDD_GUIDE.md` — Explanation mode (Diátaxis)
- `00_core/SDD_RUNTIME.md` — Reference mode (Diátaxis)
- `03_operations/ROADMAP_TEMPLATE.md` — Strategic planning
- `02_policies/ADR_POLICY.md` — When to document competitive analysis as ADR
