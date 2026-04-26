# Policy: External Framework Evaluation

> **Mode Diátaxis**: Reference

## Purpose

Define how to evaluate, adopt, and manage **external frameworks, libraries, and tools**.

This policy prevents:
- Framework sprawl (too many dependencies)
- Hidden coupling (framework becomes the architecture)
- Authority inversion (external docs override project specs)

---

## Principle

> **External frameworks provide input, not decisions.**

The project retains sovereignty over its architecture. No external framework is above `04_project_governance/PROJECT_MANIFEST.md` or `00_core/SDD_RUNTIME.md`.

---

## Evaluation Matrix

Before adopting any external framework, score it across these dimensions:

| Dimension | Weight | Question | Score (1-5) |
|-----------|--------|----------|-------------|
| **Necessity** | High | Do we need this, or can we build it simpler? | |
| **Maturity** | High | Is it stable, documented, and maintained? | |
| **Lock-in** | High | How hard is it to replace or remove? | |
| **Alignment** | Medium | Does it fit our stack and philosophy? | |
| **Community** | Medium | Is there a healthy community and support? | |
| **Size** | Medium | What is the bundle/runtime overhead? | |
| **Security** | High | Has it been audited? Are CVEs handled promptly? | |
| **License** | Medium | Is the license compatible with our project? | |

### Scoring Rules

- **≤ 2 in any High dimension**: Reject or require mitigation plan
- **Overall average < 3**: Reject
- **Lock-in = 1**: Reject unless there is no alternative
- **Security ≤ 2**: Reject unconditionally

---

## Adoption Process

### Step 1: Need Identification

Describe the problem the framework solves. If the problem is not in a seed or feature, capture it first.

### Step 2: Alternatives Analysis

List at least 2 alternatives (including "build it ourselves"). Use the evaluation matrix for each.

### Step 3: ADR (if required)

If the framework affects the stack, non-negotiables, or introduces significant lock-in, write an ADR (`templates/adr.md`).

### Step 4: Trial Period

Before full adoption:
- Implement a spike feature using the framework
- Verify it integrates cleanly with existing surfaces
- Measure the overhead (build time, bundle size, cognitive load)

### Step 5: Approval

- **Tech Lead**: approves technical fit
- **Product Owner**: approves if it affects timeline or user-facing behavior
- **Security Review**: required if the framework handles auth, crypto, networking, or user data

---

## Integration Rules

### Surface Declaration

When a framework touches an integration surface, declare it explicitly:

```markdown
## SURFACES
- browser: true  (React)
- os_fs: false
- wiring: true   (Express)
- network: true  (Axios)
- env_proxy: false
```

See `02_policies/INTEGRATION_SURFACE_POLICY.md`.

### Abstraction Layer

If a framework is likely to be replaced, add a thin abstraction layer:
- Wrap the framework in a project-specific module
- Expose only the interface the project needs
- Isolate framework-specific code to a single directory

### Version Pinning

- Pin exact versions in `package.json`, `go.mod`, `requirements.txt`, etc.
- Document why the version was chosen
- Schedule periodic review of updates (not automatic upgrades)

---

## Authority Inversion Prevention

### What is Authority Inversion?

When an external framework's conventions, patterns, or documentation override the project's own specs and policies.

Examples:
- "React hooks say we should do X" → overrides project state management policy
- "The ORM generates tables this way" → overrides database schema spec
- "The linter enforces this style" → overrides project formatting rules

### Prevention Rules

1. **Specs override frameworks**: If a framework's default behavior conflicts with the spec, the spec wins. Adapt the framework.
2. **Frameworks are implementation details**: They belong in the IMPLEMENT phase, not DESIGN or SPEC.
3. **Document deviations**: If you must deviate from a framework's recommended pattern, document it in the feature's spec or an ADR.

---

## Deprecation and Removal

### When to Remove

- The framework is no longer maintained
- A lighter alternative exists
- The framework's functionality is now native to the language/platform
- The framework causes more problems than it solves

### Removal Process

1. Capture a `debt` seed
2. Evaluate replacement options
3. Write a migration plan (see `03_operations/MIGRATION_PLAYBOOK.md`)
4. Execute as a feature following the SDD pipeline

---

## Related Documents

- `02_policies/ADR_POLICY.md` — when to write an ADR for framework adoption
- `02_policies/INTEGRATION_SURFACE_POLICY.md` — surface definitions
- `04_project_governance/PROJECT_MANIFEST.md` — stack and constraints
- `templates/adr.md` — ADR template
