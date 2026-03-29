# ai-feature-lifecycle-homework

This repository is the assignment deliverable for the AI Feature Lifecycle course. It is created in strict accordance with the course slides, including all core deliverables and standard directory structures.

## Repository Directory Structure (Consistent with Course Slides)
- /specs: Stores 6 specification documents (PRD.md, SRS.md, etc.)
- /src: Stores feature code and preprocessing logic
- /tests: Stores pytest test cases
- /pipelines: Stores training and evaluation scripts
- /reports: Stores evaluation reports, data quality reports, etc.
- /configs: Stores configuration files such as CI settings
- /examples: Stores sample test data

## How to Set Up and Run (Consistent with Course Requirements for Runnable README)
### 1. Environment Setup
```bash
# Clone the repository
git clone Your Repository URL
cd Repository Name

# Install dependencies
pip install --upgrade pip
pip install pytest pandas scikit-learn joblib
```

### 2. Running Steps
1.  Preprocess data: Run src/feature_preprocessing.py
2.  Train the model: Run pipelines/train.py
3.  Evaluate the model: Run pipelines/eval.py
4.  Run tests: pytest tests/

### 3. Reproduction Instructions
- All codes can be run directly without additional dependencies
- Data versions are fixed through the test data in the examples folder
- CI checks run automatically to ensure the code is testable and reproducible

## CI Check Instructions
- GitHub Actions is configured to automatically run pytest tests and evaluation scripts on each commit
- A green check mark will be displayed after the tests pass, ensuring the code quality meets the course requirements

## Deliverables Checklist (Consistent with Course Delivery Checklist)
1.  GitHub Repository: This repository (public with initial commit)
2.  Folder Structure: 6 standard folders (specs, src, tests, etc.)
3.  Spec Templates: 6 specification documents (PRD.md, etc., with structured content)
4.  One CI Check: GitHub Actions + pytest (configured and runnable automatically)
5.  Runnable README: This file (including setup, running, and testing instructions)
