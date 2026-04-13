#!/usr/bin/env python3
"""
Mock MLflow experiment tracker.
Simulates experiment tracking without actual MLflow dependency.
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
import hashlib


class MockMLflowTracker:
    """Mock MLflow tracker for experiment logging"""

    def __init__(self, tracking_uri: str = "mock_mlruns"):
        """Initialize mock tracker"""
        self.tracking_uri = tracking_uri
        self.active_run = None
        self.experiment_id = "exp_001"

        # Create mock directory structure
        Path(tracking_uri).mkdir(exist_ok=True)
        print(f"Mock MLflow initialized at: {tracking_uri}")

    def start_run(self, run_name: str = None, experiment_id: str = None):
        """Start a new mock run"""
        run_id = hashlib.md5(str(time.time()).encode()).hexdigest()[:8]
        self.active_run = {
            "run_id": run_id,
            "run_name": run_name or f"run_{run_id}",
            "experiment_id": experiment_id or self.experiment_id,
            "start_time": datetime.now().isoformat(),
            "params": {},
            "metrics": {},
            "tags": {},
            "artifacts": []
        }

        print(f"Started run: {self.active_run['run_name']} ({run_id})")
        return self.active_run

    def log_param(self, key: str, value: Any):
        """Log a parameter"""
        if self.active_run:
            self.active_run["params"][key] = value
            print(f"Logged param: {key} = {value}")

    def log_metric(self, key: str, value: float, step: int = None):
        """Log a metric"""
        if self.active_run:
            if step is not None:
                key = f"{key}_step{step}"
            self.active_run["metrics"][key] = value
            print(f"Logged metric: {key} = {value}")

    def log_artifact(self, local_path: str):
        """Log an artifact"""
        if self.active_run:
            self.active_run["artifacts"].append(local_path)
            print(f"Logged artifact: {local_path}")

    def set_tag(self, key: str, value: Any):
        """Set a tag"""
        if self.active_run:
            self.active_run["tags"][key] = value
            print(f"Set tag: {key} = {value}")

    def end_run(self):
        """End the current run"""
        if not self.active_run:
            print("No active run to end")
            return

        # Add end time
        self.active_run["end_time"] = datetime.now().isoformat()
        duration = (datetime.fromisoformat(self.active_run["end_time"]) -
                    datetime.fromisoformat(self.active_run["start_time"]))
        self.active_run["duration_seconds"] = duration.total_seconds()

        # Save run data
        run_id = self.active_run["run_id"]
        run_dir = Path(self.tracking_uri) / self.active_run["experiment_id"] / run_id
        run_dir.mkdir(parents=True, exist_ok=True)

        run_file = run_dir / "run_data.json"
        with open(run_file, 'w') as f:
            json.dump(self.active_run, f, indent=2)

        print(f"Ended run: {self.active_run['run_name']}")
        print(f"Run data saved to: {run_file}")

        # Print summary
        self._print_run_summary()

        # Clear active run
        ended_run = self.active_run
        self.active_run = None

        return ended_run

    def _print_run_summary(self):
        """Print run summary"""
        if not self.active_run:
            return

        print("\n" + "=" * 60)
        print(f"RUN SUMMARY: {self.active_run['run_name']}")
        print("=" * 60)

        print(f"Run ID: {self.active_run['run_id']}")
        print(f"Duration: {self.active_run.get('duration_seconds', 0):.1f}s")

        print("\nParameters:")
        for key, value in self.active_run['params'].items():
            print(f"  {key}: {value}")

        print("\nKey Metrics:")
        metrics = self.active_run['metrics']
        for key in sorted(metrics.keys()):
            if "_step" not in key:  # Skip step metrics in summary
                print(f"  {key}: {metrics[key]}")

        if self.active_run['artifacts']:
            print(f"\nArtifacts ({len(self.active_run['artifacts'])}):")
            for artifact in self.active_run['artifacts']:
                print(f"  - {artifact}")

        print("=" * 60)

    def compare_runs(self, run_ids: list):
        """Compare multiple runs"""
        print(f"\nComparing {len(run_ids)} runs:")

        # Mock comparison table
        comparison = {
            "run_ids": run_ids,
            "comparison_time": datetime.now().isoformat(),
            "results": "Mock comparison - use real MLflow for detailed analysis"
        }

        comparison_file = Path(
            self.tracking_uri) / "comparisons" / f"compare_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        comparison_file.parent.mkdir(parents=True, exist_ok=True)

        with open(comparison_file, 'w') as f:
            json.dump(comparison, f, indent=2)

        print(f"Comparison saved to: {comparison_file}")
        return comparison


def simulate_experiment():
    """Simulate a complete experiment"""
    print("Music Generation Experiment (Mock MLflow)")
    print("=" * 60)

    # Initialize tracker
    tracker = MockMLflowTracker("mock_mlruns")

    # Experiment 1: Baseline model
    print("\nExperiment 1: Baseline Model")
    run1 = tracker.start_run("baseline_evaluation")

    tracker.log_param("model_type", "random_generator")
    tracker.log_param("seed", 42)
    tracker.log_param("duration_seconds", 10.0)

    # Simulate evaluation metrics
    tracker.log_metric("generation_speed_ms", 10.0)
    tracker.log_metric("structure_score", 0.3)
    tracker.log_metric("style_consistency", 0.2)
    tracker.log_metric("overall_quality", 0.25)

    tracker.set_tag("model_family", "baseline")
    tracker.set_tag("status", "completed")

    tracker.log_artifact("models/baseline.py")

    baseline_result = tracker.end_run()

    # Experiment 2: Transformer model
    print("\nExperiment 2: Transformer Model")
    run2 = tracker.start_run("transformer_evaluation")

    tracker.log_param("model_type", "transformer")
    tracker.log_param("num_layers", 2)
    tracker.log_param("hidden_size", 128)
    tracker.log_param("training_epochs", 10)

    # Simulate better metrics
    tracker.log_metric("generation_speed_ms", 5.0)
    tracker.log_metric("structure_score", 0.75)
    tracker.log_metric("style_consistency", 0.65)
    tracker.log_metric("overall_quality", 0.70)

    # Training loss history (simulated)
    for epoch in range(10):
        loss = 2.0 * (0.85 ** epoch) + 0.1
        tracker.log_metric("training_loss", loss, step=epoch)

    tracker.set_tag("model_family", "transformer")
    tracker.set_tag("status", "completed")

    tracker.log_artifact("models/transformer_model.py")
    tracker.log_artifact("models/train.py")

    transformer_result = tracker.end_run()

    # Compare runs
    print("\nRun Comparison:")
    tracker.compare_runs([run1["run_id"], run2["run_id"]])

    # Summary
    print("\n" + "=" * 60)
    print("EXPERIMENT SUMMARY")
    print("=" * 60)
    print(f"Baseline - Overall Quality: {baseline_result['metrics'].get('overall_quality', 0):.3f}")
    print(f"Transformer - Overall Quality: {transformer_result['metrics'].get('overall_quality', 0):.3f}")

    improvement = ((transformer_result['metrics'].get('overall_quality', 0) -
                    baseline_result['metrics'].get('overall_quality', 0)) /
                   max(baseline_result['metrics'].get('overall_quality', 0.01), 0.01))

    print(f"Improvement: {improvement:.1%}")
    print("=" * 60)


if __name__ == "__main__":
    simulate_experiment()