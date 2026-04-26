# Mining — `01_design/13_SECURITY_MODEL.md` (legacy)

## Metadata
- Source: `01_design/13_SECURITY_MODEL.md`
- Date: 2026-04-09
- Guiding question: Quines decisions mínimes de seguretat fan que “Zero Trust” sigui enforceable (modes, mediació, logs) i no una descripció aspiracional?

## A) Seeds desbloquejadores (Top 3)

- Seed: Kernel mediation (cap agent executa directament) + auditabilitat total
  - Why it exists (risk): Execució directa crea bypassos, accions no traçables i compromís.
  - What it unlocks: Seguretat i governança transversal.
  - Minimal contract: Totes les accions passen pel Kernel; el Kernel valida/executa/registra; l’humà manté control final.
  - Cost to change later: Alt.
  - Evidence: `13_SECURITY_MODEL.md:11`, `13_SECURITY_MODEL.md:12`, `13_SECURITY_MODEL.md:17`.

- Seed: Contracte de modes de seguretat (READ_ONLY/PROPOSE/EXECUTE_SAFE/FULL/SAFE_MODE/LOCKDOWN) + mode per defecte
  - Why it exists (risk): Sense modes, no hi ha control incremental ni postura per defecte; apareixen pegats per tool/feature.
  - What it unlocks: Operació segura i UX coherent (Telegram/IDE).
  - Minimal contract: Conjunt de modes amb descripció i “default mode” (READ_ONLY) que governa accions permeses.
  - Cost to change later: Alt.
  - Evidence: `13_SECURITY_MODEL.md:29`, `13_SECURITY_MODEL.md:31`, `13_SECURITY_MODEL.md:35`, `13_SECURITY_MODEL.md:36`.

- Seed: SAFE_MODE i LOCKDOWN com a mecanismes d’emergència (bloqueig d’eines + procediment de desactivació)
  - Why it exists (risk): Sense mecanismes d’emergència, una intrusió o bug pot continuar executant accions.
  - What it unlocks: Resposta a incidents.
  - Minimal contract: SAFE_MODE bloqueja totes les eines del Kernel i permet només lectura + notificació; LOCKDOWN bloqueja tot amb procediment/codi de sortida.
  - Cost to change later: Mitjà-alt.
  - Evidence: `13_SECURITY_MODEL.md:143`, `13_SECURITY_MODEL.md:187`, `13_SECURITY_MODEL.md:193`.

## B) Seeds importants però no crítiques (Top 5)

- Seed: Separació de poders (agents proposen, Kernel valida, humà decideix)
  - Why it exists (risk): Sense separació, l’agent pot prendre decisions de risc “end-to-end”.
  - What it unlocks: Governança clara.
  - Minimal contract: Propose pipeline explícit.
  - Cost to change later: Mitjà.
  - Evidence: `13_SECURITY_MODEL.md:18`.

- Seed: Permission Manager com a component central (gating per mode i permisos)
  - Why it exists (risk): Sense gating central, permisos deriven per feature.
  - What it unlocks: Coherència de permisos.
  - Minimal contract: Abans d’executar, el Kernel verifica mode i permisos; en PROPOSE genera una proposta amb comanda exacta.
  - Cost to change later: Mitjà.
  - Evidence: `13_SECURITY_MODEL.md:75`, `13_SECURITY_MODEL.md:76`.

- Seed: Mapping tool → required_mode + risk level com a contracte
  - Why it exists (risk): Sense mapping, cada eina acaba tenint “rules” ad hoc i drift de seguretat.
  - What it unlocks: Catàleg d’eines governat per modes.
  - Minimal contract: Cada eina defineix mode mínim; CRITICAL no s’executa automàticament en modes baixos.
  - Cost to change later: Mitjà.
  - Evidence: `13_SECURITY_MODEL.md:236`, `13_SECURITY_MODEL.md:239`, `13_SECURITY_MODEL.md:241`.

- Seed: Canvi de mode amb confirmació explícita (anti-accidents)
  - Why it exists (risk): Mode-switch accidental és un risc crític.
  - What it unlocks: Operació segura.
  - Minimal contract: Canvis de mode demanen confirmació i deixen rastre.
  - Cost to change later: Baix-mitjà.
  - Evidence: `13_SECURITY_MODEL.md:543`, `13_SECURITY_MODEL.md:544`, `13_SECURITY_MODEL.md:550`.

- Seed: Comandes d’auditoria com a API operativa (`/audit show/search/export`)
  - Why it exists (risk): Sense consulta/export, la “auditabilitat total” no és usable.
  - What it unlocks: Post-mortem i compliance.
  - Minimal contract: Comandes/funcionalitats mínimes per inspeccionar i exportar logs.
  - Cost to change later: Baix-mitjà.
  - Evidence: `13_SECURITY_MODEL.md:489`, `13_SECURITY_MODEL.md:490`, `13_SECURITY_MODEL.md:491`.

## C) No-seeds
- Vendor específic (Twilio/Home Assistant) és substituïble; el seed és “notificació d’emergència”, no el proveïdor.
- Codi Go d’exemple (ExecuteTool) és implementació; el seed és la semàntica dels modes/permisos.

## D) Mapa d’implementacions (grosso modo)
- Enforcement de modes + Permission Manager — UNKNOWN.
- SAFE_MODE/LOCKDOWN triggers + notificacions — UNKNOWN.
- Tool registry amb required_mode — UNKNOWN.
- Audit log + export/search — UNKNOWN.

