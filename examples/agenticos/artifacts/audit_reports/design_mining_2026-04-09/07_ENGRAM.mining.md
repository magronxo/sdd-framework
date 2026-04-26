# Mining — `01_design/07_ENGRAM.md` (legacy)

## Metadata
- Source: `01_design/07_ENGRAM.md`
- Date: 2026-04-09
- Guiding question: Quines decisions mínimes de memòria fan que el sistema sigui auditable i eficient (hardware limitat) sense deriva de formats ni bypassos d’escriptura?

## A) Seeds desbloquejadores (Top 3)

- Seed: Format d’Engram com a fitxer `.engram.md` (Markdown) amb JSON frontmatter + immutabilitat
  - Why it exists (risk): Si el format deriva o es pot editar després, es trenca auditabilitat, compatibilitat i “truthfulness” de memòria.
  - What it unlocks: Memòria interoperable humans/agents, diffs i auditoria temporal.
  - Minimal contract: L’engram és un fitxer `.engram.md` llegible; metadades en JSON (no YAML); un cop tancat és immutable (correccions via nou engram).
  - Cost to change later: Alt (migració de corpus i indexació).
  - Evidence: `07_ENGRAM.md:19`, `07_ENGRAM.md:20`, `07_ENGRAM.md:22`.

- Seed: Indexació baseline amb SQLite FTS5 + WAL (per-agent + global) com a decisió de producte/infra
  - Why it exists (risk): Si la memòria “requereix” vector DB o consumeix RAM en idle, el sistema es torna inviable en hardware limitat; si canvia sovint, hi ha refactors cars.
  - What it unlocks: Cerca ràpida i estable, zero-Idle-RAM i crash-safety (WAL).
  - Minimal contract: `engram.db` usa FTS5 i opera en WAL; existeix un índex global i (com a mínim conceptualment) índex per agent.
  - Cost to change later: Mitjà-alt (migracions i compat).
  - Evidence: `07_ENGRAM.md:38`, `07_ENGRAM.md:40`, `07_ENGRAM.md:202`, `07_ENGRAM.md:205`, `07_ENGRAM.md:605`.

- Seed: Contracte MCP del Librarian (`memory_query`/`memory_store`) amb timeout i fallback deterministes
  - Why it exists (risk): Sense contracte, cada consumer (Context Builder, etc.) inventa una API i apareix drift; sense timeout/fallback, la memòria bloqueja el sistema.
  - What it unlocks: Integració estable Context Builder ↔ Librarian i extensibilitat via MCP.
  - Minimal contract: Eines MCP `memory_query` i `memory_store` amb schema; timeout explícit (p.ex. 5s) i fallback a `[]` si hi ha timeout/error.
  - Cost to change later: Mitjà.
  - Evidence: `07_ENGRAM.md:491`, `07_ENGRAM.md:522`, `07_ENGRAM.md:555`, `07_ENGRAM.md:556`, `07_ENGRAM.md:484`.

## B) Seeds importants però no crítiques (Top 5)

- Seed: “Només el Kernel escriu”: Kernel fa `INSERT`, Librarian no fa write a `engram.db`
  - Why it exists (risk): Si el Librarian escriu, es creen bypassos i inconsistència de governança; si hi ha múltiples writers, augmenta corrupció i drift.
  - What it unlocks: Control centralitzat de persistència i auditoria.
  - Minimal contract: Les escriptures a SQLite passen sempre pel Kernel; Librarian només consulta i actualitza índex (sense INSERT/UPDATE/DELETE).
  - Cost to change later: Alt.
  - Evidence: `07_ENGRAM.md:410`, `07_ENGRAM.md:836`.

- Seed: `prompt_hash` com a traçabilitat mínima del prompt origen
  - Why it exists (risk): Sense rastre del prompt, és difícil explicar divergències o regressions.
  - What it unlocks: Debugging/auditoria de memòria.
  - Minimal contract: El model de dades d’engram inclou `prompt_hash` (o equivalent) per correlació.
  - Cost to change later: Mitjà.
  - Evidence: `07_ENGRAM.md:10`.

- Seed: Tags com a array JSON (emmagatzemat com TEXT) com a contracte de cerca
  - Why it exists (risk): Tags inconsistents fan la cerca inestable i trenquen automatitzacions.
  - What it unlocks: Filtrat consistent per topic/tags.
  - Minimal contract: Tags definits com array JSON serialitzat, amb exemples de consulta FTS5.
  - Cost to change later: Mitjà.
  - Evidence: `07_ENGRAM.md:1232`.

- Seed: Decisió explícita “Fase 1 = FTS5 (no vector obligatori)”
  - Why it exists (risk): Si no es fixa baseline, apareixen pressions per “RAG vectorial” i es refà la memòria abans d’hora.
  - What it unlocks: Full de ruta estable (vectorial és futur, no prerequisit).
  - Minimal contract: La selecció de memòria Fase 1 és FTS5 (p.ex. + `topic_key`), amb fases futures com a no-governants.
  - Cost to change later: Mitjà.
  - Evidence: `07_ENGRAM.md:1212`, `07_ENGRAM.md:1213`, `07_ENGRAM.md:595`.

- Seed: Cadena de generació d’engrams (Kernel extreu → valida → Kernel `INSERT` → Librarian indexa)
  - Why it exists (risk): Si la cadena no és explícita, diferents components poden començar a resumir/reescriure memòria.
  - What it unlocks: Responsabilitats clares i menys drift.
  - Minimal contract: La generació i inserció final té propietari (Kernel) i ordre definit.
  - Cost to change later: Mitjà.
  - Evidence: `07_ENGRAM.md:1220`.

## C) No-seeds
- Implementació “HybridSearch”/embeddings: és Fase 2+ i no governa el contracte baseline (`07_ENGRAM.md:1212`).
- Detalls complets de triggers SQL/FTS5: són implementació de referència, no el contracte mínim (`07_ENGRAM.md:308`).

## D) Mapa d’implementacions (grosso modo)
- Escriptura de fitxers `.engram.md` + immutabilitat — UNKNOWN.
- `engram.db` FTS5+WAL (global/per-agent) — UNKNOWN.
- MCP Librarian `memory_query`/`memory_store` + timeout/fallback — UNKNOWN.
- Enforcement “Kernel és l’únic writer” — UNKNOWN.

