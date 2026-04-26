# Memory Slice — Candidates de Memòria/Context/Engram

> Data: 2026-04-12  
> Font: `dryrun_extract_2026-04-12.md` — CAND-012, CAND-013, CAND-014, CAND-015, CAND-016  
> Propòsit: Preparar debat d'arquitectura de memòria (engram/context/skills/prompts) **sense aplicar res al PKLot**  
> Regla hard: **NO APPLY** — Cap edició a 04_PARKING_LOT.md, cap creació de SEED dossiers.

---

## Resum del Slice

| CAND | Títol | Capa de Memòria Afectada | Action |
|------|-------|-------------------------:|--------|
| CAND-012 | Context Builder — Multi-Tier Hierarchy + Budgets | Working | NEEDS_REVIEW |
| CAND-013 | Context Segregation — IT/Sec-Only + Auditor | Working / Policy | **KEEP** |
| CAND-014 | Engram Format — .engram.md + JSON Frontmatter | Episodic / Semantic | NEEDS_REVIEW |
| CAND-015 | Engram Index — SQLite FTS5 + WAL | Episodic / Semantic | NEEDS_REVIEW |
| CAND-016 | Librarian MCP Contract — memory_query/store | Operational | DEFER |

---

## Vocabulari de Capes de Memòria (proposat)

Per consistència en el debat, proposem aquest vocabulari:

| Capa | Descripció | Exemples | Persistència |
|------|-----------|----------|--------------|
| **Working** | Context actiu de l'agent durant una sessió/tasca. Prompt actual, estat immediat. | Context Builder output, prompt injectat a LLM | Volàtil (sessió) |
| **Episodic** | Records d'esdeveniments específics, traça d'execucions. | .engram.md amb traça de tickets, decisions | Persistent (fitxers) |
| **Semantic** | Coneixement general extret, patterns, documentació. | Engrams de documentació, FAQs, patterns | Persistent (FTS5/SQLite) |
| **Policy** | Regles de governança, permisos, modes. | Security modes, capability gating, segregation | Persistent (config) |
| **Operational** | Estat del sistema, mètriques, health. | kernel.state.json, logs, telemetry | Persistent / Volàtil mix |

---

## Detall de Candidates

### CAND-012 — Context Builder: Multi-Tier Hierarchy + Token/Byte Budgets

**Problema (2-4 línies):**  
Sense pressupost estable i jerarquia de context, els prompts creixen incontroladament fins a provocar OOM o latència inacceptable. Cada component injecta el que vol sense límit ni prioritat.

**Intent:**  
Definir jerarquia (Global → Departament → Agent → Tasca) amb pressupostos explícits (32KB global, 8KB per tools) i política de truncament determinista per prioritat.

**Capa de memòria afectada:** **Working** — Defineix com es construeix i es limita el context actiu que rep l'agent.

**Contracts existents que toca:**
- `feat-008` (Context Builder — SPEC DONE però estat d'implementació unknown)
- `08_CONTEXT_BUILDER.mining.md` identifica gap: "Algorisme baseline de sliding window — no especificat"

**Risc principal:** Complexitat del truncament — si és massag complex, el sistema fallarà silenciosament.

---

### CAND-013 — Context Segregation: IT/Sec-Only Global State + Auditor Context

**Problema (2-4 línies):**  
Agents de baixa confiança veuen estat global del host (agenticos_state), el qual és reconeixement intern i vector d'atac. L'Auditor necessita un context diferent per auditar amb claredat sense exposició innecessària.

**Intent:**  
Restringir `agenticos_state` només a rols IT/Sec; definir context especial per Auditor amb "intenció d'acció" + constitució/diff/risc en lloc d'objectius oberts.

**Capa de memòria afectada:** **Working** (el que veu l'agent) + **Policy** (qui pot veure què).

**Contracts existents que toca:**
- `feat-008` (Context Builder — on es construeix el context)
- `00_SUMMARY.mining.md:33` — drift-prone gap #1: "Format mínim del context global no especificat"

**Risc principal:** Complexitat de permisos — pot crear latència addicional al context builder.

---

### CAND-014 — Engram Format: .engram.md + JSON Frontmatter + Immutability

**Problema (2-4 línies):**  
Sense format formal per als engrams, la memòria persistent deriva entre versions i es trenca la capacitat d'auditar o recuperar informació històrica. Edicions in-place corrompen la traçabilitat.

**Intent:**  
Establir que tot engram és un fitxer `.engram.md` llegible per humans, amb metadades en JSON frontmatter (no YAML), immutable després de tancar-se (correccions via nou engram, no edit).

**Capa de memòria afectada:** **Episodic** (traça d'esdeveniments) + **Semantic** (coneixement general emmagatzemat).

**Contracts existents que toca:**
- `feat-003` (Engram Memory — partial overlap, estat unknown)
- `07_ENGRAM.mining.md` — defineix el format però no està clar si està implementat

**Risc principal:** Migració del corpus existent — cal backward compatibility.

---

### CAND-015 — Engram Index: SQLite FTS5 + WAL Mode

**Problema (2-4 línies):**  
Sense índex de cerca eficient, recuperar engrams rellevants és lent o impossible en hardware limitat. Canviar d'estratègia d'indexació constantment genera refactors cars.

**Intent:**  
Decisió estable: usar SQLite amb FTS5 (Full-Text Search) i WAL mode (Write-Ahead Logging) per lectures simultànies i crash safety. Índex global + potencialment índex per agent.

**Capa de memòria afectada:** **Episodic** + **Semantic** — com es cerca i es recupera la memòria persistent.

**Contracts existents que toca:**
- `feat-003` (Engram Memory — partial overlap, estat unknown)
- `03_FILESYSTEM_AND_DEPARTMENTS.mining.md` — menciona FTS5+WAL com a decisió de producte

**Risc principal:** Migracions de schema — cal mantenir estabilitat una vegada desplegat.

---

### CAND-016 — Librarian MCP Contract: memory_query + memory_store

**Problema (2-4 línies):**  
Sense contracte explícit entre Context Builder i Librarian, cada consumer inventa la seva API, generant drift i incompatibilitats. Crides bloquejants poden penjar el sistema.

**Intent:**  
Definir contracte MCP amb schema per `memory_query` i `memory_store`, timeout explícit (5s), i fallback determinista a `[]` si timeout o error.

**Capa de memòria afectada:** **Operational** — com es comuniquen components per accedir a memòria.

**Contracts existents que toca:**
- `feat-003` (Engram Memory) — menciona MCP però no detalla contracte
- `feat-008` (Context Builder) — consumeix aquest contracte
- No existeix feat específic només per aquest contracte

**Risc principal:** Drift de contracte — cal versionar i mantenir estable.

---

## Proposta de 5 Seeds per PKLot (futur)

*(Per sessió posterior de triage — NO aplicar ara)*

| CAND → Seed | Títol proposat | Per què val la pena |
|-------------|---------------|---------------------|
| **CAND-012** | "Context Budgets and Multi-Tier Hierarchy" | Fonamental per escalabilitat. Sense pressupostos, el sistema és vulnerable a OOM. Aquest seed definiría els límits abans que el context creixi. |
| **CAND-013** | "Context Segregation and Zero Trust Memory Access" | Drift-prone gap #1 del mining. La segregació IT/Sec és crítica per Zero Trust real. Afecta tots els futurs components de context. |
| **CAND-014** | "Engram File Format Contract v1" | La persistència de memòria necessita un format estable. Immutabilitat garanteix auditabilitat. Aquest seed bloquejaria el format abans de més drift. |
| **CAND-015** | "Engram Search Infrastructure — FTS5 + WAL" | Decisió d'infraestructura de cerca. Cal prendre-la abans d'implementar més funcionalitat de memòria. "Reserve now" per evitar canvis cars. |
| **CAND-016** | "Librarian MCP Interface Contract" | Contracte d'integració entre Context Builder i Librarian. Necessari per evitar drift d'API. Podria ser ADR en lloc de feature. |

**Nota:** Aquestes són propostes per a debat. Els IDs `SEED-XX` reals s'assignaran al triage batch, no ara.

---

## Open Questions per al Debat d'Arquitectura

### Q1 — Relació Working/Episodic
Com es decideix què va a Working (context immediat) vs què es persisteix a Episodic? Hi ha un "sliding window" explícit o és implícit?

### Q2 — Granularitat dels Engrams
Un engram = una acció/ticket, o pot ser agregat? Com es fa correlació entre engrams relacionats?

### Q3 — Segregació vs Performance
La segregació IT/Sec de CAND-013 implica filtrat de context a cada request. Quin és el cost de latència? Es pot cachejar?

### Q4 — Formats Competing
CAND-014 proposa JSON frontmatter. Hi ha alternativa YAML? Què passa si algú escriu YAML per error? Cal validador?

### Q5 — FTS5 vs Embeddings
CAND-015 aposta per FTS5. Quan consideraríem embeddings/vectors? Hi ha un camí de migració futur o són paradigmes incompatibles?

### Q6 — MCP vs REST
CAND-016 proposa MCP. Per què no REST/gRPC? Quins avantatges té MCP per al cas d'ús Librarian?

### Q7 — Immutabilitat Real
CAND-014 diu "immutable". Com es gestionen correccions d'errors? "Correcció via nou engram" = append-only log o històric separat?

### Q8 — Multi-Tenancy de Memòria
Els índexs FTS5 són per agent, per departament, o globals? Com es gestiona l'aïllament de memòria entre agents?

### Q9 — Retenció i TTL
Quant de temps es guarden els engrams? Hi ha política de TTL automàtica o és manual? Qui decideix què s'arxiu vs esborra?

### Q10 — Skills vs Prompts com a Memòria
Els skills (SDD) són "memòria semàntica" del sistema? Com es relacionen amb els engrams episòdics? Cal unificar vocabulari?

---

## External refs (inputs del debat)

- `00_project_documentation/external_refs/1_MEMORIA.md`
- `00_project_documentation/external_refs/2_Semantica.md`

---

## No Apply Confirmation

```
✅ No s'ha editat 00_project_documentation/04_PARKING_LOT.md
✅ No s'han creat fitxers SEED-*.md a seed_dossiers/
✅ No s'han creat feat-*.json nous
✅ Tots els proposed_seed_id = TBD (no assignats)
✅ Proposta de 5 seeds és només per a futura sessió de triage

Aquest document és preparació per al debat d'arquitectura de memòria.
Qualsevol aplicació al PKLot depèn d'un triage batch signat pel responsable.
```
