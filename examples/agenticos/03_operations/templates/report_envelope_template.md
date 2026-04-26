# Template: Report Envelope (VERIFY / AUDIT)

> Aquest template segueix `00_project_documentation/SDD/02_policies/REPORT_ENVELOPE_POLICY.md`.

---

# <type>_<feature_id>_<YYYY-MM-DD>

feature_id: feat-XXX
date (UTC): YYYY-MM-DDTHH:MM:SSZ
environment_mode: execute | plan-only | unknown
verification_result: PASS | PARTIAL | FAIL
audit_result: PASS | WARN | FAIL

## INVOCATIONS
- engine: (sdd-verify | sdd-audit | inline)
- skill: (si aplica)
- notes: (constraints: PLAN mode, manca runner, etc.)

## EVIDENCE
### Fitxers llegits
- (paths)

### Artefactes / context
- feature record: (path)
- spec: (path)
- tasks: (path)
- reports previs: (paths)

## COMMANDS
- (cwd) `command`
  - status: EXECUTED | NOT EXECUTED
  - reason (si NOT EXECUTED): ...
  - raw_output (si EXECUTED):
    ```
    ...
    ```

## COMPLIANCE (opcional però recomanat)
| Item (SDT/RF) | Estat | Evidència |
|---|---|---|
| SDT-01 ... | COMPLIANT / PARTIAL / UNTESTED / FAILING / UNKNOWN | TestX / output / manual |

## VERDICT
- verdict: PASS / PARTIAL / FAIL (verify) o PASS / WARN / FAIL (audit)
- reasons:
  1) ...
  2) ...
  3) ...
- next_action:
  1) ...
  2) ...
  3) ...

## SURFACES (obligatori)
- browser: true|false
- os_fs: true|false
- wiring: true|false
- network: true|false
- env_proxy: true|false
- notes: (opcional)

### Surface Evidence (si alguna surface és true)
| Surface | Evidència | Estat |
|---------|-----------|-------|
| browser | (ref: preflight / Network tab) | OK / MISSING |
| wiring | (ref: test handler→core) | OK / MISSING |
| os_fs | (ref: test path handling) | OK / MISSING |
| network | (ref: test retries/timeout) | OK / MISSING |
| env_proxy | (ref: env notes / wrapper) | OK / MISSING |
