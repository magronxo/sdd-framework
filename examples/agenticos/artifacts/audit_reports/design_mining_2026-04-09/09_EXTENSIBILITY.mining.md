# Mining — `01_design/09_EXTENSIBILITY.md` (legacy)

## Metadata
- Source: `01_design/09_EXTENSIBILITY.md`
- Date: 2026-04-09
- Guiding question: Quines decisions mínimes fan que l’ecosistema d’eines (natives/WASM/MCP) sigui plug&play però segur, auditable i estable?

## A) Seeds desbloquejadores (Top 3)

- Seed: Zero Trust d’execució d’eines dinàmiques (aïllament WASM / MCP extern)
  - Why it exists (risk): Sense aïllament, eines dinàmiques són un vector d’execució arbitrària (xarxa/disc) i compromís.
  - What it unlocks: Extensibilitat segura sense recompilar el Kernel.
  - Minimal contract: Eines dinàmiques s’executen aïllades: WASM sandbox o servidor MCP extern, sota control del Kernel.
  - Cost to change later: Alt.
  - Evidence: `09_EXTENSIBILITY.md:19`, `09_EXTENSIBILITY.md:75`, `09_EXTENSIBILITY.md:387`.

- Seed: Tool registry data-driven (schemas) + discovery per escaneig de rutes canòniques + compatibilitat Tool Calling
  - Why it exists (risk): Si el contracte de tools no és data-driven, apareix “implementació per feature” i deriva de formats.
  - What it unlocks: Plug&play d’eines i consistència de tool calling.
  - Minimal contract: El Kernel escaneja rutes compartides (`/departments/shared/{wasm,mcp}/`), carrega schemas, i els converteix a JSON Schema compatible amb tool calling.
  - Cost to change later: Alt.
  - Evidence: `09_EXTENSIBILITY.md:66`, `09_EXTENSIBILITY.md:67`, `09_EXTENSIBILITY.md:353`.

- Seed: Validació de MCP externs (whitelist + auditoria híbrida) com a política canònica
  - Why it exists (risk): MCP extern és una dependència no confiable; sense validació, és superfície d’atac i fuga de dades.
  - What it unlocks: Integració segura de serveis externs (search, etc.).
  - Minimal contract: Model de seguretat per MCP extern amb whitelist (Fase 1) i auditoria híbrida.
  - Cost to change later: Mitjà-alt.
  - Evidence: `09_EXTENSIBILITY.md:635`, `09_EXTENSIBILITY.md:641`.

## B) Seeds importants però no crítiques (Top 5)

- Seed: Regla d’or WASM vs MCP (Kernel valida/audita → WASM; agent treballa → MCP)
  - Why it exists (risk): Sense regla, es barregen canals i es trenca la seguretat per acoblament.
  - What it unlocks: Arquitectura estable i previsible.
  - Minimal contract: Criteri de decisió explícit per ubicar funcionalitat en WASM vs MCP.
  - Cost to change later: Mitjà.
  - Evidence: `09_EXTENSIBILITY.md:404`.

- Seed: Timeout i fallback de MCP (baseline 5s)
  - Why it exists (risk): Sense timeout, MCP pot bloquejar el sistema; sense fallback, memòria/search fan “hard fail”.
  - What it unlocks: Resiliència del runtime.
  - Minimal contract: Timeout per defecte (p.ex. 5s) i comportament de fallback explícit.
  - Cost to change later: Baix-mitjà.
  - Evidence: `09_EXTENSIBILITY.md:238`, `09_EXTENSIBILITY.md:563`.

- Seed: Gestió d’errors WASM amb hard limit (p.ex. 5s) i cancel·lació
  - Why it exists (risk): WASM pot entrar en bucle infinit o OOM; sense límits, bloqueig total.
  - What it unlocks: Execució segura d’eines locals.
  - Minimal contract: Hard limit de temps i cancel·lació per context si s’excedeix.
  - Cost to change later: Baix-mitjà.
  - Evidence: `09_EXTENSIBILITY.md:410`, `09_EXTENSIBILITY.md:413`.

- Seed: “Hardware-aware”: preferir MCP extern per no saturar la RAM local
  - Why it exists (risk): Execució local pesada degrada inferència i kernel.
  - What it unlocks: Operació estable en Orange Pi / ARM.
  - Minimal contract: Polítiques que prioritzin MCP extern per càrregues que no calen localment.
  - Cost to change later: Mitjà.
  - Evidence: `09_EXTENSIBILITY.md:21`.

- Seed: Librarian com a MCP server (fitxers canònics de schema/config)
  - Why it exists (risk): Sense paths canònics, la descoberta deriva.
  - What it unlocks: Interoperabilitat consistent.
  - Minimal contract: Ubicació canònica de `librarian.schema.json` i `librarian.mcp.json` amb `timeout_ms`.
  - Cost to change later: Baix-mitjà.
  - Evidence: `09_EXTENSIBILITY.md:114`, `09_EXTENSIBILITY.md:226`, `09_EXTENSIBILITY.md:238`.

## C) No-seeds
- Structs Go del client MCP i pools: implementació de referència, no contracte mínim (`09_EXTENSIBILITY.md:477`).
- Inventari concret d’eines natives: és catàleg, però el seed és la semàntica/permís, no la llista.

## D) Mapa d’implementacions (grosso modo)
- Discovery de WASM/MCP + conversió a tool schema — UNKNOWN.
- WASM sandbox (wazero) + hard timeouts — UNKNOWN.
- MCP client (unix socket/http) + timeout/fallback — UNKNOWN.
- Validació MCP extern (whitelist/auditoria) — UNKNOWN.

