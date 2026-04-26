# AUDIT — feat-028: LLM Proxy Hardening (REAUDIT)

feature_id: feat-028
date (UTC): 2026-04-10T12:30:00Z
environment_mode: execute
audit_result: WARN

## INVOCATIONS
- audit_engine: sdd-audit (inline)
- policy: `00_project_documentation/SDD/02_policies/REPORT_ENVELOPE_POLICY.md`
- policy: `00_project_documentation/SDD/02_policies/INTEGRATION_SURFACE_POLICY.md` (wiring)

## EVIDENCE
### Fitxers llegits
- Spec: `00_project_documentation/SDD/artifacts/specs/feat-028-llm-proxy-hardening.md`
- VERIFY (original): `00_project_documentation/SDD/audit_reports/verify_feat_028_2026-04-09.md`
- Code (hardening exists):
  - `02_implementation/internal/llm/proxy_hardening.go`
  - `02_implementation/internal/llm/virtual_keys.go`
- Code (handler wiring):
  - `02_implementation/internal/api/handlers_dashboard.go` (`handleLLMChat`)

### Observació clau (wiring)

`handleLLMChat` envia requests amb `llm.Client.SendRequest(...)` (amb fallback a Ollama) i **no** passa per cap capa de hardening (retry/cooldown/rate-limit/spend/virtual-key ACL) definida a feat-028.

## COMMANDS
- status: NOT EXECUTED
- reason: Aquest reaudit és evidencia-per-lectura (gap de wiring). Els tests existents no demostren “handler → hardening”.

## COMPLIANCE (wiring)
| Item (Acceptance) | Estat | Evidència |
|---|---|---|
| A1 retry/cooldown/fallback aplicat al chat | PARTIAL | Hardening existeix (`internal/llm`) però `handleLLMChat` no el crida |
| A3 rate limit (429) aplicat al chat | PARTIAL | Virtual keys/hardening no wired al handler |
| A6 ACL virtual key (403) al chat | PARTIAL | Handler no enforceix `virtual_keys` |

## VERDICT
- verdict: WARN
- reasons:
  1) La lògica de hardening existeix i està testejada a `internal/llm`, però falta integració a la surface `wiring` (handler).
  2) Els reports PASS/PARTIAL previs no evidencien el camí complet “API chat → hardening → provider”.
  3) Cal una acció explícita: o integrar el hardening a `handleLLMChat`, o ajustar l’scope/acceptance per reflectir que és backend-only.
- next_action:
  1) Reclassificar la feature com a `verification_result: PARTIAL` (manté), i `audit_result: WARN`.
  2) Obrir subfeature nova per wiring (`feat-028b` o feat nova) si es decideix completar l’acceptance a nivell d’API.

