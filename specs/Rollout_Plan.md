# Rollout Plan – Canary / Shadow Deployment

## 1. Shadow Mode (Pre‑Canary)
- **Duration**: 24 hours in staging environment.
- **Action**: Deploy new model `v2.0.0` alongside the current production model `v1.0.0`. Both receive the same input but v2.0.0 outputs are **not served** to users.
- **Comparison**:
  - Collect output audio features (RMS energy, spectral centroid, duration).
  - Compare distribution of features using KL divergence.
  - Log any output where silence ratio > 5% as a warning.
- **Exit criteria**: No more than 5% of samples show “drifted” features (KL > 0.1). If exceeded, abort.

## 2. Canary Release
- **Traffic splits**:
  - Phase 1: 5% new model, 95% current → observe 30 minutes.
  - Phase 2: 25% new, 75% current → observe 30 minutes.
  - Phase 3: 50% new, 50% current → observe 1 hour.
  - Phase 4: 100% new → final observation.
- **Observation window**: Each phase runs a fixed time; pause and evaluate.
- **Metrics to watch**:
  - Error rate (HTTP 5xx / inference failures) – threshold: < 1%
  - p99 latency – threshold: < 2.5s (from 200 concurrent requests)
  - User feedback (thumbs down percentage) – threshold: < 5% increase vs baseline
- **Rollback triggers** – if ANY condition is met:
  1. Error rate exceeds 1% for more than 2 consecutive minutes.
  2. p99 latency exceeds 3s and does not recover within 1 minute.
  3. User negative feedback jumps > 10% over baseline.
- **Rollback action**: Immediately set traffic to 0% for new model (feature flag override). Previous model remains deployed and ready.

## 3. Gradual Ramp‑Up (Post‑Canary)
After successful 100% canary, release to all users. Monitor for 24 hours at full production load. No additional split needed.

## 4. Kill Switch
- A dedicated endpoint `/admin/rollback` that instantly switches traffic back to `v1.0.0`.
- Automation: If latency p99 > 4s for 30 seconds, auto‑rollback (via deployment controller).

> **Owner**: [Wang] – responsible for monitoring and executing rollback if needed.