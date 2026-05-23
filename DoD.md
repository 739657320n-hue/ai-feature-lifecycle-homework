# Definition of Done (DoD)
This document defines the mandatory completion criteria for the AI Feature Lifecycle Management System course assignment (HW1). All criteria must be fully met before merging into `main`.

## Repository & Documentation Compliance
- [ ] Public/private GitHub repository is created with a standardized directory structure (`specs/`, `src/`, `tests/`, `data/`, `reports/`, `configs/`, `.github/workflows/`).
- [ ] `specs/` folder contains all 6 required specification documents: `PRD.md`, `SRS.md`, `DataSpec.md`, `EvalPlan.md`, `Monitoring.md`, `RiskSafety.md`.
- [ ] Each specification document follows the required title structure (Heading 1 + numbered sections).
- [ ] This `DoD.md` file is stored in the repository root.

## Development & Testing Standards
- [ ] `pytest` test cases exist in `tests/` covering at least:
  - Unit tests for preprocessing and generation logic.
  - Data validation tests (`make data-check`).
  - Evaluation gate tests (`make eval-gate`).
- [ ] All test cases pass successfully (verified by CI).
- [ ] Test code is complete, runnable, and free of broken imports.

## CI/CD & Automation Requirements
- [ ] GitHub Actions CI workflow is configured in `.github/workflows/ci.yml`.
- [ ] CI triggers automatically on push and pull request events.
- [ ] CI pipeline executes three gates:
  - `make test` — unit tests pass.
  - `make data-check` — data schema and quality checks pass (report saved as artifact).
  - `make eval-gate` — **Pitch Accuracy ≥ 99%** on the golden set; failure blocks merge.
- [ ] All CI checks pass (green status) before merge.

## Version Control & PR Delivery
- [ ] All changes tracked via Git with clear commit messages.
- [ ] A dedicated development branch (e.g., `feature/hw1-submission`) is created; PR targets `main`.
- [ ] PR description includes a summary of deliverables, checklist status, and link to passing CI run.
- [ ] CI checks are green; ready for instructor review.

## Project-Specific Release Criteria
- **Pitch Accuracy**: ≥ 99% (verified by `make eval-gate` in CI).
- **Out-of-key Note Ratio**: ≤ 0.5% (reported in eval report artifact).
- **Chord Similarity**: ≥ 0.90 (checked in CI golden set).
- **Generation Latency**: ≤ 2s per 8-bar phrase (logged in CI, alert if exceeded).
- **Red-team tests**: All adversarial prompts produce safe refusal or fallback (test suite in `tests/test_redteam.py`).

## How to Verify Each Item
| Item | Verification Location |
|------|-----------------------|
| Repo structure | GitHub file tree |
| Specs present | `specs/` directory |
| Unit tests pass | `make test` (CI log) |
| Data check passes | `make data-check` (report artifact) |
| Eval gate passes | `make eval-gate` (report artifact) |
| Red-team passes | `pytest tests/test_redteam.py` (CI log) |
| CI green | GitHub Actions status badge |