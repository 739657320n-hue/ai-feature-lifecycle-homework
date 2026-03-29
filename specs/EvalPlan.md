# Eval Plan (Evaluation Plan)
## 1. Metric Selection
- Metrics shall reflect business costs, not just model performance
- Define target thresholds in the evaluation script

## 2. Slices & Segments
- Per-segment metrics table for key user groups
- Avoid masking failures with aggregated data; ensure segmented reports are visible

## 3. Release Gates
- Configure eval_gate CI task
- Pipeline automatically fails if thresholds are not met; manual override is not allowed

## 4. Regression Testing
- Protect critical behavior across versions using golden datasets and snapshot tests
- Regression report against the previous version must be provided

## 5. Reporting
- Evaluation report (HTML or Markdown format) stored at /reports/eval_report.md
- Must be attached as CI artifacts for every run
