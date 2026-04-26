# PKLot normalization report — normalize_2026-04-12

date (UTC): 2026-04-12T18:30:00Z
source: `00_project_documentation/04_PARKING_LOT.md`
status: **APPLIED**

## Apply Actions

- [x] Renombrar MAN-01..MAN-08 (Manual) → DOC-01..DOC-08
- [x] Afegir camp Estat explícit a tots els items (tots ⬜ Pendent excepte DOC-08 MITJANA)
- [x] Verificar que HITL MAN-01..MAN-04 no afectats

## 1) Proposed PKLot INDEX block

**NO CHANGE** — El bloc INDEX + Invariants (OBLIGATORI) existent és correcte. La secció "Com capturar seeds (PKLot Seed v1)" afegida el 2026-04-12 (PRE-SDD-02) no trenca cap invariant.

## 2) Violations found

- **MAN-01..MAN-08 (Manual d'usuari)** a Deferred backlog — Aquests items tenen camp Estat buit (no apareix a la taula). L'esquema de tasques requereix `⬜/✅/📋`. A més, l'ID MAN-* col·lideix amb MAN-01..MAN-04 de la secció HITL (línia 317-324), que sí són funcionalitat real.

## 3) Promotion candidates (ADR / CD / VOLATILE/KEEP)

| candidate | type | rationale | already_in_adr_log? |
|----------|------|-----------|---------------------|
| Models disponibles a OpenCode.ai (Blockers) | VOLATILE/KEEP | Snapshot datat (2026-04-08); canvia amb el temps. No promoure a ADR/CD. | yes (as volatile snapshot) |
| Manual tasks (DOC-01..DOC-08) | KEEP | Tasques de documentació, no decisions. Mantenir com tasques ara que tenen schema correcte. | no |
| Futures (MULTI-01, MULTI-02, FUT-01, etc.) | KEEP | Exploració/estudi, no decisions consolidades. No promoure a ADR. | no |
| LLM Providers (LLM-05, LLM-07, LLM-08) | KEEP | backlog de feina, no decisions. El model híbrid ja documentat a CD-017. | yes (CD-017) |

**Conclusió**: No hi ha nous candidats a ADR/CD en aquest scan. L'últim normalization (2026-04-08) ja va promoure CTX-02, TLS-01, SEC-00 baseline.

## 4) Proposed physical reordering plan

- **Renombrar MAN-01..MAN-08 (Manual)** → DOC-01..DOC-08
- **Afegir camp Estat** (tots ⬜ Pendent excepte DOC-08 que és MITJANA)
- **No moure seccions** — l'ordre de secció és correcte
- **No tocar HITL MAN-01..MAN-04** — aquests sí tenen schema correcte

## 5) Notes / ambiguities

- El conflicto MAN-* entre HITL (funcionalitat) i Manual (documentació) era nominal, no estructural. Ara DOC-*区分 clearly.
- La secció "Manual d'usuari" podria viure al seu propi document (03_MANUAL.md) si creix molt, però ara no cal.
- El camp Estat de la taula Manual era absent abans (es mostrava buit); ara és explícit.