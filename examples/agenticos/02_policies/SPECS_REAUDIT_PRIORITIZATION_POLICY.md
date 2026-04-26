# Policy: Priorització de Re-Auditoria de Specs

## Purpose

Evitar el patró d'alt risc: **re-auditar totes les specs alhora**.

La re-auditoria s'ha de fer per lots i per ordre de risc/impacte, per reduir:

- contaminació de specs derivades
- divergència documental
- soroll d'auditoria (moltes conclusions poc accionables)

## Effective date

- 2026-04-09

## Core rule

No té sentit re-auditar totes les specs alhora.

Cal començar per les specs que:

- defineixen primitives centrals del sistema
- tenen més radi d'impacte
- poden contaminar altres specs si estan mal definides
- combinen risc estructural amb alta reutilització

## Application (operativa)

Quan s'obri una ronda de re-auditoria:

1) Definir el lot (3–10 specs) amb criteri de priorització.
2) Aplicar el workflow canònic de re-auditoria:
   - `00_project_documentation/SDD/03_operations/SPEC_REAUDIT_WORKFLOW.md`
3) Documentar el perquè del lot (1 paràgraf) i el següent lot candidat.

## Non-goals

- No redefineix el pipeline SDD.
- No obliga a usar cap eina externa (gentle-ai, context-engine, etc.).
