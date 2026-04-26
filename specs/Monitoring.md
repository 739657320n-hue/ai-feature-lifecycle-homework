# Monitoring Specification – Music Generation Service

## Signals, Thresholds & Actions

| Signal | Metric | Threshold | Action | Owner |
|--------|--------|-----------|--------|-------|
| **Latency** | p99 inference time (ms) | > 2500ms for 1 min | Auto‑scale GPU workers; alert #oncall | Alice (Infra) |
| **Error rate** | HTTP 5xx / total requests (%) | > 1% for 2 min | Page on‑call; investigate model or cluster | Bob (ML) |
| **Throughput** | Requests per second | < 5 for 5 min (too low) or > 100 (unexpected spike) | Alert; check for traffic anomaly | Carol (Ops) |
| **Data drift** | Text input embedding distribution (KL divergence vs training) | > 0.15 over 1‑hour window | Notify data team; trigger retraining if sustained | David (Data) |
| **Quality proxy – silence** | % of generated files with >5% silent frames | > 3% over last 1000 requests | Alert ML team; review model behavior | Eve (QA) |
| **Quality proxy – duration** | Mean output duration | < 80% or > 120% of expected (e.g., 30s) | Investigate prompt or generation parameters | Frank (ML) |
| **Cost** | Daily inference cost ($) | > $50/day | Flag to engineering lead; consider throttling | Grace (PM) |
| **Cost** | Cost per request ($) | > $0.05 | Log; warn if sustained | Grace (PM) |

## Alert Routing
- **P1 (Critical)** : Latency p99 > 4s, error rate > 5% → page on‑call immediately (PagerDuty / Slack urgent).
- **P2 (Warning)** : Drift threshold hit, quality proxy degradation → Slack channel #ml-alerts, next business day response.
- **P3 (Info)** : Cost approaching daily budget → email to team lead.

## Detection Tools
- Prometheus + Grafana for latency, error rate, throughput.
- Evidently AI for data drift checks (run as sidecar or scheduled job).
- Custom logging to CloudWatch / ELK for silence ratio, duration.

> All thresholds are subject to review every 2 weeks and updated as system matures.