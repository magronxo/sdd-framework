# Mining — `01_design/04_SEED_AND_AGENT_ANATOMY.md` (legacy)

## Metadata
- Source: `01_design/04_SEED_AND_AGENT_ANATOMY.md`
- Date: 2026-04-09
- Guiding question: Quines decisions mínimes sobre “què és una seed” i “què és un agent” eviten drift (privilegis, identitats, eines) i fan el sistema governable?

## A) Seeds desbloquejadores (Top 3)

- Seed: Seed bootstrap (departaments fundacionals + rings) i immutabilitat de Ring 0
  - Why it exists (risk): Si Ring 0 és mutable per agents, la seguretat deriva i el sistema es pot autocomprometre.
  - What it unlocks: Seguretat, governança, i evolució segura de Ring 1+.
  - Minimal contract: La seed conté com a mínim `00_genesis` i `01_guardian`; existeix model d’anells; Ring 0 és immutable (no es pot mutar via agents).
  - Cost to change later: Alt.
  - Evidence: Definició de seed/rings i estructura (`04_SEED_AND_AGENT_ANATOMY.md:10-12`, `04_SEED_AND_AGENT_ANATOMY.md:35-42`) i “NO pot mutar Ring 0” (`04_SEED_AND_AGENT_ANATOMY.md:221-223`).

- Seed: Mutació d’identitats via ticket + auditoria (prohibició de bypass via inotify)
  - Why it exists (risk): Si identitats es poden editar “fora de canal”, es creen bypassos de seguretat i drift.
  - What it unlocks: Control de canvis, traçabilitat i enforcement real.
  - Minimal contract: Tota mutació d’identitat passa per un ticket de mutació amb auditoria; mecanismes de “watch/inotify” d’identitats no són via de mutació.
  - Cost to change later: Alt.
  - Evidence: “Eliminat mecanisme inotify… Tota mutació HA de passar per ticket SYSTEM_MUTATION amb auditoria” (`04_SEED_AND_AGENT_ANATOMY.md:265-266`).

- Seed: Model de permisos i descoberta d’eines (zero tools per defecte + discovery controlat)
  - Why it exists (risk): Si les eines “apareixen” sense contracte, l’agent pot executar accions no governades o el prompt creix fins a ser inusable.
  - What it unlocks: Tooling extensible i segur, i context builder estable.
  - Minimal contract: Agents neixen amb zero eines; les capacitats es concedeixen explícitament a `identity.md`; el Kernel descobreix eines dinàmiques escanejant rutes canòniques i les injecta.
  - Cost to change later: Mitjà-alt.
  - Evidence: “Descobreix Eines Dinàmiques… escaneja …” (`04_SEED_AND_AGENT_ANATOMY.md:236-238`) i principi de “Zero eines” (alineat amb Guardian).

## B) Seeds importants però no crítiques (Top 5)

- Seed: Només `00_genesis` pot modificar `identity.md` de Ring 1
  - Why it exists (risk): Auto-modificació d’identitat és drift immediat.
  - What it unlocks: Delegació segura de canvis (control plane humà/Genesis).
  - Minimal contract: El dret de mutar identitats Ring 1 és exclusiu de Genesis.
  - Cost to change later: Alt.
  - Evidence: “Només 00_genesis pot modificar identity.md…” (`04_SEED_AND_AGENT_ANATOMY.md:415-416`).

- Seed: Prohibició de modificar la pròpia identitat
  - Why it exists (risk): Self-escalation i drift de comportament.
  - What it unlocks: Seguretat i auditabilitat.
  - Minimal contract: Cap agent pot modificar la seva identitat.
  - Cost to change later: Alt.
  - Evidence: “NO pot modificar la seva pròpia identitat (evitar drift)” (`04_SEED_AND_AGENT_ANATOMY.md:222-223`).

- Seed: Versionat/snapshots d’identitats (mantenir mínim 2 versions + auto-cleanup)
  - Why it exists (risk): Sense versionat, no hi ha rollback segur de regressions d’identitat/polítiques.
  - What it unlocks: Rollback, auditoria, i estabilitat operativa.
  - Minimal contract: Versions completes en `/versions/`, límit de versions i política de retenció.
  - Cost to change later: Mitjà-alt.
  - Evidence: “Es manté sempre mínim 2 versions…” (`04_SEED_AND_AGENT_ANATOMY.md:384-385`) i “Snapshots… màxim 10… auto-cleanup” (`04_SEED_AND_AGENT_ANATOMY.md:416`).

- Seed: Contracte d’output de tool-calling (JSON determinista) per agents
  - Why it exists (risk): Respostes lliures trenquen parsing, auditoria i execució segura.
  - What it unlocks: Determinisme del bucle ReAct i del tool executor.
  - Minimal contract: L’agent produeix una estructura JSON estable que descriu `tool_name` i `tool_params`.
  - Cost to change later: Mitjà.
  - Evidence: “output ONLY valid JSON” i schema amb `tool_name`/`tool_params` (`04_SEED_AND_AGENT_ANATOMY.md:139-148`).

- Seed: Validacions del Kernel sobre origen/destí per ring en mutacions
  - Why it exists (risk): Mutacions sense checks creen escalació de privilegis.
  - What it unlocks: Enforcement de ring model.
  - Minimal contract: El Kernel valida que el ticket de mutació ve de Genesis i que el target és Ring 1.
  - Cost to change later: Mitjà-alt.
  - Evidence: “Kernel valida: Ticket ve de Genesis? Target és agent Ring 1?” (`04_SEED_AND_AGENT_ANATOMY.md:260-261`).

## C) No-seeds
- Llistats d’arbre de directoris són útils però no són el seed; el seed és l’invariant (què és obligatori i què és immutable).
- Detalls concrets de rutes d’executor/memory són implementació (mapatge a paquets).

## D) Mapa d’implementacions (grosso modo)
- Seed bootstrap amb `00_genesis` i `01_guardian` — UNKNOWN.
- Enforcement “Ring 0 immutable” al Kernel — UNKNOWN (doc diu “hardcoded”).
- Mutacions via `SYSTEM_MUTATION` + auditoria — UNKNOWN.
- Descoberta d’eines via escaneig de rutes — UNKNOWN.
- Versionat d’identitats — UNKNOWN.

