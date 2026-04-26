# Mining — `01_design/14_MULTISEED_future.md` (future/legacy vision)

## Metadata
- Source: `01_design/14_MULTISEED_future.md`
- Date: 2026-04-09
- Guiding question: Quines decisions mínimes cal “reservar” ara perquè un futur multi-seed no obligui refactors caríssims ni canvis de contracte de tickets?

## A) Seeds desbloquejadores (Top 3)

- Seed: Gate de producte — multi-seed és `FUTURE` (no implementar fins single-seed estable)
  - Why it exists (risk): Implementar massa aviat dispersa el focus i crea deuda estructural.
  - What it unlocks: Roadmap i governança de direcció.
  - Minimal contract: Multi-seed només s’activa quan el core single-seed és estable; fins llavors és visió/prepare.
  - Cost to change later: Mitjà.
  - Evidence: `14_MULTISEED_future.md:7`.

- Seed: Definició de Seed com a unitat autònoma (Kernel + Agents + Memòria + Tools + Config)
  - Why it exists (risk): Sense definició, multi-seed deriva cap a “clúster” inconsistent i sense boundaries.
  - What it unlocks: Disseny de routing, seguretat i operació distribuïda.
  - Minimal contract: Una seed és una instància completa amb dades/config pròpies.
  - Cost to change later: Alt.
  - Evidence: `14_MULTISEED_future.md:23`, `14_MULTISEED_future.md:173`, `14_MULTISEED_future.md:175`.

- Seed: Interfície mínima `Seed` + Control Plane “coordina, no executa”
  - Why it exists (risk): Sense interfícies, el sistema s’acobla a un deployment i és difícil separar control/data plane.
  - What it unlocks: Routing i monitor de seeds heterogènies.
  - Minimal contract: Interfície `Seed` i rol del Control Plane amb responsabilitats limitades (coordinar).
  - Cost to change later: Alt.
  - Evidence: `14_MULTISEED_future.md:71`, `14_MULTISEED_future.md:82`, `14_MULTISEED_future.md:42`.

## B) Seeds importants però no crítiques (Top 5)

- Seed: Camps `source_seed` / `target_seed` al ticket (routing explícit)
  - Why it exists (risk): Sense routing explícit, cada integració inventa metadades i apareix drift.
  - What it unlocks: RPC via tickets entre seeds.
  - Minimal contract: Ticket pot expressar origen/destí seed.
  - Cost to change later: Mitjà-alt.
  - Evidence: `14_MULTISEED_future.md:99`, `14_MULTISEED_future.md:100`.

- Seed: Scopes/permisos per seed (contracte de seguretat distribuïda)
  - Why it exists (risk): Sense scopes, una seed pot operar fora del seu domini i es trenca seguretat.
  - What it unlocks: Control de capacitats per node/rol.
  - Minimal contract: Definir scopes i permisos associats en config.
  - Cost to change later: Alt.
  - Evidence: `14_MULTISEED_future.md:178`, `14_MULTISEED_future.md:183`.

- Seed: Separació de dades/memòria/config/secrets per seed
  - Why it exists (risk): Compartir memòria o secrets entre seeds crea fuga i risc sistemàtic.
  - What it unlocks: Aïllament i compliance.
  - Minimal contract: Cada seed té directori propi i secrets diferents.
  - Cost to change later: Alt.
  - Evidence: `14_MULTISEED_future.md:173`, `14_MULTISEED_future.md:175`.

- Seed: Control Plane permissions (operador vs client)
  - Why it exists (risk): Sense permissos, el control plane es converteix en superuser distribuït.
  - What it unlocks: Governança en entorns heterogenis.
  - Minimal contract: Permisos explícits de control plane i canals de report.
  - Cost to change later: Mitjà.
  - Evidence: `14_MULTISEED_future.md:189`, `14_MULTISEED_future.md:192`.

- Seed: Preparació mínima (config externalitzada, seed_id a config) com a prerequisits
  - Why it exists (risk): Sense això, multi-seed exigeix reescriure config/routing.
  - What it unlocks: “Multi-seed ready” incremental.
  - Minimal contract: Config externalitzada i suport per `seed_id`.
  - Cost to change later: Mitjà.
  - Evidence: `14_MULTISEED_future.md:118`, `14_MULTISEED_future.md:126`, `14_MULTISEED_future.md:234`.

## C) No-seeds
- TODO checklist de branch/tasks és implementació/roadmap, no contracte mínim (`14_MULTISEED_future.md:240`).

## D) Mapa d’implementacions (grosso modo)
- Interfície `Seed` al codi — UNKNOWN.
- Ticket routing `target_seed` — UNKNOWN.
- Control Plane (registry+routing) — UNKNOWN.
- Config `seed_id` + scopes — UNKNOWN.

