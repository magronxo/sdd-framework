# Example: Hello World Feature

> **Mode Diátaxis**: Tutorial

This directory contains a **complete, realistic example** of one feature flowing through the entire SDD pipeline.

## What is this?

A trivial but complete feature: **"Add a health check endpoint"**.

It demonstrates every phase of the SDD pipeline with real artifacts:
- Feature record (state tracking)
- Design document (WHAT)
- Spec document (HOW)
- Validation decision (gate)
- Tasks document (work breakdown)
- Audit report (final review)

## Files

| File | Phase | Description |
|------|-------|-------------|
| `feat-001-health-check.json` | — | Feature record with state history |
| `design.md` | DESIGN | What the feature does |
| `spec.md` | SPEC | How it does it (interfaces, errors, scenarios) |
| `validation.md` | VALIDATION | Validator decision with checklist |
| `tasks.md` | TASKS | Ordered work breakdown |
| `audit.md` | AUDIT | Final review report |

## How to read this example

1. Start with the **feature record** (`feat-001-health-check.json`) — it links to all other files and shows state transitions
2. Read the **design** to understand WHAT was requested
3. Read the **spec** to see HOW it was formalized
4. Check the **validation** to see the gate that was passed
5. Review the **tasks** to see the work breakdown
6. Read the **audit** to see the final quality check

## Key takeaway

Even a trivial feature (returning `{"status": "ok"}`) goes through the full pipeline. This ensures:
- No ambiguity
- No forgotten edge cases
- Complete traceability
- Reproducible audit trail

---

**Note**: This is a conceptual example. The "code" shown is pseudo-code for clarity. In a real project, the implementer would write actual code in the project's language.
