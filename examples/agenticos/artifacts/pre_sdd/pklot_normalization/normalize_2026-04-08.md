# PKLot normalization report — normalize_2026-04-08

date (UTC): 2026-04-08T20:46:46Z  
source: `00_project_documentation/04_PARKING_LOT.md`  

## 1) Proposed PKLot INDEX block

**NO CHANGE** — El bloc `INDEX + Invariants (OBLIGATORI)` existent és correcte.

## 2) Violations found

- CTX-02 i TLS-01 estan marcats `✅ Fet` dins `NOW backlog`: s’han de moure a ADR/CD i deixar el NOW backlog net.
- SEC-00 conté sub-items implementats (SEC-00A/SEC-00B/SEC-00B2/SEC-00C) que mereixen consolidació a ADR com a CD (agrupat).

## 3) Promotion candidates (ADR / CD / VOLATILE/KEEP)

| candidate | type | rationale | already_in_adr_log? |
|----------|------|-----------|---------------------|
| CTX-02 (Context-engine resilient fallback) | CD | Implementat; cal un CD formal per no deixar-ho com a nota dispersa. | mentioned (no CD) |
| TLS-01 (Normalitzar aliases de tools) | CD | Implementat/absorvit; cal un CD formal que fixi la convenció canònica. | mentioned (no CD) |
| SEC-00 baseline hardening (SEC-00A/B/B2/C) | CD | Implementat (segons ADR log + PKLot); consolidar com a un CD únic. | mentioned (no CD) |
| Models disponibles a OpenCode.ai | VOLATILE/KEEP | Snapshot datat; canvia amb el temps. | yes (as volatile snapshot in PKLot) |

## 4) Proposed physical reordering plan

- Eliminar `CTX-02` i `TLS-01` del `NOW backlog` (deixar-los com a links a CD).
- Afegir a `NOW backlog` una nota “Completed (see ADR)” amb links a CD-020 i CD-021.
- No tocar seeds ni horizons en aquest batch.

## 5) Notes / ambiguities

- `TLS-01` està descrit com “absorbit” (no com a feature independent). El CD l’ha de descriure com a decisió operativa: convenció canònica d’alias/noms, no com una feature nova.
- Evitar micro-CD per `SEC-00A/B/...`: consolidar en un CD global (CD-022).

