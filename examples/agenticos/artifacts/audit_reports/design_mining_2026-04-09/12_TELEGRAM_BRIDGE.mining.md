# Mining — `01_design/12_TELEGRAM_BRIDGE.md` (legacy)

## Metadata
- Source: `01_design/12_TELEGRAM_BRIDGE.md`
- Date: 2026-04-09
- Guiding question: Quines decisions mínimes fan que Telegram sigui un canal de control útil però segur (auth, modes, confirmacions, secrets) sense bypass del Kernel?

## A) Seeds desbloquejadores (Top 3)

- Seed: Secrets fora del git + permisos estrictes (chmod 600) per token/config
  - Why it exists (risk): Si el token s’exposa o té permisos febles, el canal queda compromès i es perd control del sistema.
  - What it unlocks: Operació segura del control plane mòbil.
  - Minimal contract: Tokens en fitxer de secrets fora del git; permisos `chmod 600`; config del bridge en path de sistema.
  - Cost to change later: Mitjà.
  - Evidence: `12_TELEGRAM_BRIDGE.md:274`, `12_TELEGRAM_BRIDGE.md:315`, `12_TELEGRAM_BRIDGE.md:319`, `12_TELEGRAM_BRIDGE.md:335`.

- Seed: Autenticació per whitelist de user_id + controls d’acció (confirmació/doble confirmació + keyword)
  - Why it exists (risk): Sense whitelist/confirmació, qualsevol filtració de token o error d’UX pot executar accions crítiques.
  - What it unlocks: Control de risc i traçabilitat d’accions remotes.
  - Minimal contract: Verificació user_id (whitelist) i protocol de confirmació (simple/doble + paraula clau) per accions crítiques.
  - Cost to change later: Mitjà.
  - Evidence: `12_TELEGRAM_BRIDGE.md:238`, `12_TELEGRAM_BRIDGE.md:265`, `12_TELEGRAM_BRIDGE.md:337`.

- Seed: Mode per defecte READ-ONLY (decisió de seguretat per defecte)
  - Why it exists (risk): Canal remot amb execució per defecte és un risc alt (compromís de compte/mòbil).
  - What it unlocks: Seguretat per defecte.
  - Minimal contract: Telegram opera en READ-ONLY per defecte; accions es rebutgen si el mode no ho permet.
  - Cost to change later: Mitjà.
  - Evidence: `12_TELEGRAM_BRIDGE.md:15`, `12_TELEGRAM_BRIDGE.md:106`, `12_TELEGRAM_BRIDGE.md:263`, `12_TELEGRAM_BRIDGE.md:336`.

## B) Seeds importants però no crítiques (Top 5)

- Seed: Rotació periòdica del token (p.ex. 90 dies) i resposta a compromís
  - Why it exists (risk): Tokens compromesos persisteixen; cal un protocol de rotació i resposta.
  - What it unlocks: Recuperació de seguretat.
  - Minimal contract: Política de rotació i accions immediates davant compromís.
  - Cost to change later: Baix-mitjà.
  - Evidence: `12_TELEGRAM_BRIDGE.md:351`.

- Seed: Timeout per confirmacions
  - Why it exists (risk): Confirmacions pendents poden quedar obertes i ser explotades.
  - What it unlocks: Seguretat i UX.
  - Minimal contract: Les confirmacions tenen TTL (p.ex. 30s).
  - Cost to change later: Baix.
  - Evidence: `12_TELEGRAM_BRIDGE.md:338`.

- Seed: Decisió sobre E2E (no E2E en grups) com a política d’ús del canal
  - Why it exists (risk): Assumir E2E quan no existeix crea falsa seguretat.
  - What it unlocks: Política clara d’ús.
  - Minimal contract: Restriccions/guia d’ús segons tipus de chat; considerar xats secrets si cal.
  - Cost to change later: Baix.
  - Evidence: `12_TELEGRAM_BRIDGE.md:344`, `12_TELEGRAM_BRIDGE.md:485`.

- Seed: Config canònica del bridge a `/etc/agenticos/telegram.json`
  - Why it exists (risk): Sense ubicació canònica, la configuració deriva.
  - What it unlocks: Operació repetible.
  - Minimal contract: Fitxer de config en path estable.
  - Cost to change later: Baix.
  - Evidence: `12_TELEGRAM_BRIDGE.md:274`.

- Seed: Mode-dependent behavior (READ-ONLY rebutja; FULL exigeix doble confirmació)
  - Why it exists (risk): Si el comportament per mode no és consistent, el canal es torna perillós.
  - What it unlocks: Control incremental de capacitats.
  - Minimal contract: Semàntica per mode definida i enforced.
  - Cost to change later: Mitjà.
  - Evidence: `12_TELEGRAM_BRIDGE.md:263`, `12_TELEGRAM_BRIDGE.md:265`.

## C) No-seeds
- Detalls de fitxers Go (bot.go, etc.) i dependències són implementació.
- Roadmap d’integracions (charts, etc.) és product backlog.

## D) Mapa d’implementacions (grosso modo)
- Config + secrets paths + permisos — UNKNOWN.
- Whitelist + confirmacions + keyword — UNKNOWN.
- Enforcement de mode READ-ONLY per defecte — UNKNOWN.

