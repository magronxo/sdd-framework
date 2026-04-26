# Mining — `01_design/08_CONTEXT_BUILDER.md` (legacy)

## Metadata
- Source: `01_design/08_CONTEXT_BUILDER.md`
- Date: 2026-04-09
- Guiding question: Quines decisions mínimes del Context Builder eviten prompts inflats, fuites d’informació i inconsistències entre agents (incloent Auditor/Guardian)?

## A) Seeds desbloquejadores (Top 3)

- Seed: Principi “Zero-Noise” + jerarquia multi-tier (Global → Departament → Agent → Tasca)
  - Why it exists (risk): Sense jerarquia i zero-noise, els agents reben context innecessari (fuites) o inconsistent (decisions errònies).
  - What it unlocks: Context coherent i governable per tot el sistema.
  - Minimal contract: El context es construeix per capes ordenades; només s’injecta el mínim necessari.
  - Cost to change later: Mitjà-alt.
  - Evidence: `08_CONTEXT_BUILDER.md:19`, `08_CONTEXT_BUILDER.md:21`.

- Seed: Pressupost de tokens/bytes (hardware-aware) amb límit explícit (32KB / 8.192 tokens) + truncament per prioritat
  - Why it exists (risk): Sense pressupost estable, el sistema pot caure per OOM/latència i cada feature introdueix truncaments diferents.
  - What it unlocks: Robustesa en hardware limitat i consistència de prompts.
  - Minimal contract: Límit global de context (32KB/8.192 tokens) i política de truncament determinista per prioritat.
  - Cost to change later: Mitjà.
  - Evidence: `08_CONTEXT_BUILDER.md:22`, `08_CONTEXT_BUILDER.md:108`, `08_CONTEXT_BUILDER.md:123`.

- Seed: Segregació Zero Trust del context global + context especial per l’Auditor
  - Why it exists (risk): Si agents de baixa confiança veuen estat global/host, és reconeixement intern i vector d’atac; l’Auditor necessita un context diferent per auditar amb claredat.
  - What it unlocks: Seguretat (IT/Sec-only) i auditoria efectiva.
  - Minimal contract: `agenticos_state`/estat host només és visible per IT/Sec; l’Auditor rep “intenció d’acció” + constitució/diff/risc en lloc d’un objectiu obert.
  - Cost to change later: Alt.
  - Evidence: `08_CONTEXT_BUILDER.md:38`, `08_CONTEXT_BUILDER.md:665`, `08_CONTEXT_BUILDER.md:676`, `08_CONTEXT_BUILDER.md:727`.

## B) Seeds importants però no crítiques (Top 5)

- Seed: Memòria via Librarian (MCP) — prohibició d’accés directe a SQLite des del Context Builder
  - Why it exists (risk): Accés directe a DB crea acoblaments i bypassos de permisos.
  - What it unlocks: Separació de responsabilitats i extensibilitat.
  - Minimal contract: El Context Builder consulta el Librarian via MCP per obtenir engrames rellevants.
  - Cost to change later: Mitjà.
  - Evidence: `08_CONTEXT_BUILDER.md:101`, `08_CONTEXT_BUILDER.md:743`.

- Seed: Budget de tools injectades (≈8KB) com a invariant de context
  - Why it exists (risk): Sense límit, la quantitat d’eines pot menjar-se el context i degradar el comportament.
  - What it unlocks: Prompt estable i “tool calling” usable.
  - Minimal contract: Pressupost dedicat per tools (WASM/MCP) i política de reducció de descripcions llargues.
  - Cost to change later: Baix-mitjà.
  - Evidence: `08_CONTEXT_BUILDER.md:115`, `08_CONTEXT_BUILDER.md:738`.

- Seed: `agenticos_state.md` com a contracte explícit (GAP de format)
  - Why it exists (risk): Sense format definit, l’estat global deriva i es torna inutilitzable/unsafe.
  - What it unlocks: Context global coherent i operació.
  - Minimal contract: Definir un format mínim estable per `agenticos_state.md`.
  - Cost to change later: Mitjà.
  - Evidence: `08_CONTEXT_BUILDER.md:33`, `08_CONTEXT_BUILDER.md:751`.

- Seed: Algorisme de “Sliding Window” per prioritzar engrames (GAP)
  - Why it exists (risk): Sense criteri, la memòria injectada és sorollosa o arbitrària.
  - What it unlocks: Qualitat i determinisme del context.
  - Minimal contract: Estratègia baseline per priorització (temps/relevància/freqüència) sota pressupost.
  - Cost to change later: Mitjà.
  - Evidence: `08_CONTEXT_BUILDER.md:752`, `08_CONTEXT_BUILDER.md:761`.

- Seed: Contracte MCP detallat (DEP-001) com a dependència crítica (GAP)
  - Why it exists (risk): Sense contracte complet, hi ha drift entre components i implementacions incompatibles.
  - What it unlocks: Interoperabilitat estable.
  - Minimal contract: Especificació completa del contracte MCP entre Context Builder i Librarian.
  - Cost to change later: Mitjà.
  - Evidence: `08_CONTEXT_BUILDER.md:230`, `08_CONTEXT_BUILDER.md:750`, `08_CONTEXT_BUILDER.md:772`.

## C) No-seeds
- Blocs llargs de “prompt templates” i “output schema” són exemples de forma, però el seed és el contracte/invariant (pressupostos, segregació, jerarquia), no el text literal.
- Codi Go d’exemple (QueryMemory, etc.) és implementació de referència, no contracte mínim.

## D) Mapa d’implementacions (grosso modo)
- Context layering + zero-noise — UNKNOWN.
- Budgets (32KB/8KB tools) + truncament per prioritat — UNKNOWN.
- Restricció IT/Sec-only de context global — UNKNOWN.
- MCP calls al Librarian (timeout/fallback) — UNKNOWN.
- Context especial de l’Auditor — UNKNOWN.

