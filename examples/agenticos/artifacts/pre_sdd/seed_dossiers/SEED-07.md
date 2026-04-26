# SEED-07 — LLM Proxy hardening + capability study post-LiteLLM

> Dossier v1 — migrated from free-form notes

Note: two blocks (`Inspiració externa…` and `Tall operatiu…`) were duplicated/mispositioned in the PKLot (they appeared after `SEED-08`). They are consolidated here as the durable reference.

---

## Dades de referència (del PKLot)

- **ID:** `SEED-07`
- **Títol:** LLM Proxy hardening + capability study post-LiteLLM
- **Trigger:** Revisió del proxy propi després d'abandonar LiteLLM per risc de compromís extern
- **Idea:** Contrastar de manera estructurada el proxy propi actual amb les capacitats de valor afegit de LiteLLM per decidir quines funcions realment aporten robustesa a AgenticOS i quines serien sobreenginyeria o risc innecessari.
- **Impacte potencial:** `workflow` / `context` / `all`
- **Risc de drift:** `mitjà`
- **Horizon:** `NEXT`
- **Estat (PRE-SDD):** `Explored` (dossier complet, ready per triage)
- **Batch ref:** triage_2026-04-09
- **Destí probable:** `feat-028`

---

## problem

El proxy propi (feat-002) té nucli funcional però li falten rails i capacitats (routing/resiliència/governança/auth) que abans s'estudiaven via LiteLLM. Sense hardening, el proxy és vulnerable a errors de providers, no té control de cost, i no pot fer fallback intel·ligent.

## intent

Definir i implementar hardening del proxy que aporti robustesa sense sobreenginyeria enterprise, alineat amb local-first + Zero Trust.

## scope_in

- Retries/cooldowns cap a providers
- Fallback automàtic (p. ex. a Ollama) quan un provider cloud falla
- Rate limiting (per IP/per key)
- Spend tracking / budgets per provider
- Routing intel·ligent (least-busy, latency-based, etc.)
- Auth fina (virtual keys, JWT, ACLs, limits per request)

## scope_out

- Multi-tenant enterprise
- UI/CRUD de gestió de keys al dashboard
- Autodiscovery de models per provider (fora de scope aquí)

## capabilities

- El proxy ha de fer retry automàtic en errors 5xx del provider
- El proxy ha de tenir rate limiter actiu i traçable
- El spend per provider ha de estar registrat i consultable via API
- El proxy ha de fer fallback a Ollama quan provider cloud retorna error
- El proxy ha de suportar auth amb virtual keys i JWT

## approach

Contrastar amb LiteLLM com a catàleg de capacitats (no com a model a clonar). Prioritat: 1) routing/fallbacks/retries, 2) tracking i budgets, 3) auth més fina. La motivació original per tenir proxy propi (reduir superfície d'atac) continua vigent. No reconstruir tota la complexitat de LiteLLM.

## risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| Scope creep cap a funcionalitat enterprise | High | Definir explícitament non-scope abans de triage |
| Dependència de feat-027 (provider contract) | Medium | Crear feat-028 DEPENDENT de feat-027 explícitament |
| Sobreenginyeria ("copiar LiteLLM") | Medium | Tenir present filosofia local-first i Zero Trust en cada decisió |

## success_signals

- [ ] El proxy aplica retry automàtic en errors 5xx del provider
- [ ] El rate limiter està actiu i traçable
- [ ] El spend per provider està registrat i consultable via API
- [ ] El fallback a Ollama funciona quan provider cloud falla
- [ ] Auth amb virtual keys i JWT funciona

## dependencies

- `feat-027` — Provider Connection Contract (existeix)
- `feat-002` — LLM Proxy (base, existeix)
- `feat-055` — Action Log (per traçabilitat de decisions de routing)

## exploration_required

**`false`** — reason: seed is well-understood, triage batch already processed (triage_2026-04-09)

### Exploration Notes (when required)

Not required — seed was already analyzed in triage_2026-04-09 batch. See triage_notes for analysis.

## entry_checklist

Before passing to triage, verify ALL:

- [x] `problem` is clear and non-circular
- [x] `intent` describes outcome, not solution
- [x] `scope_in` and `scope_out` are explicit and not empty
- [x] `capabilities` are testable (observable outcomes)
- [x] `approach` references existing patterns/artifacts where possible
- [x] Risks have severity and mitigation
- [x] `exploration_required` is set with reason if true
- [x] All dependencies reference existing artifacts (feat-027, feat-002)
- [x] Entry checklist is complete

---

## triage_notes

**Anàlisi inicial**: El proxy actual cobreix bé el nucli mínim: endpoint OpenAI-compatible de `chat/completions`, selecció de proveïdor, health bàsic, autenticació local opcional i timeout controlat. També existeixen peces útils fora del binari del proxy: monitor de salut de providers, configuració multi-provider al dashboard i fallback cap a Ollama en parts del backend.

**Tall operatiu per a MVP**:
- **Implementació/config directa:** alta de nous providers compatibles amb el client actual, ampliació manual de `models`, ús de models free d'un provider existent dins del kernel, millores internes de logging/health que no alterin contracte extern.
- **Candidat clar a spec:** retries/fallbacks/cooldowns oficials, rate limiting real, spend/budgets, auth fina.

**Prioritat pràctica suggerida**: 1) afegir provider `minimax` si és compatible, 2) ampliar `zen` amb models free, 3) només després estudiar `autodiscovery` com a comportament nou.

---

## batch_handoff

| Date | Batch | Decision | Feature Record |
|------|-------|----------|----------------|
| 2026-04-09 | triage_2026-04-09 | `Adopted` | `feat-028-llm-proxy-hardening.json` |