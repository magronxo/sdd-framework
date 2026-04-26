# Mining — `01_design/01_KERNEL.md` (legacy)

## Metadata
- Source: `01_design/01_KERNEL.md`
- Date: 2026-04-09
- Guiding question: Quines garanties mínimes ha de donar el Kernel perquè el sistema sigui determinista, recuperable de fallades i estable sota càrrega, sense “pegats” locals per feature?

## A) Seeds desbloquejadores (Top 3)

- Seed: Contracte de persistència d’estat del Kernel + Crash Recovery
  - Why it exists (risk): Sense una font d’estat persistent i una seqüència de recovery definida, apareixen tickets orfes, dobles execucions o pèrdua d’auditoria després de crash (OOM/kill -9/pànic).
  - What it unlocks: Robustesa del runtime (restarts segurs), invariants del pipeline, coherència d’observabilitat/auditoria post-crash.
  - Minimal contract: Existeix un fitxer d’estat persistent (`kernel.state.json`) amb heartbeat periòdic; el boot fa detecció d’instància prèvia i recupera tickets actius/orfes re-enrutant-los de forma segura.
  - Cost to change later: Alt (canvia semàntica de recovery, migració de camps, compatibilitat amb arxius existents).
  - Evidence: El doc descriu heartbeat i criteri de crash (`last_heartbeat`) i defineix ubicació/recuperació (p.ex. `01_KERNEL.md:137-139`, `01_KERNEL.md:2692`, `01_KERNEL.md:2784-2786`).

- Seed: Contracte de control de càrrega (Load Balancer) + spool/delay/reject
  - Why it exists (risk): Sense llindars i decisions deterministes, el sistema entra en allau (OOM, loadavg fora de control), i cada feature acaba implementant “rate limit” propi.
  - What it unlocks: Execució estable en hardware limitat, política única de backpressure per tots els departaments.
  - Minimal contract: El Kernel monitoritza mètriques i decideix Allow/Delay/Spool/Reject amb llindars explícits; el spool és retard, no pèrdua.
  - Cost to change later: Alt (impacte transversal: scheduling, latències, UX i errors).
  - Evidence: Definició de Load Balancer i decisió segons càrrega (`01_KERNEL.md:64-65`, `01_KERNEL.md:269-270`) i llindars resumits (`01_KERNEL.md:2889`).

- Seed: Contracte d’execució d’eines (exit codes + timeouts) com a part del pipeline
  - Why it exists (risk): Sense un “vocabulari” d’errors/timeout consistent, els errors es propaguen incoherents i s’acaben fent pegats per cada tool.
  - What it unlocks: Error taxonomy compartida amb tickets/guardian/observabilitat; recuperació i reintents consistents.
  - Minimal contract: Cada execució d’eina produeix un resultat normalitzat (exit_code, stdout/stderr, timeout/oom) amb mapping estable.
  - Cost to change later: Mitjà-alt (afecta historial d’execució i interpretació d’errors).
  - Evidence: Taula d’exit codes i exemples de timeout/OOM (`01_KERNEL.md:342-343`, `01_KERNEL.md:475-479`).

## B) Seeds importants però no crítiques (Top 5)

- Seed: Decisió “Pure Go” (Zero Python)
  - Why it exists (risk): Barreges runtime (Go+Python) acostumen a crear punts de fallada, tooling inconsistent i dependències que deriven.
  - What it unlocks: Simplicitat operacional, build/release determinista, menys superfície d’atac.
  - Minimal contract: El runtime del Kernel i components core són en Go; scripts poden existir però no governen el runtime.
  - Cost to change later: Alt (ecosistema, tooling, deploy).
  - Evidence: Secció “Decisió 'Pure Go' (Zero Python)” (`01_KERNEL.md:2.3`).

- Seed: Worker Pool fix com a invariant de concurrència
  - Why it exists (risk): Crear goroutines il·limitades per ticket trenca el control de càrrega.
  - What it unlocks: Scheduling determinista i integració neta amb load balancer.
  - Minimal contract: Nombre de workers limitat i controlat; el Kernel no “spawn” infinit per ticket.
  - Cost to change later: Mitjà-alt.
  - Evidence: “Worker Pool fix… garanteix que el Load Average…” (`01_KERNEL.md:270`).

- Seed: Semàfor d’inferència + circuit breaker / mode degradat
  - Why it exists (risk): Inferència local simultània pot saturar RAM/CPU i bloquejar el sistema.
  - What it unlocks: Degraded mode estable, protecció davant errors d’LLM/proxy.
  - Minimal contract: L’inferència passa per un limitador (semàfor) amb mecanisme de circuit breaker i una semàntica de “degradat”.
  - Cost to change later: Mitjà-alt.
  - Evidence: Secció “Semàfor d’Inferència Dinàmic amb Circuit Breaker” (`01_KERNEL.md:814-815`).

- Seed: Self-healing loop per errors de ticket/JSON (distinció de classes d’error)
  - Why it exists (risk): Sense diferenciació (sintaxi vs esquema), es fan reintents inútils o es deixa passar corrupció.
  - What it unlocks: Recuperació automàtica controlada, menys intervenció humana en errors trivials.
  - Minimal contract: Existeix un bucle de correcció per errors recuperables amb límits d’intents; errors d’esquema són terminals.
  - Cost to change later: Mitjà.
  - Evidence: Secció “Self-Healing JSON Loop” i “Distinció d’Errors JSON” (`01_KERNEL.md:3.4`).

- Seed: Autogeneració de documentació sota demanda (via ticket)
  - Why it exists (risk): Sense contracte d’autodoc, la documentació deriva i el sistema perd traçabilitat.
  - What it unlocks: Governança operativa (docs com a output), menys dependència de memòria humana.
  - Minimal contract: Hi ha un mecanisme (via ticket) per generar docs sota demanda humana.
  - Cost to change later: Mitjà.
  - Evidence: “Autogeneració documents sota demanda humana” (`01_KERNEL.md:2484`, `01_KERNEL.md:2892`).

## C) No-seeds
- Codi d’exemple “GitOps / immunology” (p.ex. `git commit`/`reset`) és implementació/estratègia, no contracte de runtime (`01_KERNEL.md:667-804`).
- Taules “IMPLEMENTAT/PENDent” són estat/notes; serveixen per mapatge, no per definir contractes (`01_KERNEL.md:2917-2933`).

## D) Mapa d’implementacions (grosso modo)
- Policy structures (`internal/kernel/policy.go`) — EXISTS (doc diu “IMPLEMENTAT/PASS”) (`01_KERNEL.md:2917`).
- Worker Pool (`internal/kernel/workerpool.go`) — EXISTS (doc diu “IMPLEMENTAT”) (`01_KERNEL.md:2918`).
- Load Balancer (`internal/kernel/loadbalancer.go`) — EXISTS (doc diu “IMPLEMENTAT”) (`01_KERNEL.md:2919`).
- WASM runtime (`internal/kernel/wasm.go`) — EXISTS (doc diu “IMPLEMENTAT”) (`01_KERNEL.md:2920`).
- Semàfor d’inferència (`internal/kernel/semaphore.go`) — UNKNOWN (doc marca pendent) (`01_KERNEL.md:2929`).
- Recovery Manager (`internal/kernel/recovery.go`) — UNKNOWN (doc marca pendent) (`01_KERNEL.md:2932`).

