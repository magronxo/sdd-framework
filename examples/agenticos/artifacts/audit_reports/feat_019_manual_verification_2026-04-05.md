# feat-019 Manual Verification - 2026-04-05

**Feature:** `feat-019`  
**Date:** 2026-04-05  
**Mode:** Manual runtime verification  
**Environment:** `K:\AgenticOsGen\02_implementation\manual_verification\feat-019-2026-04-05\agenticos_data`

## Setup

- Kernel launched against a temporary `AGENTICOS_DATA_DIR`.
- Security policy was scoped to the temporary workspace path.
- A local mock LLM server was started on `http://127.0.0.1:4010`.
- Seed path used: `K:\AgenticOsGen\03_deployments\seed`.

## T14 - Direct Valid Ticket

- Ticket ID: `manual_direct_ok_001`
- Input: direct `fs_read` against workspace file `test.txt`
- Observed final status: `COMPLETED`
- Observed result: `stdout = "manual hello"`
- Evidence path:
  `K:\AgenticOsGen\02_implementation\manual_verification\feat-019-2026-04-05\agenticos_data\tickets\success\manual_direct_ok_001.json`

## T15 - Direct Ticket Blocked By Guardian

- Ticket ID: `manual_direct_blocked_001`
- Input: direct `fs_read` against forbidden path `/etc/passwd`
- Observed final status: `FAILED`
- Observed error code: `E_PATH_TRAVERSAL`
- Observed message: `Path contains forbidden pattern: /etc/`
- Evidence path:
  `K:\AgenticOsGen\02_implementation\manual_verification\feat-019-2026-04-05\agenticos_data\tickets\failed\manual_direct_blocked_001.json`

## T16 - llm_agent Ticket

- Ticket ID: `manual_llm_001`
- Input: `llm_agent` ticket with `instruction`, `department=genesis`, `maxSteps=3`
- Mock LLM returned a direct completion response
- Observed final status: `COMPLETED`
- Observed result:
  `reasoning = "Resposta manual"`
  `lesson_learned = "manual verification"`
  `steps_taken = 1`
- Evidence path:
  `K:\AgenticOsGen\02_implementation\manual_verification\feat-019-2026-04-05\agenticos_data\tickets\success\manual_llm_001.json`

## T17 - Execution Failure

- Ticket ID: `manual_exec_fail_001`
- Input: direct `fs_read` against missing file inside allowed workspace
- Observed final status: `FAILED`
- Observed error code: `E_FILE_NOT_FOUND`
- Observed message starts with:
  `File not found: ...\workspace\missing.txt`
- Evidence path:
  `K:\AgenticOsGen\02_implementation\manual_verification\feat-019-2026-04-05\agenticos_data\tickets\failed\manual_exec_fail_001.json`

## Notes

- Manual verification confirmed final closure paths and contract-compliant archives for all four scenarios.
- Intermediate states `AUDITING` and `EXECUTING` were already covered by automated integration tests; during manual runs these transitions completed too quickly to capture reliably by hand.
- No ambiguous leftovers remained in `tickets/incoming` or `tickets/processing` for the verified cases.
