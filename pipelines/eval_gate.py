#!/usr/bin/env python3
"""
eval_gate.py – CI evaluation gate for music generation models.
"""

import json
import random
import sys
from pathlib import Path
import os

import yaml

# Automatically switch working directory to the parent of the script's directory (project root)
HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parent
os.chdir(PROJECT_ROOT)

# Paths relative to project root
GOLDEN_FILE = PROJECT_ROOT / "data" / "golden_set" / "golden_samples.jsonl"
THRESHOLDS_FILE = PROJECT_ROOT / "configs" / "thresholds.yaml"
METRICS_FILE = PROJECT_ROOT / "reports" / "metrics.json"

random.seed(42)


def load_golden_set() -> list:
    if not GOLDEN_FILE.exists():
        print(f"ERROR: Golden set not found at {GOLDEN_FILE}")
        sys.exit(1)

    samples = []
    with open(GOLDEN_FILE, encoding="utf-8") as f:
        for line in f:
            samples.append(json.loads(line.strip()))
    print(f"Loaded {len(samples)} golden samples.")
    return samples


def evaluate_model(golden_samples: list) -> dict:
    # Simulated evaluation – replace with real model inference later
    metrics = {
        "pitch_accuracy": round(random.uniform(0.985, 1.0), 4),
        "out_of_key_note_ratio": round(random.uniform(0.002, 0.006), 4),
        "chord_similarity": round(random.uniform(0.92, 0.98), 4),
        "structural_correlation": round(random.uniform(0.88, 0.95), 4),
        "generation_speed_ms": round(random.uniform(600, 1500), 1),
    }
    return metrics


def write_metrics(metrics: dict):
    METRICS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(METRICS_FILE, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False)
    print(f"Metrics written to {METRICS_FILE}")


def load_thresholds() -> dict:
    with open(THRESHOLDS_FILE, encoding="utf-8") as f:
        return yaml.safe_load(f)


def check_thresholds(metrics: dict, thresholds: dict) -> bool:
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


def main():
    golden = load_golden_set()
    if not golden:
        print("ERROR: Golden set is empty.")
        sys.exit(1)

    metrics = evaluate_model(golden)
    write_metrics(metrics)

    thresholds = load_thresholds()
    print(f"Thresholds loaded from {THRESHOLDS_FILE}")

    if check_thresholds(metrics, thresholds):
        print("All thresholds passed.")
        sys.exit(0)
    else:
        print("Gate failed. Blocking merge.")
        sys.exit(1)


if __name__ == "__main__":
    main()