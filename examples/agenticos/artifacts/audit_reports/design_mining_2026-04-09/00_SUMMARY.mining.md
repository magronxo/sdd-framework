# Design Mining — Summary (global)

Data: 2026-04-09  
Corpus: `01_design/*.md` (sense `01_design/flows/`)  
Objectiu: Identificar seeds/decisions que, si no existeixen o no són explícites, acaben generant pegats, inconsistències i refactors cars. (Sense proposar implementació.)

## Global Top 5 seeds (P0/P1)

1) **Ticket com a únic contracte d’IPC + màquina d’estats sobre disc (P0)**
   - Evita protocols paral·lels i drift entre components.
   - Fonts: `02_TICKET_SYSTEM.mining.md`.

2) **Precedència d’autoritat del contracte (authority list) (P0)**
   - Evita múltiples “veritats” (docs vs codi) i dona un mecanisme de resolució de conflictes.
   - Fonts: `TICKET_RUNTIME_TRANSITIONS_MINIMUM.mining.md`.

3) **Transicions mínimes + state→folder + semàntica Router (P0)**
   - Evita estats impossibles i inconsistència operativa/recovery.
   - Fonts: `TICKET_RUNTIME_TRANSITIONS_MINIMUM.mining.md`, `02_TICKET_SYSTEM.mining.md`.

4) **Governança de mutacions: SYSTEM_MUTATION + `.approval.json` (P0)**
   - Evita bypassos i canvis de sistema no auditats.
   - Fonts: `02_TICKET_SYSTEM.mining.md`, `04_SEED_AND_AGENT_ANATOMY.mining.md`, `06_ORCHESTRATION_AND_ROLES.mining.md`.

5) **Zero Trust aplicable: Kernel mediation + modes + SAFE_MODE/LOCKDOWN (P0)**
   - Defineix què pot fer el sistema en cada mode i com es respon a emergències.
   - Fonts: `13_SECURITY_MODEL.mining.md`, `10_OBSERVABILITY.mining.md`, `12_TELEGRAM_BRIDGE.mining.md`.

Nota: **Crash Recovery + `kernel.state.json`** continua sent seed crítica (P1) però queda just fora del Top 5 per prioritzar governança/contracte base. Veure `01_KERNEL.mining.md`.

## Top 5 “drift-prone gaps” detectats (on falta contracte explícit)

1) **Format mínim del context global (`agenticos_state`)** — `08_CONTEXT_BUILDER.mining.md` (doc diu “no especificat”).
2) **Algorisme baseline de sliding window / priorització d’engrams** — `08_CONTEXT_BUILDER.mining.md` (doc ho deixa obert).
3) **Límit de mida per identity/tickets (filesystem)** — `03_FILESYSTEM_AND_DEPARTMENTS.mining.md` (doc diu “no especificat”).
4) **Multi-tenancy / múltiples instàncies al mateix host** — `03_FILESYSTEM_AND_DEPARTMENTS.mining.md` (doc diu “no considerat”).
5) **Contracte i validació d’MCP externs (whitelist/auditoria) com a política canònica** — apareix a `09_EXTENSIBILITY.mining.md` però cal consolidar-lo amb governança actual.

## Recomanació: quines seeds convertir en feature records SDD (sense implementació)

- Ticket runtime contract (schema + transicions + state→folder + router semantics).
- Governança de mutacions (SYSTEM_MUTATION + `.approval.json` + Ring enforcement).
- Modes de seguretat (READ_ONLY/PROPOSE/EXECUTE_SAFE/FULL + SAFE_MODE/LOCKDOWN) + canals de notificació.
- Quarantena (tickets/engrams) + manifest + política de recuperació.
- Crash recovery + `kernel.state.json` (camps mínims + boot recovery).

## Coarse implementation map (només segons docs, sense confirmar codi)

- Docs indiquen components “exists/pendent” de forma inconsistent (p.ex. `01_KERNEL.mining.md` inclou una taula de mòduls).
- En la resta de corpus, molts punts es declaren com a “dissenyat” o “legacy baseline”; tractar l’estat com `UNKNOWN` fins a contrastar amb SDD i implementació.

## Nota sobre fitxers duplicats
- Els fitxers canònics del mining són els `*.mining.md` (sense el sufix extra `.md.mining.md`).
- Els `*.md.mining.md` estan marcats com a **DRAFT (Gemini)** i no s’han d’usar com a mapa.
- Contrast d’autoritats SDD/ADR: `00_CONTRAST_SDD.mining.md`.
