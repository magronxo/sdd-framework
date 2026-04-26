# Mining — `01_design/11_DASHBOARD_IDE.md` (legacy)

## Metadata
- Source: `01_design/11_DASHBOARD_IDE.md`
- Date: 2026-04-09
- Guiding question: Quines decisions mínimes fan que l’IDE sigui útil (dev+ops) però sense comprometre Ring 0 ni generar drift fora de SDD?

## A) Seeds desbloquejadores (Top 3)

- Seed: Límits d’autoritat — Kernel/Ring 0 immutable; IDE només pot modificar Ring 1+
  - Why it exists (risk): Si la UI pot tocar Ring 0, la seguretat i governança col·lapsen.
  - What it unlocks: Evolució del producte sense comprometre el core.
  - Minimal contract: Ring 0/Kernel roman immutable i “extern”; l’IDE no pot modificar Ring 0.
  - Cost to change later: Alt.
  - Evidence: `11_DASHBOARD_IDE.md:22`.

- Seed: IDE com a frontend del workflow SDD (Plan → test → audit) (decisió de producte)
  - Why it exists (risk): Sense loop governat, l’IDE es converteix en un editor lliure i incrementa drift.
  - What it unlocks: Traçabilitat i qualitat (test/audit integrats).
  - Minimal contract: L’IDE reflecteix “Mode Plan” i integra comandes/fluxos d’audit.
  - Cost to change later: Mitjà.
  - Evidence: `11_DASHBOARD_IDE.md:162`, `11_DASHBOARD_IDE.md:165`, `11_DASHBOARD_IDE.md:172`.

- Seed: Integració via canals controlats (WS/REST) en lloc d’accés directe
  - Why it exists (risk): Accés directe a shell/fs des d’UI seria bypass del Kernel.
  - What it unlocks: UI segura i observable.
  - Minimal contract: Components UI consumeixen WS/REST autenticats per operar amb el sistema.
  - Cost to change later: Mitjà-alt.
  - Evidence: `11_DASHBOARD_IDE.md:84`, `11_DASHBOARD_IDE.md:85`, `11_DASHBOARD_IDE.md:86`.

## B) Seeds importants però no crítiques (Top 5)

- Seed: Stack tecnològic baseline (React/TS/Tailwind/Zustand/Monaco/ReactFlow) com a decisió explícita
  - Why it exists (risk): Canvis de stack constants maten el producte i fragmenten el codi.
  - What it unlocks: Coherència d’UI i velocitat d’iteració.
  - Minimal contract: Stack definit com a baseline de producte.
  - Cost to change later: Mitjà.
  - Evidence: `11_DASHBOARD_IDE.md:9`, `11_DASHBOARD_IDE.md:52`, `11_DASHBOARD_IDE.md:58`.

- Seed: Ubicació canònica del projecte IDE (contracte d’operació)
  - Why it exists (risk): Tooling/build/deploy deriven si la ubicació canvia sense governança.
  - What it unlocks: Build i deploy repetibles.
  - Minimal contract: IDE viu a una ruta estable dins repo.
  - Cost to change later: Baix-mitjà.
  - Evidence: `11_DASHBOARD_IDE.md:4`.

- Seed: Estat global com a “slice” de producte (no només UI)
  - Why it exists (risk): Sense estat global, el graf/monitoring deriva i l’IDE perd fiabilitat.
  - What it unlocks: UX consistent i diagnòstic.
  - Minimal contract: Estat global persistent/consultable i un model de dades per UI.
  - Cost to change later: Mitjà.
  - Evidence: `11_DASHBOARD_IDE.md:93`.

- Seed: `/audit` com a feature de primera classe (no “nice-to-have”)
  - Why it exists (risk): Sense audit accessible, la UI incentiva canvis no governats.
  - What it unlocks: Quality loop.
  - Minimal contract: UI pot invocar audits i mostrar resultats.
  - Cost to change later: Mitjà.
  - Evidence: `11_DASHBOARD_IDE.md:165`, `11_DASHBOARD_IDE.md:172`.

- Seed: Coexistència IDE + altres canals (p.ex. SSH/TUI) com a principi d’operació
  - Why it exists (risk): Dependre d’una sola UI fa operació fràgil.
  - What it unlocks: Operació robusta.
  - Minimal contract: L’IDE és un canal, no l’únic.
  - Cost to change later: Mitjà.
  - Evidence: `11_DASHBOARD_IDE.md:4`.

## C) No-seeds
- Llistats de components TSX concrets són implementació.
- “Polish UI” i backlog d’UX són tasques, no seeds.

## D) Mapa d’implementacions (grosso modo)
- WS chat + REST endpoints — UNKNOWN.
- Integració `/audit` — UNKNOWN.
- Enforcement “IDE no pot mutar Ring 0” — UNKNOWN.

