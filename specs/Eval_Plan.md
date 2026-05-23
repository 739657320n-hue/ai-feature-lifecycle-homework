# Evaluation Plan – Music Generation Transformer

## 1. Metrics

| Metric                    | Target      | Business Impact                |
|---------------------------|-------------|--------------------------------|
| Pitch Accuracy            | ≥99%        | User trust, no jarring notes   |
| Out-of-key Note Ratio     | ≤0.5%       | Musical correctness            |
| Chord Similarity (cosine) | ≥0.90       | Harmonic coherence             |
| Structural Correlation    | ≥0.85       | Form integrity (verse–chorus)  |

All metrics are computed on the golden set (20 segments).  
Baseline values are recorded in the first champion model run.

---

## 2. Evaluation Protocol

- **Runs**: 5 independent runs with fixed seeds [42, 123, 456, 789, 1011]
- **Report**: mean ± standard deviation for each metric
- **Significance**: paired t‑test (p < 0.05) + Cohen’s d (effect size)

---

## 3. Data Slices (≥6)

| Slice Name          | Description                                          | # Golden Samples |
|---------------------|------------------------------------------------------|------------------|
| Genre Pop           | 5 pop samples (keys: various)                        | 5                |
| Genre Classical     | 5 classical samples                                  | 5                |
| Genre Jazz          | 5 jazz samples                                       | 5                |
| Genre Rock          | 5 rock samples                                       | 5                |
| BPM Low (≤100)      | All samples with BPM ≤100                            | 6                |
| BPM High (>100)     | All samples with BPM >100                            | 14               |
| Mood Energetic      | Samples with mood = “energetic” or “happy”           | 8                |
| Mood Calm/Sad       | Samples with mood = “calm” or “sad”                  | 4                |
| Key Major           | Samples in major keys (G, C, F, etc.)                | 5                |
| Key Minor           | Samples in minor keys (E, D, A, etc.)                | 15               |
| Duration ≤10s       | Samples of 5 seconds (all golden are 5s, but future) | 20               |
| Time 4/4            | All golden samples are 4/4                           | 20               |

*These slices ensure coverage across genre, tempo, emotion, tonality, and length.*

---

## 4. Thresholds / Gates

All thresholds are defined in `configs/thresholds.yaml`.

- **Gate 1 (strong)**: *Pitch Accuracy* ≥99% on the full golden set.
- **Gate 2 (weak)**: All four metrics must meet their absolute thresholds.
- **Gate 3 (relative)**: Improvement over baseline (see thresholds.yaml: relative section).

Gate failure → **block merge** (CI exit 1).

---

## 5. Regression Rule

- **Regression** is declared when any of the four primary metrics drops by more than **1% absolute** on the golden set compared to the **champion baseline**.
- The champion baseline is the last model that passed all gates.
- If a regression is detected, the candidate model is **automatically rejected**.
- The regression comparison runs during CI (via `eval_gate.py`).

---

## 6. Release Gates (CI)

- `make eval-gate` runs `eval_gate.py`:
  1. Load golden set (generate if missing)
  2. Evaluate model (simulated or real)
  3. Write `reports/metrics.json`
  4. Compare with `configs/thresholds.yaml`
  5. Exit with 0 (pass) or 1 (fail)

---

## 7. Report Output

- **`reports/metrics.json`** – JSON of all per-metric values and pass/fail status.
- **`reports/eval_report.html`** – (optional) HTML summary for artifact upload.