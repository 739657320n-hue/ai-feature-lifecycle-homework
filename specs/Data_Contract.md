# Data Contract — Audio Feature & Note Sequence Dataset

## 1. Purpose & Scope
This contract defines the mandatory format, constraints, and quality standards for the music generation dataset composed of two files:
- `data/raw/audio_features.csv`
- `data/raw/note_sequences.jsonl`

Any dataset version that violates this contract **must be rejected** by the CI pipeline and cannot be used for model training.

## 2. Format Contract

### 2.1 General Rules
- All files must be UTF‑8 encoded.
- Line endings: Unix `\n`.
- No BOM (byte order mark).

### 2.2 `audio_features.csv`
| Rule | Specification |
|------|---------------|
| Delimiter | Comma `,` |
| Header | Required; field names exactly as in DataSpec |
| Rows | 10 – 50 (sample) / ≥1000 (production) |
| Missing values | Prohibited for all columns |
| Column order | Must be exactly: `segment_id, duration_sec, bpm, key, genre, mood, time_signature, mfcc_mean_1, …, chroma_12, …, spectral_contrast_7, tempo_confidence, beat_count, zero_crossing_rate, spectral_centroid, spectral_bandwidth, spectral_rolloff` |

### 2.3 `note_sequences.jsonl`
| Rule | Specification |
|------|---------------|
| Format | One valid JSON object per line |
| Fields per object | Must contain `segment_id`, `notes`, `time_signature`, `tempo_changes` |
| JSON validity | Every line must pass `json.loads()`; no trailing commas, no malformed keys |

## 3. Field‑Level Contract

### 3.1 `audio_features.csv` fields

| Column | Type | Constraints | Forbidden Values |
|--------|------|-------------|------------------|
| `segment_id` | string | Pattern `seg_\d{3}` | Null, non‑matching pattern |
| `duration_sec` | float | 5.0 ≤ value ≤ 30.0 | Null, <5.0, >30.0 |
| `bpm` | int | 40 ≤ value ≤ 200 | Null, decimals, outside range |
| `key` | string | Must be valid key: `{A..G}{_major|_minor}` | Null, non‑musical strings |
| `genre` | string | One of: `pop`, `classical`, `jazz`, `rock` | Null, any other value |
| `mood` | string | One of: `sad`, `calm`, `energetic`, `happy` | Null, any other value |
| `time_signature` | string | Only `4/4` | Null, `3/4`, `6/8`, etc. |
| `mfcc_mean_*` | float | `\|value\| < 10` | Null, non‑numeric |
| `chroma_*` | float | 0.0 ≤ value ≤ 1.0 | Null, <0, >1 |
| `tempo_confidence` | float | 0.0 ≤ value ≤ 1.0 | Null |
| `beat_count` | int | >0 | Null, ≤0 |
| `spectral_*` | float | Must be positive finite | Null, NaN, Inf |

### 3.2 `note_sequences.jsonl` fields

Each JSON line must satisfy:
| Field | Type | Constraints |
|-------|------|-------------|
| `segment_id` | string | Same pattern as in CSV; must exist in `audio_features.csv` |
| `notes` | list (min 1) | Each note is an object with `pitch`, `start`, `duration`, `velocity` |
| `notes[].pitch` | int | 0–127 |
| `notes[].start` | float | ≥0 |
| `notes[].duration` | float | >0 |
| `notes[].velocity` | int | 0–127 |
| `time_signature` | string | Only `"4/4"` |
| `tempo_changes` | list (min 1) | Each entry: `{time: float, bpm: int}` |

## 4. Quality Checks (Minimum 10)

### 4.1 Syntactic (3)
1. CSV file exists and is non‑empty.
2. JSONL file exists and is non‑empty.
3. All required columns present in CSV header.

### 4.2 Structural (4)
4. No missing values in CSV or JSONL.
5. No duplicate `segment_id` within or across files.
6. Cross‑file consistency: every `segment_id` in CSV appears in JSONL.
7. Train/val/test splits (if present) are disjoint and cover all IDs.

### 4.3 Statistical (3)
8. Each genre appears at least 2 times in sample (≥100 in production).
9. BPM range: at least 3 unique BPM values.
10. Mean duration within [8.0, 15.0] seconds.

## 5. CI Integration

- **Trigger**: On push to `dev-homework` or pull‑request to `main`.
- **Pipeline steps**:
  1. Checkout code
  2. Setup Python 3.10
  3. Install dependencies (pandas, pytest)
  4. Run `pytest test_data_checks.py` (all tests must pass)
- **Failure rule**: If any test fails, the CI status will be red and the dataset version is rejected.

## 6. Versioning

- Contract version follows dataset version (e.g., `v1.0`).
- Major: field addition/deletion, core constraint change.
- Minor: constraint refinement, additional checks.
- Each dataset release must reference the exact contract version it satisfies.

## 7. Contract Violation Handling

- Violations stop any model training using this dataset.
- Fix the data and re‑run CI until all checks pass.
- All changes to the contract must be logged in `CHANGELOG.md`.