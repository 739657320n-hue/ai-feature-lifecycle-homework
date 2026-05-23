# Release Checklist – Music Generation Model

Before promoting a model version from **staging** to **production**, verify all items below.

### Metrics & Evaluation

 **FAD score** < 3.0 on the held-out test set (report attached)

 **CLAP similarity** > 0.75 on a diverse prompt set (≥200 prompts)

 **Mean output duration** within ±10% of expected (e.g., 30s ±3s)

 **Silence ratio** (frames < -60dB) < 2% over all test samples

 **Per‑genre slice metrics** all pass (FAD per genre < 3.5)

### Version Control

 Model artifact is registered in MLflow with a unique version and checksum

 Training dataset version (hash or tag) recorded in the experiment

 Pre‑/post‑processing code pinned to a Git commit or tag

 Inference hyperparameters (temperature, top_p, max_length) stored in a versioned config file

### Tests & Validations

 Unit tests for data preprocessing pass (resample, trim, format)

 Integration test: model can generate 3‑second audio within 1.5s latency

 Data contract check: input schema (text length, optional melody) matches expected

### Security & Safety

 No new secrets or credentials in code (scanned with `git secrets` or similar)

 Input text filter active: blocked prompts with potentially harmful content

 Output audio volume normalization applied (no sudden loud clips)

### Rollback Readiness

 Previous production model version is tagged `rollback-ready` in registry

 Rollback procedure documented and tested in staging (≤5 min)

 Feature flag `use_new_model` is toggleable without redeployment

### Approvals

 At least one peer review on the PR (code + evaluation report)

 Lead engineer sign‑off for metrics threshold pass

 Product owner confirmation (if user‑facing impact is high)

> All checklist items must be **green** before a production promotion. Partial passes require a **waiver** approved by the team lead.