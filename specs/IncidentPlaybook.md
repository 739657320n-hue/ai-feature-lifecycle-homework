# Incident Playbook – Music Generation Service

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

## Type 2: Model Incident – Quality Degradation (Silence Surge)
- **Symptoms**: Abrupt increase in generated silence > 5% of requests. User complaints rising.
- **Triage**:
  1. Check quality proxy (silence ratio) dashboard – confirm spike.
  2. Compare to any recent model deployment or training data change.
  3. Sample 50 silent outputs – is it all silence or partial? Check with playback.
- **Rollback**: Immediately switch traffic to previous model version (feature flag or DNS). Monitor silence ratio drops.
- **Resolution**: Investigate root cause (training data contamination? bug in post‑processing?). Fix and re‑evaluate.
- **Post‑mortem**: Add slice monitoring by prompt category.

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

> **General Rollback Procedure** (for all incidents):
> 1. Set `use_new_model` feature flag to `false`.
> 2. Verify traffic shifts to old model within 30 seconds.
> 3. Confirm silence ratio / latency return to normal.
> 4. Announce in #incident channel.