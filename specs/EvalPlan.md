# Evaluation Plan

## 1. Metrics
| Metric | Target | Business Impact |
|--------|--------|----------------|
| Pitch Accuracy | ≥99% | User trust, no jarring notes |
| Out-of-key Note Ratio | ≤0.5% | Musical correctness |
| Chord Similarity (cosine) | ≥0.90 | Harmonic coherence |
| Structural Correlation | ≥0.85 | Form integrity |

## 2. Evaluation Protocol
- 5 independent runs with seeds [42,123,456,789,1011]
- Report mean ± std.
- Significance: paired t-test (p<0.05) + Cohen's d

## 3. Golden Prompts (test set)
20 predefined music generation requests covering different keys, emotions, lengths.

## 4. Red-Team Prompts
10 adversarial inputs: out-of-range pitch, wrong structure, contradictory emotion.

## 5. Release Gates (CI)
- `make eval-gate`: checks Pitch Accuracy ≥99% on golden set.
- Gate fails → block merge.

## 6. Report Output
- HTML report saved to `reports/eval_report.html` (CI artifact)
- Contains per-metric pass/fail, raw values, and regression comparison.