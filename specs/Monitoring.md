# Monitoring Plan – Music Generation Service

## 1. Service Health (Infrastructure)

| Signal | Metric / Calculation | Threshold | Severity | Owner | Action |
|--------|----------------------|-----------|----------|-------|--------|
| Inference latency | p99 latency (ms) | > 2500 ms for 5 consecutive minutes | **Critical** | Carol (Engineering Lead) | Auto‑scale GPU replicas; if exceeds 3000 ms, rollback via `use_new_model` flag |
| Inference latency | p95 latency (ms) | > 2000 ms for 10 minutes | Warning | Carol | Scale up GPU or throttle incoming requests |
| Error rate | HTTP 5xx / inference failures | > 1% for > 2 minutes | **Critical** | Carol | Rollback immediately to previous model version |
| GPU memory | Memory usage (GB) | > 5 GB on any node | Warning | Carol | Check for memory leak; rotate model if persistent |
| Throughput | Requests per second (RPS) | < 10 RPS (degradation) | Warning | Alice (Platform) | Investigate upstream connectivity or scaling limits |

## 2. Model Quality Proxies (Model Incidents)

| Signal | Metric / Calculation | Threshold | Severity | Owner | Action |
|--------|----------------------|-----------|----------|-------|--------|
| Quality proxy | Silence ratio (frames < -60dB) | > 5% of outputs in a 5‑minute window | **Critical** | Carol | Rollback model; investigate training data or post‑processing |
| Golden test set | Pitch accuracy on held‑out set | < 98% for two consecutive evaluation runs | **Critical** | Bob (Data Scientist) | Trigger retraining pipeline; block any promotion until fixed |
| Slice regression | FAD per genre (e.g., classical, jazz) | > 3.5 for any genre | Warning | Bob | Investigate genre‑specific drift; consider domain tuning |
| User feedback | Thumbs‑down rate (sampled) | Increase > 5% compared to previous 24h baseline | Warning | Alice (Product) | Tag for review; if >10%, escalate to Carol for rollback consideration |

## 3. Data Drift (Data Incidents)

| Signal | Metric / Calculation | Threshold | Severity | Owner | Action |
|--------|----------------------|-----------|----------|-------|--------|
| Input drift | KL divergence of note distribution (daily vs. training) | > 0.1 on a 1% sample of inputs | Warning | Bob | Begin investigation; re‑run data contract checks |
| Output drift | Distribution of generated audio features (RMS, centroid) | KL > 0.15 vs. previous day | Warning | Bob | Compare with production baseline; escalate to Carol if persists > 24h |
| Schema violation | Input prompt length > 512 chars or empty | > 1% of requests | **Critical** | Carol | Isolate bad inputs; contact upstream data producer; add preprocessing guard |

## 4. Cost Monitoring (Business KPIs)

| Signal | Metric / Calculation | Threshold | Severity | Owner | Action |
|--------|----------------------|-----------|----------|-------|--------|
| Inference cost | Daily GPU cost ($) | > $10 | Warning | Alice (Finance) | Notify team; review model size or caching strategy |
| Token cost (if LLM) | Tokens per request | > 2000 tokens per request average | Warning | Carol | Investigate prompt patterns; consider token limit enforcement |
| Cost spike | Hourly GPU cost > $2 | > $2/hour for 2 hours | Warning | Alice | Downgrade to cheaper model variant if available |

## 5. Error Tracking (Unexpected Failures)

| Signal | Metric / Calculation | Threshold | Severity | Owner | Action |
|--------|----------------------|-----------|----------|-------|--------|
| Crashes | Unexpected non‑compliance (empty output, wrong format) | > 5 occurrences per hour | **Critical** | Carol | Route to Sentry; check error logs; rollback if code change introduced bug |
| Log leaks | PII detected in logs (email, phone) | Any occurrence | **Critical** | Bob (Security) | Rotate log credentials; isolate affected logs; run redaction |

## 6. Ownership Summary

- **Carol (Engineering Lead)**: Latency, error rate, GPU memory, rollback execution, quality proxies.
- **Bob (Data Scientist / Security)**: Drift monitoring, schema checks, golden test set, log security.
- **Alice (Product / Finance)**: Cost monitoring, user feedback, throughput.

## 7. Alerting Channels

| Severity | Channel | Response Time |
|----------|---------|---------------|
| Critical | PagerDuty / #incident Slack | 5 minutes |
| Warning | Email / #monitoring Slack | 4 business hours |
