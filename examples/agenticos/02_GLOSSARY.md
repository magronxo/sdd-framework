# Diccionari de Conceptes (Glossary)

Aquest glossari recull els termes fonamentals d'AgenticOS. Per a detalls d'arquitectura, consulta `01_design/`.

---

## Conceptes Core

### Multi-Seed Ready
Arquitectura preparada per escalar horitzontalment. El sistema suporta múltiples instàncies autònomes (Seeds) connectades via Control Plane. Veure `01_design/14_MULTISEED_future.md`.

### Seed
Instància autònoma completa d'AgenticOS: Kernel + Agents + Memòria + Tools + Config. Cada seed té `seed_id` propi.

### Control Plane
Coordinador central que NO executa tasques. Reponsabilitats: registre de seeds, routing de tickets, observabilitat global, autenticació.

### Zero Trust
Arquitectura on l'LLM es considera intrínsecament insegur. L'LLM genera intencions (JSON), no executa accions. El Kernel valida aquestes intencions abans d'executar-les físicament.

### SDD (Spec-Driven Development)
Metodologia: *Cap línia de codi sense especificació*. Tot canvi passa per: Debat -> Decisió (ADR) -> Especificació -> Tasques.

### Tot és un Fitxer
Arquitectura basada en el sistema d'arxius (`.ticket.json`, `.engram.md`). Els agents es comuniquen via lectura/escriptura en bústies (`/inbox`, `/outbox`).

### Radical Observability
Tota acció del sistema està registrada de forma immutable per ser auditable.

### Self-Healing
Mecanisme del Kernel per corregir automàticament JSON mal format de l'LLM, permetent reintents.

### Anti-Suïcidi (Rollback)
Mecanisme de seguretat que restaura la versió anterior si una mutació falla.

---

## Arquitectura

### Kernel
El nucli en Go (Ring 0). Orquestrador determinista que executa accions i gestiona la seguretat.

### FastAuditor
Mòdul intern del Kernel (Ring 0). Validació determinista per regex/patró en <1ms. Sense LLM.

### Guardian
Departament (Ring 1) amb tres rols: Verifier, Tester, Compliance.

### Verifier
Agent dins del Guardian que fa validacions semàntiques amb LLM (Slow-Path).

### Departament
Carpeta física (`/departments/XX/`) que allotja un agent (identitat, bústia, memòria).

### Ticket (`.ticket.json`)
Unitat d'execució i comunicació. Màquina d'estats que viatja pel disc. 11 estats: PENDING, PROCESSING, AUDITING, REQUIRES_HUMAN, WAITING, APPROVED, REJECTED, EXECUTING, LOOPING, COMPLETED, FAILED.

### Engram
Unitat de memòria immutable (Markdown + JSON Frontmatter). Indexada amb SQLite FTS5.

### Librarian
Departament `02_librarian` (Ring 1). Gestiona consultes de memòria via MCP. Conté l'índex global d'Engrams.

### Compactor
Agent dins del Librarian. Fusiona Engrams antics periòdicament per reduir espai.

---

## Tecnologies

### Go
Llenguatge del Kernel (eficiència, binari estàtic, concurrència).

### WASM
WebAssembly. Eines sandboxed per al Kernel (deterministes, aïllades).

### MCP
Model Context Protocol. Eines dinàmiques per als departaments (DB, HTTP, Git, LLM).

### LLM Proxy (Propi)
Proxy LLM propi (feat-002) escrit en Go. Substitueix LiteLLM per problemes de seguretat (ADR-012). Suporta models al núvol via OpenCode API (Go, Zen, Gemini).

### React + ReactFlow
Stack del Frontend (Dashboard IDE Agentic). React per components, ReactFlow per visualització de grafs.

### Bubbletea
Llibreria Go per a TUI (Terminal User Interface). "God Mode" via SSH.

### SQLite FTS5
Base de dades amb cerca de text complet. Índex d'Engrams.

---

## Anells de Privilegi

### Ring 0 (Immutable)
Departaments fundacionals: `00_genesis` i `01_guardian`. No poden ser alterats.

### Ring 1 (Dinàmic)
Departaments operacionals: `10_it_ops`, `02_librarian`. Creats per tasques.

---

## Model de Seguretat

### Fast-Path (Polítiques Estàtiques)
Regles JSON carregades al Kernel. Validació en mil·lisegons.

### Slow-Path (Auditoria Semàntica LLM)
Validació via LLM quan les regles ràpides no són suficients.

### HITL (Human-in-the-Loop)
Aprovació humana requerida per a accions de risc alt.

---

## Seed i Deployment

### Seed
Carpeta/arxiu de configuració que defineix l'estat inicial del sistema. Conté: agents, departaments, polítiques.

### Seed Deployment
Procés de plantar la llavor inicial al sistema. Script: `03_deployments/setup.ps1`.

### Agent Registry
Mòdul que carrega system_prompts des de fitxers JSON (agents/*.json). Implementat a `contextbuilder/agent_registry.go`.

### Tool Registry
Mòdul que carrega eines des de fitxers JSON (config/tools/*.json). Implementat a `contextbuilder/tool_registry.go`.

### Seed Config
Configuració d'una instància Seed. Inclou: seed_id, paths, capacitats. Implementat a `kernel/seed_config.go`.

---

## Flux de Treball

### Spool, Router, Worker, Archive
- **Spool** (`/spool/incoming`): Lloc on es deixen tickets nous.
- **Router** (Kernel): Llegeix, valida JSON, mou a `/inbox`.
- **Worker** (Kernel): Mou atòmic a `/active`, executa.
- **Archive** (`/archive/success`): Tickets completats.

### Self-Distillation
Quan un ticket es resol, el Kernel extreu lliçons apreses i crea un Engram.

### System Mutation
Intent de modificar el codi del Kernel o crear departaments. Requereix QA -> Seguretat -> Quarantena -> Aprovació Humana.

---

## Formats de Fitxer

| Format | Extensió | Ús |
|--------|----------|-----|
| Ticket | `.ticket.json` | Màquina d'estats |
| Engram | `.engram.md` | Memòria immutable |
| Identity | `identity.md` | Prompt de l'agent |
| Config | `llm_config.json` | Configuració model |
| Policy | `.json` | Polítiques Fast-Path |
| Schema | `.schema.json` | Esquemes eines |

**Nota:** YAML prohibit. JSON frontmatter obligatori (ADR-005).

---

*Actualitzat: 2026-04-02 — Afegit Multi-Seed Architecture, SEED-01..03 (AgentRegistry, ToolRegistry, SeedConfig)*
