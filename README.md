# AI Feature Lifecycle Homework

This repository is the assignment deliverable for the **AI Feature Lifecycle** course. It demonstrates a complete feature lifecycle—from data preparation and model training to evaluation, safety gating, and CI/CD. All code and configurations are structured according to industry best practices.

---

## Table of Contents

-   [Project Overview](#project-overview)
    
-   [Directory Structure](#directory-structure)
    
-   [How to Set Up and Run](#how-to-set-up-and-run)
    
    -   [Environment Setup](#1-environment-setup)
        
    -   [Running the Pipeline](#2-running-the-pipeline)
        
    -   [Running Tests](#3-running-tests)
        
-   [CI/CD and Gates](#cicd-and-gates)
    
-   [Deliverables Checklist](#deliverables-checklist)
    
-   [License](#license)
    

---

## Project Overview

The project implements:

-   **Music generation** with a simulated model (e.g., MusicGen-style).
    
-   **Data preprocessing** and **feature engineering**.
    
-   **Training pipeline** with MLflow tracking.
    
-   **Evaluation gates** (threshold-based quality checks).
    
-   **Tool validation** (allowlist, write-tool confirmation, parameter schema).
    
-   **LLM safety gates** (red-teaming, golden prompt testing).
    
-   **CI/CD** via GitHub Actions with multiple workflow files.
    

---

## Directory Structure

The repository follows the course slide layout plus additional folders for LLM‑specific work:

```text
.
├── .github/workflows/          # CI workflow files
│   ├── data-check.yml
│   ├── eval_gate.yml
│   ├── llm-gates.yml
│   ├── safety-tests.yml
│   └── slo-gate-ci.yml
├── configs/                    # Configuration files
│   ├── ci_config.yml
│   ├── thresholds.yaml
│   └── tool_allowlist.yaml
├── data/                       # All datasets
│   ├── golden_set/             # Golden samples (JSONL)
│   │   ├── golden_samples.jsonl
│   │   └── metadata.json
│   ├── processed/
│   ├── raw/
│   ├── reports/
│   ├── splits/
│   └── ... (generation scripts)
├── labeling/                   # (future use)
├── models/                     # Model artifacts
├── notebooks/                  # Jupyter notebooks
├── pipelines/                  # Training and evaluation scripts
│   ├── data/                   # Data pipeline
│   ├── reports/                # Pipeline-generated reports
│   ├── eval_gate.py            # Evaluation gate (pytest test file)
│   ├── metrics.py
│   ├── slo_gate.py
│   ├── tracker.py
│   └── train.py
├── reports/                    # Global generated reports
│   └── metrics.json
├── specs/                      # Specification documents
│   ├── Acceptance_Criteria_Table.md
│   ├── Dataset_Card.md
│   ├── Data_Contract.md
│   ├── Data_Spec.md
│   ├── Eval_Plan.md
│   ├── Incident_Playbook.md
│   ├── Model_Spec.md
│   ├── Monitoring.md
│   ├── PRD.md
│   ├── RELEASE_CHECKLIST.md
│   ├── Risk_Safety.md
│   ├── Rollout_Plan.md
│   ├── Safety_Privacy_Policy.md
│   └── SRS.md
├── specsLLM/                   # LLM-specific specs
│   ├── LLM_Eval_Plan.md
│   ├── Output_Schema.json
│   ├── Prompt_Behavior_Spec.md
│   ├── RAG_Spec.md
│   └── Tool_Contracts.md
├── src/                        # Source code
│   ├── feature_preprocessing.py
│   └── tool_validator.py
├── tests/                      # Unit & integration tests
│   ├── redteam/
│   ├── reports/
│   ├── test_data_checks.py
│   ├── test_preprocessing.py
│   └── test_safety.py
├── testsLLM/                   # LLM-specific tests
│   ├── golden_prompts.json
│   ├── redteam_prompts.json
│   ├── test_golden.py
│   ├── test_redteam.py
│   └── test_tool_gate.py
├── .gitignore
├── DoD.md
├── label_studio_config.xml
├── Makefile
├── metrics.json                # (root-level report)
├── README.md                   # This file
└── requirements.txt
```

---

## How to Set Up and Run

### 1\. Environment Setup

```bash
# Clone the repository
git clone https://github.com/YOUR_USER/ai-feature-lifecycle-homework.git
cd ai-feature-lifecycle-homework

# Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
.venv\Scripts\activate      # Windows

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

If you don’t have a `requirements.txt` yet, install the core packages manually:

```bash
pip install pytest pandas scikit-learn joblib pyyaml
```

### 2\. Running the Pipeline

**Data preprocessing:**

```bash
python src/feature_preprocessing.py
```

**Training:**

```bash
python pipelines/train.py
```

**Evaluation (SLO gate):**

```bash
python pipelines/slo_gate.py
```

**Evaluation gate (pytest‑based):**

```bash
make eval-gate
# or directly:
python -m pytest pipelines/eval_gate.py -v
```

### 3\. Running Tests

All test suites can be executed with pytest:

```bash
# Run all tests (including LLM tests)
pytest tests/ testsLLM/ -v

# Run only specific test files
pytest tests/test_safety.py -v
pytest testsLLM/test_tool_gate.py -v
pytest testsLLM/test_golden.py -v
```

**Note:** The `tool_allowlist.yaml` has been updated so that `generate_audio` requires human confirmation (`confirmation_required: true`). The corresponding test now passes.

---

## CI/CD and Gates

GitHub Actions workflows are configured in `.github/workflows/`:

| Workflow File | Description |
| --- | --- |
| `data-check.yml` | Validates dataset integrity |
| `eval_gate.yml` | Runs evaluation thresholds check |
| `llm-gates.yml` | LLM prompt & tool validation |
| `safety-tests.yml` | Safety and red‑team tests |
| `slo-gate-ci.yml` | Service‑level objective gates |

Each workflow triggers on every push and pull request. A green check mark appears when all gates pass.

---

## Deliverables Checklist

| #   | Deliverable | Status |
| --- | --- | --- |
| 1   | Public GitHub repository | ✅   |
| 2   | Standard folder structure | ✅   |
| 3   | Six specification documents | ✅   |
| 4   | One CI check (GitHub Actions) | ✅   |
| 5   | Runnable README with instructions | ✅   |
| 6   | All core feature code (src) | ✅   |
| 7   | Unit tests (tests + testsLLM) | ✅   |
| 8   | Tool validation (allowlist) | ✅   |
| 9   | Evaluation gate (thresholds) | ✅   |
| 10  | LLM safety/red‑team tests | ✅   |

---

## License

This project is for educational purposes as part of the AI Feature Lifecycle course. No license is implied for production use.

---

*For questions or issues, please open a GitHub Issue.*