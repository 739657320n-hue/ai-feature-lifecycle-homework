#!/usr/bin/env python3
"""
eval_gate.py – CI evaluation gate for music generation models.
Now a pytest test file. Run with: python -m pytest pipelines/eval_gate.py
"""

import json
import random
from pathlib import Path
import os
import shutil

import pytest
import yaml

# Automatically switch working directory to the parent of the script's directory (project root)
HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parent
os.chdir(PROJECT_ROOT)

# Default paths (adjust if needed in tests)
GOLDEN_FILE = PROJECT_ROOT / "data" / "golden_set" / "golden_samples.jsonl"
THRESHOLDS_FILE = PROJECT_ROOT / "configs" / "thresholds.yaml"
REPORTS_DIR = PROJECT_ROOT / "reports"
METRICS_FILE = REPORTS_DIR / "metrics.json"

random.seed(42)


# ----------------------------------------------------------------------
# Helper functions (unchanged logic)
# ----------------------------------------------------------------------

def load_golden_set(path: Path = GOLDEN_FILE) -> list:
    """Load golden samples from a JSONL file."""
    if not path.exists():
        raise FileNotFoundError(f"Golden set not found at {path}")
    samples = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            samples.append(json.loads(line.strip()))
    print(f"Loaded {len(samples)} golden samples.")
    return samples


def evaluate_model(golden_samples: list) -> dict:
    """Simulated evaluation – replace with real model inference later."""
    metrics = {
        "pitch_accuracy": round(random.uniform(0.985, 1.0), 4),
        "out_of_key_note_ratio": round(random.uniform(0.002, 0.006), 4),
        "chord_similarity": round(random.uniform(0.92, 0.98), 4),
        "structural_correlation": round(random.uniform(0.88, 0.95), 4),
        "generation_speed_ms": round(random.uniform(600, 1500), 1),
    }
    return metrics


def write_metrics(metrics: dict, metrics_path: Path = METRICS_FILE):
    """Write metrics to a JSON file."""
    metrics_path.parent.mkdir(parents=True, exist_ok=True)
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False)
    print(f"Metrics written to {metrics_path}")


def load_thresholds(thresholds_path: Path = THRESHOLDS_FILE) -> dict:
    """Load threshold configuration from YAML file."""
    if not thresholds_path.exists():
        raise FileNotFoundError(f"Thresholds file not found at {thresholds_path}")
    with open(thresholds_path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def check_thresholds(metrics: dict, thresholds: dict) -> bool:
    """Check metrics against absolute thresholds. Returns True if all pass."""
    abs_thresh = thresholds.get("absolute", {})
    passed = True
    for metric, config in abs_thresh.items():
        if metric not in metrics:
            continue
        if "min" in config and metrics[metric] < config["min"]:
            print(f"FAIL: {metric} = {metrics[metric]} < {config['min']}")
            passed = False
        if "max" in config and metrics[metric] > config["max"]:
            print(f"FAIL: {metric} = {metrics[metric]} > {config['max']}")
            passed = False
    return passed


def run_gate(golden_path: Path = GOLDEN_FILE,
             thresholds_path: Path = THRESHOLDS_FILE,
             metrics_path: Path = METRICS_FILE) -> bool:
    """
    Execute the full evaluation gate:
    1. Load golden set
    2. Evaluate model (simulated)
    3. Write metrics
    4. Load thresholds
    5. Check thresholds
    Returns True if all thresholds pass, False otherwise.
    """
    golden = load_golden_set(golden_path)
    if not golden:
        raise ValueError("Golden set is empty.")

    metrics = evaluate_model(golden)
    write_metrics(metrics, metrics_path)

    thresholds = load_thresholds(thresholds_path)
    print(f"Thresholds loaded from {thresholds_path}")

    return check_thresholds(metrics, thresholds)


# ----------------------------------------------------------------------
# Pytest tests
# ----------------------------------------------------------------------

class TestEvalGate:

    @pytest.fixture(autouse=True)
    def setup_teardown(self, tmp_path: Path):
        """Use a temporary directory for generated metrics to avoid polluting real reports folder."""
        self.golden_file = tmp_path / "golden_samples.jsonl"
        self.metrics_file = tmp_path / "metrics.json"
        self.thresholds_file = tmp_path / "thresholds.yaml"

        # Create a minimal golden set
        golden_samples = [
            {"id": 1, "prompt": "jazz piano", "expected_pitch_accuracy": 0.99},
            {"id": 2, "prompt": "lofi beat",  "expected_pitch_accuracy": 0.97}
        ]
        with open(self.golden_file, "w", encoding="utf-8") as f:
            for sample in golden_samples:
                f.write(json.dumps(sample) + "\n")

        # Create a minimal thresholds file
        thresholds = {
            "absolute": {
                "pitch_accuracy": {"min": 0.95},
                "out_of_key_note_ratio": {"max": 0.01},
                "chord_similarity": {"min": 0.90},
                "structural_correlation": {"min": 0.85},
                "generation_speed_ms": {"max": 2000}
            }
        }
        with open(self.thresholds_file, "w", encoding="utf-8") as f:
            yaml.safe_dump(thresholds, f)

        yield

        # Clean up (tmp_path is automatically removed by pytest)

    def test_load_golden_set_valid(self):
        """Test loading a valid golden set."""
        samples = load_golden_set(self.golden_file)
        assert len(samples) == 2
        assert samples[0]["prompt"] == "jazz piano"

    def test_load_golden_set_missing_file(self):
        """Test that missing file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            load_golden_set(Path("/nonexistent/path.jsonl"))

    def test_evaluate_model_returns_expected_keys(self):
        """Test that evaluate_model returns all required metrics."""
        samples = load_golden_set(self.golden_file)
        metrics = evaluate_model(samples)
        required_keys = {"pitch_accuracy", "out_of_key_note_ratio", "chord_similarity",
                         "structural_correlation", "generation_speed_ms"}
        assert required_keys.issubset(metrics.keys())

    def test_write_metrics_creates_file(self):
        """Test that write_metrics actually creates a JSON file."""
        metrics = {"test_metric": 0.99}
        write_metrics(metrics, self.metrics_file)
        assert self.metrics_file.exists()
        with open(self.metrics_file, encoding="utf-8") as f:
            data = json.load(f)
            assert data == metrics

    def test_check_thresholds_pass(self):
        """Test that thresholds are correctly checked for passing metrics."""
        thresholds = {"absolute": {"pitch_accuracy": {"min": 0.90}}}
        metrics = {"pitch_accuracy": 0.95}
        assert check_thresholds(metrics, thresholds) is True

    def test_check_thresholds_fail(self):
        """Test that thresholds correctly detect a failing metric."""
        thresholds = {"absolute": {"pitch_accuracy": {"min": 0.99}}}
        metrics = {"pitch_accuracy": 0.95}
        assert check_thresholds(metrics, thresholds) is False

    def test_run_gate_passes_with_valid_data(self):
        """Integration test: the full gate should pass with golden set and thresholds defined above."""
        result = run_gate(
            golden_path=self.golden_file,
            thresholds_path=self.thresholds_file,
            metrics_path=self.metrics_file
        )
        # With random.seed(42) and the thresholds we created, the simulated metrics should all pass.
        assert result is True

    def test_run_gate_fails_on_empty_golden_set(self):
        """Test that an empty golden set raises an error."""
        empty_file = self.golden_file.parent / "empty.jsonl"
        empty_file.write_text("", encoding="utf-8")
        with pytest.raises(ValueError, match="Golden set is empty"):
            run_gate(golden_path=empty_file)

    def test_run_gate_fails_on_missing_thresholds(self):
        """Test that missing thresholds file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            run_gate(
                golden_path=self.golden_file,
                thresholds_path=Path("/nonexistent/thresholds.yaml")
            )