# Monitoring Plan

## 1. System Health
- GPU utilization, memory, latency (Prometheus + Grafana)
- Alert when p95 latency >2.5s or memory >5 GB

## 2. Model & Data Drift
- Compare generated note distribution vs training data (KL divergence)
- Trigger retraining if pitch accuracy drops below 98% on a held-out test

## 3. Cost Monitoring
- Log tokens (if using LLM) or compute time per generation
- Alert if daily GPU cost > $10

## 4. Error Tracking (Sentry)
- Catch unexpected non-compliance: output empty, wrong format, crash
- Route errors to owner via CODEOWNERS

## 5. Incident Playbook
- If drift detected: revert to previous model version, raise ticket
- If latency spike: scale up GPU, or throttle requests