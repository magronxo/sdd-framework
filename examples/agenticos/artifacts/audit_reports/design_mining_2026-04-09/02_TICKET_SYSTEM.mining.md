# Mining — `01_design/02_TICKET_SYSTEM.md` (legacy)

## Metadata
- Source: `01_design/02_TICKET_SYSTEM.md`
- Date: 2026-04-09
- Guiding question: Quines decisions/contractes mínims del ticket fan que el runtime sigui coherent (IPC, estat, auditoria, errors) i evitin que cada component inventi el seu “mini-protocol”?

## A) Seeds desbloquejadores (Top 3)

- Seed: Ticket com a únic contracte d’IPC + màquina d’estats “sobre disc”
  - Why it exists (risk): Si hi ha múltiples canals (REST/gRPC/queues) el sistema deriva i apareixen inconsistències d’estat i auditories incompletes.
  - What it unlocks: Delegació, auditoria, observabilitat i recovery coherents a tot el sistema.
  - Minimal contract: El `.ticket.json` és l’únic contracte intern; el ticket encapsula missatge+estat+audiència (auditoria) i es mou físicament (filesystem) amb semàntica d’estat.
  - Cost to change later: Alt (impacte global sobre tota comunicació interna).
  - Evidence: “El `.ticket.json` és l’únic contracte de comunicació… màquina d’estats que viatja físicament pel disc” (`02_TICKET_SYSTEM.md:27-28`).

- Seed: Atomicitat de transicions via “rename” i prohibició d’edició in-place
  - Why it exists (risk): Edició parcial/in-place crea corrupció i estats intermedis impossibles després de fallades elèctriques/crash.
  - What it unlocks: Crash safety i determinisme de transicions (i compatibilitat amb quarantena/recovery).
  - Minimal contract: El Kernel mai edita in-place; transicions i moviments són atòmics (p.ex. `os.Rename`).
  - Cost to change later: Alt.
  - Evidence: “El Kernel mai edita un ticket in-place… utilitza os.Rename” (`02_TICKET_SYSTEM.md:30`).

- Seed: Contracte estricte de JSON (schema) + quarantena a desviacions
  - Why it exists (risk): Sense validació estricte, el ticket es converteix en “bag of fields” i trenca compatibilitat.
  - What it unlocks: Interoperabilitat entre agents, auditories consistents, suport d’eines i UI.
  - Minimal contract: Existeix un esquema formal; qualsevol desviació provoca quarantena; camps core (request/audit/result/error/metadata) tenen semàntica estable.
  - Cost to change later: Alt (migracions i retrocompatibilitat).
  - Evidence: “El Kernel valida aquest esquema estricte. Qualsevol desviació provoca quarantena.” (`02_TICKET_SYSTEM.md:37-38`).

## B) Seeds importants però no crítiques (Top 5)

- Seed: Regla Anti-Bloat per outputs grans
  - Why it exists (risk): Tickets inflats trenquen memòria/IO, i afecten context builder i observabilitat.
  - What it unlocks: Estabilitat en hardware limitat i UX del sistema.
  - Minimal contract: Definició de quan un resultat s’externalitza a fitxer i què queda al ticket.
  - Cost to change later: Mitjà-alt.
  - Evidence: Secció “Regla Anti-Bloat” (`02_TICKET_SYSTEM.md:115-118`).

- Seed: Taxonomia d’errors + política de reintents per classe d’error
  - Why it exists (risk): Sense política de reintents, el sistema o bé spameja reintents o bé no es recupera de falles transitòries.
  - What it unlocks: Self-healing controlat, menys intervenció humana, coherència entre kernel/guardian/tools.
  - Minimal contract: Mapeig de codis d’error a “reintentar sí/no”, amb límits d’intents; errors d’esquema són terminals.
  - Cost to change later: Mitjà.
  - Evidence: Distinció `E_MALFORMED_INTENT` vs `E_INVALID_JSON` i taula de reintents (`02_TICKET_SYSTEM.md:1657-1666`).

- Seed: TTL / stale detection com a semàntica de “zombi”
  - Why it exists (risk): Tickets penjats generen drift, backlog i bloquejos operacionals.
  - What it unlocks: Neteja, quarantena, i UX consistent per falles/timeout.
  - Minimal contract: Ticket pot expirar; hi ha un codi d’error associat i semàntica de “no reintent” per expiració.
  - Cost to change later: Mitjà.
  - Evidence: Referències a `E_EXPIRED` i política de reintents “No” (`02_TICKET_SYSTEM.md:1677-1678`).

- Seed: “System mutation” com a categoria especial amb auditoria obligatòria
  - Why it exists (risk): Mutacions directes de sistema creen bypassos de seguretat i drift.
  - What it unlocks: Governança de canvis i traçabilitat.
  - Minimal contract: Definició clara de què és mutació vs no mutació; mutacions passen per un ticket auditat.
  - Cost to change later: Alt.
  - Evidence: Secció “Definició de System Mutation… HA de passar per ticket… amb auditoria” (`02_TICKET_SYSTEM.md:2.7`).

- Seed: `.approval.json` com a contracte d’aprovació humana
  - Why it exists (risk): HITL ad hoc trenca consistència i auditabilitat.
  - What it unlocks: UX coherent (dashboard/telegram), seguretat i “mode switching”.
  - Minimal contract: Existeix un format d’aprovació i un estat de ticket que el representa.
  - Cost to change later: Mitjà-alt.
  - Evidence: Secció “Contracte d’Aprovació (`.approval.json`)” (`02_TICKET_SYSTEM.md:2013-2014`).

## C) No-seeds
- “Implementació Go (notes breus) / codi d’exemple” és implementació, no contracte (secció 6).
- Optimitzacions opcionals (p.ex. “Preemptive scheduling”) són tuning/roadmap, no seeds.

## D) Mapa d’implementacions (grosso modo)
- Validador de ticket contra JSON schema — UNKNOWN (doc diu que existeix; estat real no confirmat).
- Moviments atòmics via rename — UNKNOWN.
- Quarantena per desviacions d’esquema — UNKNOWN.
- Sistema d’errors + reintents (classe d’error) — UNKNOWN.
- TTL/stale detection — UNKNOWN.
- `.approval.json` generation/consumption — UNKNOWN.
- Priority queue/spool segons priority — UNKNOWN (doc marca “pendent” en estat d’implementació) (`02_TICKET_SYSTEM.md:2088-2089`).

