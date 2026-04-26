# Mining — `01_design/TICKET_RUNTIME_TRANSITIONS_MINIMUM.md` (legacy “minimum runtime contract”)

## Metadata
- Source: `01_design/TICKET_RUNTIME_TRANSITIONS_MINIMUM.md`
- Date: 2026-04-09
- Guiding question: Quina és la mínima màquina d’estats i precedència d’autoritat que evita drift entre docs, spec i implementació del ticket runtime?

## A) Seeds desbloquejadores (Top 3)

- Seed: Llista d’autoritat (precedència de fonts) com a contracte de governança
  - Why it exists (risk): Si no hi ha precedència, conviuen contractes incompatibles i el sistema deriva.
  - What it unlocks: Resolució de conflictes doc↔codi i control de drift.
  - Minimal contract: Quan hi ha conflicte, mana la llista d’autoritat; aquest document pot ser “wrong” i s’ha d’actualitzar.
  - Cost to change later: Mitjà.
  - Evidence: `TICKET_RUNTIME_TRANSITIONS_MINIMUM.md:5`, `TICKET_RUNTIME_TRANSITIONS_MINIMUM.md:19`.

- Seed: Estat mínim + mapatge state → ubicació filesystem
  - Why it exists (risk): Sense mapatge, operació/recovery i tooling no són consistents.
  - What it unlocks: Inspecció i operació coherents.
  - Minimal contract: Taula de states mínims amb significat i folder canònic.
  - Cost to change later: Mitjà-alt.
  - Evidence: `TICKET_RUNTIME_TRANSITIONS_MINIMUM.md:25`.

- Seed: Matriu mínima de transicions + semàntica Router (`Acquire/Transition/Fail/Complete`)
  - Why it exists (risk): Sense transicions canòniques, apareixen estats impossibles i implementacions divergents.
  - What it unlocks: Router determinista i arxiu consistent d’errors/èxits.
  - Minimal contract: Transicions permeses mínimes i efectes; el Router persisteix l’estat de manera consistent.
  - Cost to change later: Alt.
  - Evidence: `TICKET_RUNTIME_TRANSITIONS_MINIMUM.md:36`, `TICKET_RUNTIME_TRANSITIONS_MINIMUM.md:48`, `TICKET_RUNTIME_TRANSITIONS_MINIMUM.md:53`.

## B) Seeds importants però no crítiques (Top 5)

- Seed: Set mínim de codis d’error compartits (semàntica base)
  - Why it exists (risk): Codis d’error inconsistents trenquen retries/observabilitat.
  - What it unlocks: Diagnòstic coherent.
  - Minimal contract: Codis d’error mínims i significat estable.
  - Cost to change later: Mitjà.
  - Evidence: `TICKET_RUNTIME_TRANSITIONS_MINIMUM.md:83`, `TICKET_RUNTIME_TRANSITIONS_MINIMUM.md:84`.

- Seed: “Runtime path of truth” explícit (Router del Kernel)
  - Why it exists (risk): Contracte “mínim” sense un lloc d’implementació canònic deriva.
  - What it unlocks: Alignament implementació↔contracte.
  - Minimal contract: El runtime mínim ha de correspondre amb el Router canònic.
  - Cost to change later: Mitjà.
  - Evidence: `TICKET_RUNTIME_TRANSITIONS_MINIMUM.md:8`.

## C) No-seeds
- Enumeracions “non-exhaustive” són guies; el seed és la precedència d’autoritat i la matriu mínima.

## D) Mapa d’implementacions (grosso modo)
- Router amb `AcquireTicket/TransitionTicket/FailTicket/CompleteTicket` — UNKNOWN.
- Enforcement state→folder — UNKNOWN.
- Error codes mínims — UNKNOWN.

