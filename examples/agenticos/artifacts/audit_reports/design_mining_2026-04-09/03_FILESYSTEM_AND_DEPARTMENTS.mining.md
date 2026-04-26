# Mining — `01_design/03_FILESYSTEM_AND_DEPARTMENTS.md` (legacy)

## Metadata
- Source: `01_design/03_FILESYSTEM_AND_DEPARTMENTS.md`
- Date: 2026-04-09
- Guiding question: Quines regles mínimes de filesystem/departaments necessitem perquè el Kernel, la seguretat i l’auditoria siguin coherents i no apareguin bypassos?

## A) Seeds desbloquejadores (Top 3)

- Seed: Contracte de layout per departament (estructura obligatòria)
  - Why it exists (risk): Sense estructura mínima, el Kernel no pot descobrir agents, skills i rutes de tickets de manera fiable.
  - What it unlocks: Bootstrapping de departaments, delegació i routing per filesystem.
  - Minimal contract: Cada departament té una estructura obligatòria (incloent `identity.md` i carpetes de tickets); el Kernel reconeix “agent vàlid” per aquest layout.
  - Cost to change later: Alt (migracions de disc i compatibilitat).
  - Evidence: “Cada departament ha de contenir obligatòriament…” (`03_FILESYSTEM_AND_DEPARTMENTS.md:232-233`).

- Seed: Boundary de seguretat de rutes (deny-by-default fora del directori permès)
  - Why it exists (risk): Si una eina pot escriure fora del seu “scope”, qualsevol agent pot mutar sistema/altres departaments ⇒ drift i compromís.
  - What it unlocks: Model Zero Trust real (enforçable pel Kernel/tools).
  - Minimal contract: Operacions natives de fitxers que intentin operar fora de la carpeta permesa es deneguen immediatament, excepte permisos explícits.
  - Cost to change later: Alt (seguretat, permisos, tool executor).
  - Evidence: “Qualsevol eina… que intenti operar fora… serà DENEGADA…” (`03_FILESYSTEM_AND_DEPARTMENTS.md:364-365`).

- Seed: Sistema de quarantena (tickets i engrames) amb registre i política de recuperació
  - Why it exists (risk): Sense quarantena, inputs corruptes o sospitosos entren al pipeline i contaminen memòria/auditoria.
  - What it unlocks: Recuperació segura, investigació, i protecció contra poisoning.
  - Minimal contract: Quarantena classifica per motiu/severitat, registra en `manifest.json`, i defineix què pot/NO pot auto-recuperar-se.
  - Cost to change later: Mitjà-alt.
  - Evidence: Secció “Sistema de Quarantena” (`03_FILESYSTEM_AND_DEPARTMENTS.md:488`) i “MAI recuperar automàticament” (`03_FILESYSTEM_AND_DEPARTMENTS.md:655-656`).

## B) Seeds importants però no crítiques (Top 5)

- Seed: “Zero pèrdua” com a principi (tickets no es perden)
  - Why it exists (risk): Pèrdua de tickets implica pèrdua d’auditoria i no determinisme.
  - What it unlocks: Garantia operacional i post-mortem.
  - Minimal contract: El sistema pot retardar o rebutjar, però no “perdre” silenciosament.
  - Cost to change later: Mitjà.
  - Evidence: “Els tickets mai es perden…” (`03_FILESYSTEM_AND_DEPARTMENTS.md:222`).

- Seed: `identity.md` com a font de contracte/permís per defecte (Kernel sempre el llegeix)
  - Why it exists (risk): Si el Kernel no té una font consistent d’identitat/permís, cada agent es comporta diferent.
  - What it unlocks: Enforcement de permisos i tooling visible.
  - Minimal contract: El Kernel llegeix `identity.md` del root; per subagents el ticket especifica el path complet.
  - Cost to change later: Mitjà-alt.
  - Evidence: “El Kernel sempre llegeix identity.md…” (`03_FILESYSTEM_AND_DEPARTMENTS.md:297-298`).

- Seed: Invariant d’assignació atòmica (“cap doble agafada” de ticket)
  - Why it exists (risk): Dues execucions simultànies del mateix ticket trenquen consistència i idempotència.
  - What it unlocks: Worker pool fiable, audit trail coherent.
  - Minimal contract: Dos workers mai poden agafar el mateix ticket a la vegada.
  - Cost to change later: Alt.
  - Evidence: “Dos Workers… mai poden agafar el mateix tiquet…” (`03_FILESYSTEM_AND_DEPARTMENTS.md:368-369`).

- Seed: `/archive` com a read-only (immutabilitat post-completat)
  - Why it exists (risk): Editar tickets arxivats trenca auditabilitat i memòria.
  - What it unlocks: Auditories i generació d’engrams fiables.
  - Minimal contract: Un cop a `/archive`, el ticket és només lectura.
  - Cost to change later: Mitjà.
  - Evidence: “Un cop un tiquet entra a /archive… Read-Only.” (`03_FILESYSTEM_AND_DEPARTMENTS.md:371-372`).

- Seed: Memòria via SQLite FTS5 + WAL (com a decisió de producte/infra)
  - Why it exists (risk): Solucions vectorials per defecte poden consumir RAM; sense decisió, es canvia d’estratègia constantment.
  - What it unlocks: Memòria eficient i consultable en hardware limitat.
  - Minimal contract: Motor SQLite amb FTS5 i WAL mode (lectures simultànies + crash recovery).
  - Cost to change later: Mitjà-alt.
  - Evidence: Descripció FTS5 + WAL i beneficis (`03_FILESYSTEM_AND_DEPARTMENTS.md:342-350`).

## C) No-seeds
- Referències a fitxers de codi Go (p.ex. `setup.go`, `main.go`) són implementació a contrastar, no seed (`03_FILESYSTEM_AND_DEPARTMENTS.md:4`).
- Mermaid detallat del workflow és explicatiu; el seed és el contracte de fases/estats, no el diagrama (`03_FILESYSTEM_AND_DEPARTMENTS.md:411-420`).

## D) Mapa d’implementacions (grosso modo)
- Layout de departaments (folders tickets/tools/skills) — UNKNOWN.
- Enforcement de “deny fora de carpeta” per fs_write/fs_delete/fs_move — UNKNOWN.
- Quarantine manager + manifest.json — UNKNOWN.
- Cleanup manager amb TTL + compaction — UNKNOWN (doc diu “Resolt v5”) (`03_FILESYSTEM_AND_DEPARTMENTS.md:1224`).
- Límit de mida per identity/tickets — UNKNOWN (doc diu “No especificat”) (`03_FILESYSTEM_AND_DEPARTMENTS.md:1223`).

