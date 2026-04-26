# Mining — `01_design/05_GUARDIAN.md` (legacy)

## Metadata
- Source: `01_design/05_GUARDIAN.md`
- Date: 2026-04-09
- Guiding question: Quines decisions mínimes de seguretat (determinista vs semàntica, permisos, polítiques, HITL) eviten bypassos i pegats “per feature”?

## A) Seeds desbloquejadores (Top 3)

- Seed: Separació Fast-Path (Ring 0 determinista) vs Slow-Path (Guardian Ring 1 semàntic) + contracte d’escalada
  - Why it exists (risk): Barrejar decisió determinista i semàntica fa el sistema inconsistent i difícil d’auditar.
  - What it unlocks: Governança de seguretat escalable, rendiment en hardware limitat, i audit trail net.
  - Minimal contract: El Kernel fa validació determinista (FastAuditor); quan no pot decidir, escala al Guardian (Verifier Ring 1) via un contracte de ticket/timeout.
  - Cost to change later: Alt.
  - Evidence: “FastAuditor… resideix al Kernel… Guardian només rep escalades…” (`05_GUARDIAN.md:17-18`) i “Contracte d’Escalada… format de tickets i timeout” (`05_GUARDIAN.md:8-9`).

- Seed: Model de permisos “zero tools per defecte” + kernel-gating (capacitats)
  - Why it exists (risk): Si l’agent té eines per defecte o veu eines que no pot usar, hi ha superfície d’atac i drift.
  - What it unlocks: Seguretat i prompts més petits (zero-noise).
  - Minimal contract: Un agent neix amb zero eines; les eines/capacitats es concedeixen explícitament a `identity.md`; el Kernel amaga eines si manca capacitat.
  - Cost to change later: Alt.
  - Evidence: “Regla d’Or: Un agent neix amb Zero Eines… Kernel ni tan sols li mostra…” (`05_GUARDIAN.md:69-70`).

- Seed: Polítiques de seguretat com a dades (JSON) validades contra schema amb accions ALLOW/DENY/AUDIT
  - Why it exists (risk): Sense contracte de polítiques, hi ha decisions disperses i impossibles d’auditar.
  - What it unlocks: Enforcement consistent i “policy updates” sense recompilar.
  - Minimal contract: Política és JSON validat per schema; les regles decideixen ALLOW/DENY/AUDIT amb severitat; suport per shadow mode opcional.
  - Cost to change later: Mitjà-alt.
  - Evidence: Validació contra `policy.schema.json` (`05_GUARDIAN.md:266-267`) i enum d’accions (`05_GUARDIAN.md:297-298`).

## B) Seeds importants però no crítiques (Top 5)

- Seed: Blindfold pattern per secrets (agent no veu valor real)
  - Why it exists (risk): Exfiltració de secrets i prompt leakage.
  - What it unlocks: Seguretat operacional.
  - Minimal contract: Secrets no s’injecten en clar a agents; s’usen mecanismes indirectes.
  - Cost to change later: Mitjà.
  - Evidence: “Blindfold Pattern: L’agent MAI veu el valor real d’un secret.” (`05_GUARDIAN.md:23-24`).

- Seed: HITL per accions destructives/ambigües
  - Why it exists (risk): Execució automàtica d’accions destructives en entorns no deterministes.
  - What it unlocks: Seguretat i confiança.
  - Minimal contract: Hi ha un punt d’aprovació humana per accions d’alt risc.
  - Cost to change later: Mitjà.
  - Evidence: “Human-in-the-Loop: Per a accions destructives o ambigües.” (`05_GUARDIAN.md:24-25`).

- Seed: Fallback multi-nivell quan el Verifier (LLM) falla
  - Why it exists (risk): Timeouts/caigudes del LLM no poden bloquejar el sistema ni forçar decisions insegures.
  - What it unlocks: Disponibilitat i seguretat sota falles de proveïdor/model.
  - Minimal contract: Si Verifier falla, s’activa fallback (alt verifier/deterministic auditor/escalada humana) amb criteris.
  - Cost to change later: Mitjà.
  - Evidence: “Verifier pot fallar… Timeout…” (`05_GUARDIAN.md:1492-1494`) i ús de fallback (`05_GUARDIAN.md:1574-1575`).

- Seed: Separació audit.db (auditoria) vs engram.db (memòria)
  - Why it exists (risk): Barrejar logs d’auditoria i memòria contamina i trenca privacitat.
  - What it unlocks: Compartimentació de dades.
  - Minimal contract: Guardian manté una base pròpia d’auditories separada.
  - Cost to change later: Mitjà.
  - Evidence: `audit.db` i nota de renombrat (`05_GUARDIAN.md:48-55`).

- Seed: Criteri d’escalada “legal tècnicament però perillós semànticament”
  - Why it exists (risk): Si el Kernel només valida sintaxi/permís, es poden executar accions perilloses “legals”.
  - What it unlocks: Seguretat semàntica.
  - Minimal contract: Quan una acció és legal però perillosa, entra el Verifier.
  - Cost to change later: Mitjà.
  - Evidence: “tècnicament legal però semànticament perillosa” (`05_GUARDIAN.md:94-95`).

## C) No-seeds
- Referències a models concrets (Llama/GPT-4o) són implementació/infra substituïble, no contracte (`05_GUARDIAN.md:34-35`).
- Structs Go (monitor, shutdown, etc.) són implementació de referència.

## D) Mapa d’implementacions (grosso modo)
- FastAuditor al Kernel + escalada a Guardian — UNKNOWN (doc diu resolt v4/v5).
- Policy loader + schema validation — UNKNOWN.
- Fallback verifier + deterministic auditor + escalada humana — UNKNOWN.
- Monitor de salut + emergency shutdown — UNKNOWN.

