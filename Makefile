# Music Generation Project - Makefile (English Version)

.PHONY: help setup generate-data data-check notebook dvc-init ci-run clean

# Default target
help:
	@echo "Music Generation Project - HW3 Data Pipeline"
	@echo ""
	@echo "Available commands:"
	@echo "  make setup          Install dependencies"
	@echo "  make generate-data  Generate simulated music data"
	@echo "  make data-check     Run data quality checks"
	@echo "  make notebook       Start Jupyter notebook"
	@echo "  make dvc-init       Initialize DVC"
	@echo "  make ci-run         Run full CI pipeline"
	@echo "  make clean          Clean generated files"

# Install dependencies
setup:
	@echo "Installing Python dependencies..."
	pip install pandas numpy matplotlib seaborn jupyter
	@echo "Installing test dependencies..."
	pip install pytest pytest-cov
	@echo "Creating directory structure..."
	mkdir -p data/splits notebooks reports
	@echo "Setup completed!"

# Generate simulated data
generate-data:
	@echo "Generating simulated music data..."
	python data/generate_music_data.py

# Run data quality checks
data-check:
	@echo "Running data quality checks..."
	python tests/test_data_checks.py

# Start Jupyter notebook
notebook:
	@echo "Starting Jupyter notebook..."
	jupyter notebook notebooks/data_analysis.ipynb

# Initialize DVC
dvc-init:
	@echo "Initializing DVC..."
	dvc init
	@echo "Adding data files to DVC..."
	dvc add data/audio_features.csv
	dvc add data/note_sequences.jsonl
	@echo "Adding .gitignore rules..."
	echo "/data/audio_features.csv" >> .gitignore
	echo "/data/note_sequences.jsonl" >> .gitignore
	echo "!data/*.dvc" >> .gitignore
	@echo "DVC initialization completed!"

# Run full CI pipeline
ci-run: generate-data data-check
	@echo "CI pipeline completed successfully!"

# Clean generated files
clean:
	@echo "Cleaning generated files..."
	rm -f data/audio_features.csv
	rm -f data/note_sequences.jsonl
	rm -rf data/splits/*
	rm -rf reports/*
	rm -f .coverage
	@echo "Cleanup completed!"

# Additional targets for HW3 requirements
all: setup generate-data data-check dvc-init
	@echo "HW3 data pipeline completed!"

# Run tests with coverage
test-coverage:
	@echo "Running tests with coverage..."
	pytest tests/test_data_checks.py --cov=./ --cov-report=html
	@echo "Coverage report generated in htmlcov/"

# Generate data analysis report
analysis-report:
	@echo "Generating data analysis report..."
	python -c "import pandas as pd; import json; df=pd.read_csv('data/audio_features.csv'); report={'total_samples':len(df), 'columns':list(df.columns), 'summary':df.describe().to_dict()}; open('reports/data_summary.json','w').write(json.dumps(report,indent=2))"
	@echo "Report saved to reports/data_summary.json"

# Validate data contract
validate-contract: data-check
	@echo "Data contract validation completed!"