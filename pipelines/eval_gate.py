#!/usr/bin/env python3
"""
Create golden set for HW4 evaluation.
Simple version - selects samples from HW3 data.
"""

import json
import random
import os
from pathlib import Path


def create_simple_golden_set():
    """Create simple golden set from HW3 data"""
    print("Creating simple golden set for HW4...")

    # Create golden set directory
    golden_dir = Path("data/golden_set")
    golden_dir.mkdir(parents=True, exist_ok=True)

    # Simulate loading HW3 data
    # In reality, you would load the actual CSV/JSONL files
    print("Loading HW3 data (simulated)...")

    # Create simulated sample data matching HW3 format
    golden_samples = []

    # Define the same genres as HW3
    genres = ["pop", "classical", "jazz", "rock"]

    # Create 5 samples per genre (total 20)
    sample_id = 1
    for genre in genres:
        for i in range(5):
            # Create a simple note sequence
            notes = []
            for note_idx in range(10):
                notes.append({
                    "pitch": random.randint(60, 72),
                    "start": note_idx * 0.5,
                    "duration": 0.5,
                    "velocity": 80
                })

            sample = {
                "golden_id": f"golden_{sample_id:03d}",
                "segment_id": f"seg_{sample_id:03d}",
                "genre": genre,
                "bpm": random.choice([80, 100, 120, 140]),
                "duration_sec": 5.0,
                "notes": notes,
                "is_golden": True
            }

            golden_samples.append(sample)
            sample_id += 1

    # Save golden set as JSONL
    golden_path = golden_dir / "golden_samples.jsonl"
    with open(golden_path, "w") as f:
        for sample in golden_samples:
            f.write(json.dumps(sample) + "\n")

    print(f"Created {len(golden_samples)} golden samples")
    print(f"Saved to: {golden_path}")

    # Create simple metadata
    metadata = {
        "description": "Golden set for HW4 evaluation",
        "num_samples": len(golden_samples),
        "genres": genres,
        "samples_per_genre": 5
    }

    meta_path = golden_dir / "metadata.json"
    with open(meta_path, "w") as f:
        json.dump(metadata, f, indent=2)

    print(f"Metadata saved to: {meta_path}")

    return golden_samples


def main():
    """Main function"""
    print("=" * 60)
    print("HW4 Golden Set Creation")
    print("=" * 60)

    samples = create_simple_golden_set()

    print("\n" + "=" * 60)
    print("Golden set created successfully!")
    print(f"Total samples: {len(samples)}")
    print("Location: data/golden_set/")
    print("=" * 60)


if __name__ == "__main__":
    main()