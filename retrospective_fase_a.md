# Retrospective: Phase A — Project Governance & Pre-SDD

**Date**: 2026-04-23
**Scope**: 7 new documents + 2 updated files
**Reviewer**: Framework self-audit

---

## Summary

Phase A brings an **operational project layer and a pre-SDD intake system** that the framework did not have. Overall quality is high: documents are coherent, templates are usable, and triage rules are explicit.

**Overall verdict**: ✅ **PASS with 6 issues to fix** (all minor or medium, no blockers)

---

## Findings

### 🔴 Issue 1: Broken Reference — ADR_POLICY.md does not exist

**Location**: `04_project_governance/PROJECT_MANIFEST.md`, line 93

**Problem**: The Manifest references `02_policies/ADR_POLICY.md` within "How to modify this Manifest" and in the "Related Documents" section. This file **does not exist** in the framework.

**Impact**: A user who wants to modify the Manifest will follow a broken link.

**Proposed fix**:
- Option A: Create `02_policies/ADR_POLICY.md` (minimum content: when an ADR is needed, who approves it, where it is stored)
- Option B: Remove the reference and replace it with `templates/adr.md` (which does exist)

**Recommendation**: Option A, because an enterprise framework needs an explicit ADR policy. Additionally, PROJECT_MAP.md already assumes it exists (`artifacts/adr/`).

---

### 🟡 Issue 2: Path Inconsistency — `artifacts/adr/` is not in `sdd.config.json`

**Location**: `04_project_governance/PROJECT_MAP.md`, line 77; `sdd.config.json`

**Problem**: PROJECT_MAP.md shows `artifacts/adr/*.md` as the place for ADRs, but `sdd.config.json` does not have this path in the `artifacts` section.

**Impact**: Agents that consult `sdd.config.json` to resolve paths will not find the ADR location.

**Proposed fix**: Add `"adr": "artifacts/adr"` to `sdd.config.json` → `paths.artifacts`.

---

### 🟡 Issue 3: PROJECT_MAP.md Tree does not show `pre_sdd/` subdirectories

**Location**: `04_project_governance/PROJECT_MAP.md`, "Repository Structure" section

**Problem**: The directory tree shows `03_operations/pre_sdd/` but does not show the operational subfolders (`seeds/`, `seeds/deferred/`, `seeds/rejected/`, `seeds/promoted/`, `seeds/merged/`, `templates/`). This is critical because it is a navigation guide.

**Impact**: A new user does not know where seeds go or where to find them.

**Proposed fix**: Expand the tree:

```
├── 03_operations/pre_sdd/
│   ├── seeds/              # Active seeds (pending triage)
│   ├── seeds/deferred/     # Deferred seeds
│   ├── seeds/rejected/     # Rejected seeds
│   ├── seeds/promoted/     # Seeds promoted to features
│   ├── seeds/merged/       # Consolidated seeds
│   ├── templates/
│   │   ├── seed_dossier.md
│   │   └── triage_batch.md
│   ├── PRE_SDD_CONTRACT.md
│   └── PRE_SDD_RUNTIME.md
```

---

### 🟡 Issue 4: Nomenclature inconsistency — Feature IDs

**Location**: `03_operations/pre_sdd/PRE_SDD_RUNTIME.md`, line 133

**Problem**: The runtime says `feat-{NNN}-{short-name}` but `00_core/SDD_FEATURE_FORMAT.md` shows both `feat_<sequential>_<descriptive-name>.md` (with underscores) and `feat-001-kernel-core.md` (with hyphens). There is inconsistency within the framework itself.

**Impact**: Confusion about the exact format of IDs.

**Proposed fix**: Standardize to `feat-{NNN}-{short-name}` (hyphens) because:
- It is what SDD_RUNTIME.md uses
- It is more readable in URLs and paths
- It is the format of the SDD_FEATURE_FORMAT.md examples

Also, add a note to `SDD_FEATURE_FORMAT.md` to correct the underscore reference.

---

### 🟡 Issue 5: `AGENT_DECISION_TABLE.md` missing from PROJECT_MAP.md

**Location**: `04_project_governance/PROJECT_MAP.md`, "Where Truth Lives" section

**Problem**: `00_core/AGENT_DECISION_TABLE.md` does not appear in the "Where Truth Lives" table. It is a core document that defines how agents make operational decisions (e.g., when a feature is too small to be independent).

**Impact**: A new agent does not know this document exists.

**Proposed fix**: Add to the table:
| **Agent decision rules** | `00_core/AGENT_DECISION_TABLE.md` | `00_core/AGENT_DECISION_TABLE.md` |

---

### 🟢 Issue 6: Seed Lifecycle Contract vs Runtime mismatch

**Location**: `03_operations/pre_sdd/PRE_SDD_CONTRACT.md`, line 120

**Problem**: The contract shows `CAPTURE → CLASSIFY → TRIAGE → {PROMOTE | DEFER | REJECT | MERGE | SPIKE}` but the runtime has 7 phases (`CAPTURE → CLASSIFY → TRIAGE → PRIORITIZE → REFINE → TRANSITION → ARCHIVE`). The contract does not reflect PRIORITIZE, REFINE, or TRANSITION.

**Impact**: The contract (the "rule") does not match the runtime (the "procedure"). This violates the framework principle that the runtime reduces the contract to an executable procedure.

**Proposed fix**: Update the contract lifecycle to show all 7 phases, or at least add a note that the runtime defines the complete flow.

---

## Positive Qualities (To Preserve)

1. **GLOSSARY.md has pre-filled terms** (SDD Feature, Seed, Validation). This provides immediate value without waiting for a team to fill the glossary.

2. **Seed dossier template** has the 6 mandatory sections clearly separated and with explanations. A new reporter knows exactly what to fill.

3. **Triage batch template** includes "Capacity Check" and "Themes & Patterns". This avoids the pattern of "promote everything by default".

4. **PROJECT_MAP.md has role-based navigation**. This is pure gold for onboarding: a developer, a PM, an agent, and an auditor have different and explicit paths.

5. **PRE_SDD_CONTRACT.md prohibits "solutioneering"** with clarity: "capture the problem, not the fix". This attacks one of the main causes of premature specs.

6. **Cross-references are exhaustive**. Every document points to related ones. The navigation network is dense and useful.

---

## Recommendations for Phase B

1. **Fix the 6 issues before continuing**. None are blockers, but all degrade quality.

2. **When creating `GETTING_STARTED.md`**, use the navigation path of the "new developer" from PROJECT_MAP.md as the tutorial structure.

3. **For Mermaid diagrams**, include the state machine from PRE_SDD_RUNTIME.md and the canonical pipeline from SDD_RUNTIME.md. They are visuals that explain more than 100 words.

4. **Consider adding a `seeds/README.md`** inside `03_operations/pre_sdd/seeds/` that explains the subfolder structure. PROJECT_MAP.md shows it but a local README is more discoverable.

---

## Correction Checklist

- [ ] Issue 1: Create `02_policies/ADR_POLICY.md` or fix reference
- [ ] Issue 2: Add `adr` path to `sdd.config.json`
- [ ] Issue 3: Expand PROJECT_MAP.md tree with pre_sdd subfolders
- [ ] Issue 4: Standardize feature ID format
- [ ] Issue 5: Add AGENT_DECISION_TABLE.md to PROJECT_MAP.md
- [ ] Issue 6: Synchronize contract lifecycle with runtime
