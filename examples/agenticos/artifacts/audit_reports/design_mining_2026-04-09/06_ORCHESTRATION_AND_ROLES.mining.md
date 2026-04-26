# Mining — `01_design/06_ORCHESTRATION_AND_ROLES.md` (legacy)

## Metadata
- Source: `01_design/06_ORCHESTRATION_AND_ROLES.md`
- Date: 2026-04-09
- Guiding question: Quines regles mínimes de delegació, aprovació i orquestració eviten bucles, pèrdua d’auditoria i “protocols” informals entre agents?

## A) Seeds desbloquejadores (Top 3)

- Seed: Delegació asíncrona basada en tickets (ticket_create + callback)
  - Why it exists (risk): Comunicació directa o ad hoc trenca auditabilitat i recuperació després de falles.
  - What it unlocks: Escala organitzativa (subagents), traçabilitat i tolerància a errors.
  - Minimal contract: Una delegació crea un sub-ticket al `inbox` del departament B; el retorn és un ticket de resposta al departament A; cada delegació és un ticket independent.
  - Cost to change later: Alt.
  - Evidence: Flux amb `ticket_create` i retorn (`06_ORCHESTRATION_AND_ROLES.md:49-55`) + “Auditoria Perfecta” (`06_ORCHESTRATION_AND_ROLES.md:61-62`).

- Seed: Límit de profunditat de delegació (anti-bucle)
  - Why it exists (risk): Delegacions recursives poden generar bucles i allaus.
  - What it unlocks: Estabilitat del sistema i control de recursos.
  - Minimal contract: Existeix un màxim de profunditat; si es supera, es denega automàticament.
  - Cost to change later: Mitjà.
  - Evidence: “Si sub-ticket supera profunditat, es denega automàticament.” (`06_ORCHESTRATION_AND_ROLES.md:65-66`).

- Seed: Aprovació humana com a estat i artefacte (`REQUIRES_HUMAN` + `.approval.json`)
  - Why it exists (risk): HITL informal crea drift i impossibilita auditories consistents.
  - What it unlocks: UX coherent (dashboard/telegram), governança de canvis.
  - Minimal contract: El ticket entra a un estat d’espera d’humà i es genera un `.approval.json` amb la sol·licitud.
  - Cost to change later: Mitjà-alt.
  - Evidence: “Ticket passa a REQUIRES_HUMAN… Kernel genera .approval.json” (`06_ORCHESTRATION_AND_ROLES.md:144-145`).

## B) Seeds importants però no crítiques (Top 5)

- Seed: Selecció JIT de skills (scan + assemble) per ticket
  - Why it exists (risk): Injectar totes les skills sempre fa el context inmanejable.
  - What it unlocks: Context builder eficient i determinista.
  - Minimal contract: El Kernel/Context Builder escaneja rutes de skills i selecciona JIT les necessàries per la tasca.
  - Cost to change later: Mitjà.
  - Evidence: “Context Builder… selecció JIT… Escaneig…” (`06_ORCHESTRATION_AND_ROLES.md:151-152`).

- Seed: Límit de mida de skills injectades (pressupost en bytes)
  - Why it exists (risk): Sense límit, el prompt creix i causa OOM / degradació.
  - What it unlocks: Estabilitat en hardware limitat.
  - Minimal contract: Si la suma de bytes supera un llindar, es rebutja el ticket o es degrada.
  - Cost to change later: Mitjà.
  - Evidence: “Si la suma de bytes dels skills supera 8KB, es rebutja el ticket.” (`06_ORCHESTRATION_AND_ROLES.md:86-87`).

- Seed: “Tolerància a errors” via tickets (notificació de falles)
  - Why it exists (risk): Errors silenciosos creen drift i bloquejos.
  - What it unlocks: Resiliència en orquestració.
  - Minimal contract: L’agent que falla retorna via ticket (error) al delegador.
  - Cost to change later: Baix-mitjà.
  - Evidence: “Si Agent B falla, pot notificar Agent A via ticket.” (`06_ORCHESTRATION_AND_ROLES.md:60-61`).

- Seed: Pausa/continuació del delegador mentre espera sub-ticket
  - Why it exists (risk): Bloqueig de workers o execució duplicada.
  - What it unlocks: Concurrència estable i UX.
  - Minimal contract: El delegador marca tasca com delegada i reprèn quan rep resposta.
  - Cost to change later: Mitjà.
  - Evidence: “marca… delegada (pausa)… rep… i continua” (`06_ORCHESTRATION_AND_ROLES.md:52-55`).

- Seed: “Auditoria perfecta” com a invariant de delegació
  - Why it exists (risk): Delegació sense traça impedeix compliance.
  - What it unlocks: Auditoria sistemàtica del sistema multi-agent.
  - Minimal contract: Cada delegació és un ticket independent arxivable.
  - Cost to change later: Mitjà.
  - Evidence: “Cada delegació és un ticket independent.” (`06_ORCHESTRATION_AND_ROLES.md:61-62`).

## C) No-seeds
- Exemples de converses o flows narratius són explicatius, no contractes.

## D) Mapa d’implementacions (grosso modo)
- `ticket_create` i callback per delegació — UNKNOWN.
- Enforcement de límit de profunditat — UNKNOWN.
- Generació de `.approval.json` i estat REQUIRES_HUMAN — UNKNOWN.
- Selecció JIT de skills i límit 8KB — UNKNOWN.

