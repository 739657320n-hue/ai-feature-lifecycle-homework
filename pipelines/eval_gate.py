#!/usr/bin/env python3
"""
eval_gate.py - Create golden set for evaluation (pytest version).
This script generates a synthetic golden dataset used for model evaluation.
"""

import json
import random
from pathlib import Path

# Test data constants
GENRES = ["pop", "classical", "jazz", "rock"]
SAMPLES_PER_GENRE = 5
TOTAL_SAMPLES = len(GENRES) * SAMPLES_PER_GENRE

GOLDEN_DIR = Path("data/golden_set")
GOLDEN_PATH = GOLDEN_DIR / "golden_samples.jsonl"
METADATA_PATH = GOLDEN_DIR / "metadata.json"


def create_golden_sample(sample_id: int, genre: str) -> dict:
    """Create a single golden sample with random notes."""
    notes = []
    for note_idx in range(10):
        notes.append({
            "pitch": random.randint(60, 72),
            "start": note_idx * 0.5,
            "duration": 0.5,
            "velocity": 80
        })

    return {
        "golden_id": f"golden_{sample_id:03d}",
        "segment_id": f"seg_{sample_id:03d}",
        "genre": genre,
        "bpm": random.choice([80, 100, 120, 140]),
        "duration_sec": 5.0,
        "notes": notes,
        "is_golden": True
    }


def create_golden_set():
    """Generate the full golden set and save to disk."""
    GOLDEN_DIR.mkdir(parents=True, exist_ok=True)

    samples = []
    sample_id = 1
    for genre in GENRES:
        for _ in range(SAMPLES_PER_GENRE):
            samples.append(create_golden_sample(sample_id, genre))
            sample_id += 1

    with open(GOLDEN_PATH, "w") as f:
        for sample in samples:
            f.write(json.dumps(sample) + "\n")

    metadata = {
        "description": "Golden set for evaluation",
        "num_samples": len(samples),
        "genres": GENRES,
        "samples_per_genre": SAMPLES_PER_GENRE
    }
    with open(METADATA_PATH, "w") as f:
        json.dump(metadata, f, indent=2)

    return samples


# ---- pytest tests ----
import pytest


class TestGoldenSetCreation:
    """Tests for golden set creation."""

    @classmethod
    def setup_class(cls):
        # Ensure golden set is created before tests
        cls.samples = create_golden_set()

    def test_golden_set_exists(self):
        assert GOLDEN_PATH.exists(), "Golden set file not created"
        assert GOLDEN_PATH.stat().st_size > 0, "Golden set file is empty"

    def test_golden_metadata_exists(self):
        assert METADATA_PATH.exists(), "Metadata file not created"
        assert METADATA_PATH.stat().st_size > 0, "Metadata file is empty"

    def test_total_samples_count(self):
        assert len(self.samples) == TOTAL_SAMPLES, \
            f"Expected {TOTAL_SAMPLES} samples, got {len(self.samples)}"

    def test_genre_balance(self):
        from collections import Counter
        genre_counts = Counter(s["genre"] for s in self.samples)
        for genre in GENRES:
            assert genre_counts[genre] == SAMPLES_PER_GENRE, \
                f"Genre {genre} has {genre_counts.get(genre, 0)} samples, expected {SAMPLES_PER_GENRE}"

    def test_golden_id_format(self):
        import re
        pattern = r"^golden_\d{3}$"
        for s in self.samples:
            assert re.match(pattern, s["golden_id"]), \
                f"Invalid golden_id: {s['golden_id']}"

    def test_all_notes_valid(self):
        for s in self.samples:
            for note in s["notes"]:
                assert 0 <= note["pitch"] <= 127
                assert 0 <= note["start"]
                assert note["duration"] > 0
                assert 0 <= note["velocity"] <= 127

    def test_duration_consistent(self):
        for s in self.samples:
            max_end = max(n["start"] + n["duration"] for n in s["notes"])
            assert abs(s["duration_sec"] - max_end) <= 0.5, \
                f"Sample {s['golden_id']} duration mismatch"