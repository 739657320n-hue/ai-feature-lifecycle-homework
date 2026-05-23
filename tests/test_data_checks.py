#!/usr/bin/env python3
"""
Data Quality Checks - Music Generation Project (pytest version).
Contains 14 tests: syntactic, structural, and statistical checks.
"""

import json
import os
import re
from pathlib import Path

import pandas as pd
import pytest


# ---- Fixtures ----
@pytest.fixture(scope="module")
def data_loader():
    """Load CSV, JSONL data and split files once for all tests."""
    class Data:
        csv_path = Path(__file__).parent.parent / "data" / "raw" / "audio_features.csv"
        jsonl_path = Path(__file__).parent.parent / "data" / "raw" / "note_sequences.jsonl"
        splits_dir = Path(__file__).parent.parent / "data" / "splits"

        df = pd.read_csv(csv_path)
        segment_ids = df["segment_id"].tolist()

        jsonl_data = []
        with open(jsonl_path, "r") as f:
            for line in f:
                jsonl_data.append(json.loads(line.strip()))

    return Data()


# ---- Syntactic checks ----
class TestSyntacticChecks:

    def test_csv_file_exists(self, data_loader):
        assert data_loader.csv_path.exists(), "CSV file does not exist"
        assert os.path.getsize(data_loader.csv_path) > 0, "CSV file is empty"

    def test_jsonl_file_exists(self, data_loader):
        assert data_loader.jsonl_path.exists(), "JSONL file does not exist"
        assert os.path.getsize(data_loader.jsonl_path) > 0, "JSONL file is empty"

    def test_csv_format_correct(self, data_loader):
        required_columns = [
            "segment_id", "duration_sec", "bpm", "key",
            "genre", "mood", "time_signature"
        ]
        for col in required_columns:
            assert col in data_loader.df.columns, f"Missing required column: {col}"
        assert len(data_loader.df) == 20, f"Expected 20 rows, got {len(data_loader.df)}"

    def test_note_sequence_validity(self, data_loader):
        invalid_notes = []
        for item in data_loader.jsonl_data:
            seg_id = item["segment_id"]
            for i, note in enumerate(item["notes"]):
                if not (0 <= note["pitch"] <= 127):
                    invalid_notes.append(f"{seg_id}-note{i}: pitch={note['pitch']}")
                if note["start"] < 0:
                    invalid_notes.append(f"{seg_id}-note{i}: negative start")
                if note["duration"] <= 0:
                    invalid_notes.append(f"{seg_id}-note{i}: non-positive duration")
                if not (0 <= note["velocity"] <= 127):
                    invalid_notes.append(f"{seg_id}-note{i}: velocity={note['velocity']} out of range")
        assert len(invalid_notes) == 0, f"Invalid notes: {invalid_notes}"


# ---- Structural checks ----
class TestStructuralChecks:

    def test_no_missing_values(self, data_loader):
        missing = data_loader.df.isnull().sum().sum()
        assert missing == 0, f"Missing values found in CSV"
        for item in data_loader.jsonl_data:
            assert "segment_id" in item, "JSONL missing segment_id"
            assert "notes" in item, "JSONL missing notes"
            assert len(item["notes"]) > 0, "Empty notes"

    def test_segment_id_format(self, data_loader):
        pattern = r"^seg_\d{3}$"
        for seg_id in data_loader.df["segment_id"]:
            assert re.match(pattern, seg_id), f"Bad segment_id: {seg_id}"
        for item in data_loader.jsonl_data:
            assert re.match(pattern, item["segment_id"]), f"Bad JSONL segment_id: {item['segment_id']}"

    def test_no_duplicate_segment_ids(self, data_loader):
        dup_csv = data_loader.df[data_loader.df.duplicated("segment_id")]["segment_id"].tolist()
        assert len(dup_csv) == 0, f"Duplicates in CSV: {dup_csv}"
        jsonl_ids = [item["segment_id"] for item in data_loader.jsonl_data]
        assert len(jsonl_ids) == len(set(jsonl_ids)), "Duplicates in JSONL"

    def test_cross_file_consistency(self, data_loader):
        csv_ids = set(data_loader.df["segment_id"])
        jsonl_ids = set(item["segment_id"] for item in data_loader.jsonl_data)
        assert csv_ids == jsonl_ids, "Segment ID sets differ between CSV and JSONL"
        for seg_id in csv_ids:
            row = data_loader.df[data_loader.df["segment_id"] == seg_id].iloc[0]
            item = next(it for it in data_loader.jsonl_data if it["segment_id"] == seg_id)
            max_end = max(n["start"] + n["duration"] for n in item["notes"])
            assert abs(row["duration_sec"] - max_end) <= 0.5, \
                f"Duration mismatch for {seg_id}: CSV={row['duration_sec']}, JSONL_max_end={max_end}"

    def test_splits_exist_and_valid(self, data_loader):
        split_files = ["train_ids.txt", "val_ids.txt", "test_ids.txt"]
        for fname in split_files:
            path = data_loader.splits_dir / fname
            assert path.exists(), f"Missing {fname}"
            ids = [line.strip() for line in open(path) if line.strip()]
            assert len(ids) > 0, f"Empty {fname}"
            for seg_id in ids:
                assert re.match(r"^seg_\d{3}$", seg_id), f"Bad ID in {fname}: {seg_id}"

    def test_no_data_leakage(self, data_loader):
        splits = {}
        for split in ["train", "val", "test"]:
            path = data_loader.splits_dir / f"{split}_ids.txt"
            with open(path) as f:
                splits[split] = set(line.strip() for line in f if line.strip())
        assert len(splits["train"] & splits["val"]) == 0, "Train/val overlap"
        assert len(splits["train"] & splits["test"]) == 0, "Train/test overlap"
        assert len(splits["val"] & splits["test"]) == 0, "Val/test overlap"
        all_ids = splits["train"] | splits["val"] | splits["test"]
        assert all_ids == set(data_loader.segment_ids), "Splits do not cover all IDs"


# ---- Statistical checks ----
class TestStatisticalChecks:

    def test_genre_distribution(self, data_loader):
        counts = data_loader.df["genre"].value_counts()
        for g in ["pop", "classical", "jazz", "rock"]:
            assert g in counts.index, f"Missing genre {g}"
            assert counts[g] >= 2, f"Genre {g} has {counts[g]} samples (<2)"

    def test_bpm_range_validity(self, data_loader):
        bpm = data_loader.df["bpm"]
        assert bpm.min() >= 40, f"BPM too low: {bpm.min()}"
        assert bpm.max() <= 200, f"BPM too high: {bpm.max()}"
        assert bpm.nunique() >= 3, f"Only {bpm.nunique()} unique BPMs"

    def test_duration_distribution(self, data_loader):
        dur = data_loader.df["duration_sec"]
        assert dur.min() >= 5.0, f"Min duration {dur.min()} < 5s"
        assert dur.max() <= 30.0, f"Max duration {dur.max()} > 30s"
        mean_dur = dur.mean()
        assert 8.0 <= mean_dur <= 15.0, f"Mean duration {mean_dur:.1f}s out of [8,15]"

    def test_feature_value_ranges(self, data_loader):
        mfcc_cols = [c for c in data_loader.df.columns if "mfcc_mean" in c]
        for col in mfcc_cols:
            values = data_loader.df[col]
            assert values.abs().max() < 10, f"MFCC {col} has large value {values.abs().max()}"
        chroma_cols = [c for c in data_loader.df.columns if "chroma" in c]
        for col in chroma_cols:
            values = data_loader.df[col]
            assert values.min() >= 0, f"Chroma {col} has negative {values.min()}"
            assert values.max() <= 1, f"Chroma {col} exceeds 1: {values.max()}"