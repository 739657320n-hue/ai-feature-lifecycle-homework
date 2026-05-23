# Incident Playbook – Music Generation Service

> **General Rollback Procedure (applicable to all incidents):**
> 1. Set the `use_new_model` feature flag to `false`.
> 2. Verify traffic shifts to the old model within 30 seconds.
> 3. Confirm that silence ratio / latency returns to normal.
> 4. Announce in the #incident channel.

---

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

---

## Scenario 2: Tool Misuse (Unauthorized Delete)

- **Detection**: User reports lost files, or monitoring shows spike in `delete_audio` calls.
- **Owner**: Engineering Owner (Carol)
- **Immediate actions**:
  1. Revoke tool access for the affected model version.
  2. Rollback to previous model version.
  3. Recover deleted files from backup (if any).
- **Escalation**: Confirm no recurrence; inform Security Owner.
- **Resolution**: Add mandatory confirmation gate for all destructive tool calls.
- **Post‑incident review**: Update tool allowlist and run regression tests.

---

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

---

## Type 1: Data Incident – Schema Violation / Missing Features

- **Symptoms**: Input text is empty or malformed; upstream feeder returns 400.
- **Impact**: Users receive 500 errors; generation fails.
- **Triage**:
  1. Check input pipeline logs (e.g., Kafka / HTTP ingress). Is a data source broken?
  2. Check sample of recent inputs – do they match expected schema?
  3. If upstream issue, contact the data producer team.
- **Rollback**: If the model itself is fine, just fix the feeder. If model is not handling edge cases, rollback model to previous version.
- **Resolution**: Patch the preprocessing to handle missing fields gracefully; add unit test.
- **Post‑mortem**: Update data contract checks in CI.

---

## Type 2: Model Incident – Quality Degradation (Silence Surge)

- **Symptoms**: Abrupt increase in generated silence > 5% of requests. User complaints rising.
- **Triage**:
  1. Check quality proxy (silence ratio) dashboard – confirm spike.
  2. Compare to any recent model deployment or training data change.
  3. Sample 50 silent outputs – is it all silence or partial? Check with playback.
- **Rollback**: Immediately switch traffic to previous model version (feature flag or DNS). Monitor silence ratio drops.
- **Resolution**: Investigate root cause (training data contamination? bug in post‑processing?). Fix and re‑evaluate.
- **Post‑mortem**: Add slice monitoring by prompt category.

---

## Type 3: Infrastructure Incident – Latency SLO Breach

- **Symptoms**: p99 latency > 3s for 5 minutes; some requests time out.
- **Triage**:
  1. Check GPU utilization – any OOM or node failure?
  2. Check network latency between frontend and inference endpoint.
  3. Check queuing depth – is request rate exceeding capacity?
- **Immediate action**: Scale up GPU replicas (if auto‑scaling disabled). If no spare capacity, downgrade model to a smaller variant (e.g., tiny model) using feature flag.
- **Rollback**: If scaling fails or downgrade doesn’t help, rollback to previous model version (which may be lighter).
- **Long‑term fix**: Increase cluster size, add caching for repeated prompts, or implement request queuing with priority.
- **Post‑mortem**: Review cost‑performance trade‑off; adjust auto‑scaling policy.