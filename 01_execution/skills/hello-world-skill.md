# Skill: Hello World

## Purpose

A minimal example of an SDD skill for reference and learning.

This skill does nothing useful. It demonstrates:
- Skill structure
- Contract definition
- Input/output boundaries
- How to declare surfaces

---

## Skill Contract

### Name
`hello-world`

### Description
Prints a greeting message. Accepts an optional name parameter.

### Surfaces
- `browser`: false
- `os_fs`: false
- `wiring`: false
- `network`: false
- `env_proxy`: false

This skill is **pure computation** with no external dependencies.

---

## Interface

### Input

```json
{
  "name": "string (optional, default: 'World')"
}
```

### Output

```json
{
  "greeting": "string",
  "timestamp": "ISO8601 string"
}
```

### Errors

| Error Code | Condition |
|------------|-----------|
| `E_INVALID_NAME` | Name is not a string |

---

## Example

### Request

```json
{
  "name": "SDD"
}
```

### Response

```json
{
  "greeting": "Hello, SDD!",
  "timestamp": "2026-04-23T14:00:00Z"
}
```

---

## Implementation Notes

- Language: Any (this is a conceptual skill)
- Complexity: Trivial
- Dependencies: None

---

## Why This Matters

Skills in the SDD framework are **capabilities** that agents can invoke. They are:
- Defined by a contract (input, output, surfaces)
- Registered in `03_operations/skills/skills_registry.json`
- Versioned and auditable

This hello-world skill is the template for all other skills.

---

## Related Documents

- `02_policies/SKILLS_SYSTEM.md` — skills registry rules
- `03_operations/skills/README.md` — skills overview
- `01_execution/prompts/` — how agents use skills
