# Mining — `01_design/10_OBSERVABILITY.md` (legacy)

## Metadata
- Source: `01_design/10_OBSERVABILITY.md`
- Date: 2026-04-09
- Guiding question: Quines decisions mínimes d’observabilitat i accés remot eviten drift entre UI/operació/seguretat i fan el sistema operable sense obrir forats?

## A) Seeds desbloquejadores (Top 3)

- Seed: “MAI exposat a internet” + accés remot via VPN (decisió de producte/seguretat)
  - Why it exists (risk): Obrir ports públics converteix el sistema en superfície d’atac permanent i força pegats reactius.
  - What it unlocks: Postura de seguretat coherent i operació remota segura.
  - Minimal contract: AgenticOS no s’exposa directament a internet; l’accés remot passa per VPN (Tailscale/WireGuard).
  - Cost to change later: Alt.
  - Evidence: `10_OBSERVABILITY.md:216`, `10_OBSERVABILITY.md:217`, `10_OBSERVABILITY.md:734`.

- Seed: Aïllament del chat/UI (cap accés directe a shell o filesystem)
  - Why it exists (risk): Si el chat pot tocar shell/fs, és bypass del Kernel (RCE) i trenca auditabilitat.
  - What it unlocks: Seguretat de la capa d’interfície.
  - Minimal contract: El chat és només interfície; no té accés directe a shell/fs.
  - Cost to change later: Alt.
  - Evidence: `10_OBSERVABILITY.md:224`.

- Seed: Contracte d’events en temps real + reconnexió amb backoff exponencial
  - Why it exists (risk): Sense event types i reconnect, el dashboard deriva i el diagnòstic es torna inconsistent.
  - What it unlocks: UI robusta i telemetria consistent.
  - Minimal contract: Event types mínims (p.ex. `agent_log`, `metrics_update`) i comportament de reconnexió/backoff al client.
  - Cost to change later: Mitjà.
  - Evidence: `10_OBSERVABILITY.md:578`, `10_OBSERVABILITY.md:579`, `10_OBSERVABILITY.md:619`.

## B) Seeds importants però no crítiques (Top 5)

- Seed: TUI via SSH com a fallback operatiu robust
  - Why it exists (risk): Dependència exclusiva del web fa l’operació fràgil quan cau HTTP/UI.
  - What it unlocks: Operació de manteniment en emergència.
  - Minimal contract: Existeix un canal TUI via SSH amb funcionalitats mínimes d’admin.
  - Cost to change later: Mitjà.
  - Evidence: `10_OBSERVABILITY.md:504`, `10_OBSERVABILITY.md:512`.

- Seed: Kill Switch / aprovació de mutacions des de la interfície
  - Why it exists (risk): Sense mecanisme central, mutacions perilloses poden passar sense control.
  - What it unlocks: Governança i seguretat en operació.
  - Minimal contract: La interfície permet aprovar/rebutjar mutacions (o activar bloqueig).
  - Cost to change later: Mitjà.
  - Evidence: `10_OBSERVABILITY.md:108`, `10_OBSERVABILITY.md:508`.

- Seed: Auditories com a primitives operatives (`/audit`, `/audit-deep`, outputs a `SDD/audit_reports/`)
  - Why it exists (risk): Sense audit com a output, la veritat deriva entre spec/codi i no hi ha rutina de control.
  - What it unlocks: Qualitat i governança post-verify.
  - Minimal contract: Comandes d’audit existents i ubicació canònica d’informes.
  - Cost to change later: Mitjà.
  - Evidence: `10_OBSERVABILITY.md:764`, `10_OBSERVABILITY.md:767`, `10_OBSERVABILITY.md:786`.

- Seed: Mermaid “només documentació/exports”, no UI (decisió de producte)
  - Why it exists (risk): Si es barreja Mermaid com a UI, la UI es degrada i es fan hacks que deriven.
  - What it unlocks: Direcció clara del producte (UI interactiva vs documentació).
  - Minimal contract: Mermaid s’usa per documentació; UI real-time és una altra tecnologia.
  - Cost to change later: Mitjà.
  - Evidence: `10_OBSERVABILITY.md:77`, `10_OBSERVABILITY.md:79`.

- Seed: Separació “només per departaments, mai per Kernel” en certs mecanismes
  - Why it exists (risk): Barrejar responsabilitats pot fer el Kernel fràgil i difícil de mantenir.
  - What it unlocks: Mantenibilitat del core.
  - Minimal contract: Regla explícita de què és departamental vs core.
  - Cost to change later: Mitjà.
  - Evidence: `10_OBSERVABILITY.md:781`.

## C) No-seeds
- Llistes de connectors (email, n8n, etc.) són idees/product backlog, no contracte mínim.
- Detalls de pantalles/tecles de TUI són implementació/UX, no seed.

## D) Mapa d’implementacions (grosso modo)
- Event stream + event types + reconnect/backoff — UNKNOWN.
- Kill switch / sistema d’aprovacions — UNKNOWN.
- TUI via SSH — UNKNOWN.
- Comandes `/audit` i generació d’informes — UNKNOWN.

