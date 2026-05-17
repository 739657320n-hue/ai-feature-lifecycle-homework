# Incident Playbook – MusicGen Service

## Scenario 1: Data Exposure (PII in Logs)
- **Detection**: gitleaks alert or manual log review shows raw prompt with email address.
- **Owner**: Security Owner (Bob)
- **Immediate actions**:
  1. Rotate log store credentials.
  2. Isolate the affected log partition.
  3. Run Presidio redaction on remaining logs.
- **Escalation**: Notify Product Risk Owner (Alice) within 1 hour.
- **Resolution**: Apply redaction middleware at the ingest point.
- **Post‑incident review**: Add automated check for PII in logs.

## Scenario 2: Tool Misuse (Unauthorized Delete)
- **Detection**: User reports lost files, or monitoring shows spike in delete_audio calls.
- **Owner**: Engineering Owner (Carol)
- **Immediate actions**:
  1. Revoke tool access for the affected model version.
  2. Rollback to previous model version.
  3. Recover deleted files from backup (if any).
- **Escalation**: Confirm no recurrence; inform Security Owner.
- **Resolution**: Add mandatory confirmation gate for all destructive tool calls.
- **Post‑incident review**: Update tool allowlist and run regression tests.

## Scenario 3: Model Safety Regression
- **Detection**: Refusal rate drops below 95% or red‑team test fails in CI.
- **Owner**: Engineering Owner (Carol)
- **Immediate actions**:
  1. Block any PR that caused regression.
  2. Rollback model to the last safe version.
  3. Re‑run full red‑team suite.
- **Escalation**: Notify Security Owner; schedule a hotfix.
- **Resolution**: Identify root cause (prompt change? training data drift?) and apply fix.
- **Post‑incident review**: Add new golden prompts to regression suite.