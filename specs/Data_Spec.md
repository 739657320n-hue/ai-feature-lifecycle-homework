# Data Specification

## 1. Data Sources

| Source | Description | License | Records |
|--------|-------------|---------|---------|
| **POP909** | 909 Chinese pop piano MIDI files (CC BY-NC-SA 4.0) | CC BY-NC-SA 4.0 | Filtered to 832 usable segments |
| **MAESTRO v3.0.0** | >200h classical piano performances (CC BY-NC-SA 4.0) | CC BY-NC-SA 4.0 | Filtered to 1024 segments |

Both sources are processed and merged into a unified dataset with two modalities:
- **audio_features.csv** — audio features extracted from each segment
- **note_sequences.jsonl** — symbolic note sequences for each segment

## 2. Schema & Semantics

### File: `audio_features.csv`

| Column | Type | Description | Constraints |
|--------|------|-------------|-------------|
| `segment_id` | string | Unique identifier | Pattern `seg_XXX` (3 digits) |
| `duration_sec` | float | Duration in seconds | 5.0 – 30.0 |
| `bpm` | int | Beats per minute | 40 – 200 |
| `key` | string | Musical key (e.g., `C_major`, `A_minor`) | Must be valid key signature |
| `genre` | string | Genre label | One of: `pop`, `classical`, `jazz`, `rock` |
| `mood` | string | Mood label | One of: `sad`, `calm`, `energetic`, `happy` |
| `time_signature` | string | Time signature | Only `4/4` |
| `mfcc_mean_1` … `mfcc_mean_13` | float | MFCC feature means (13 bands) | Normalized, typical range [-5, 5] |
| `chroma_1` … `chroma_12` | float | Chroma features (12 pitch classes) | [0.0, 1.0] |
| `spectral_contrast_1` … `spectral_contrast_7` | float | Spectral contrast in 7 bands | Unbounded |
| `tempo_confidence` | float | Confidence of tempo estimation | 0.0 – 1.0 |
| `beat_count` | int | Number of detected beats | >0 |
| `zero_crossing_rate` | float | Zero crossing rate | [0, 1] |
| `spectral_centroid` | float | Spectral centroid (Hz) | Positive |
| `spectral_bandwidth` | float | Spectral bandwidth | Positive |
| `spectral_rolloff` | float | Spectral rolloff frequency | Positive |

### File: `note_sequences.jsonl`

Each line is a JSON object with the following keys:

| Key | Type | Description |
|-----|------|-------------|
| `segment_id` | string | Links to `audio_features.csv` |
| `notes` | list of objects | Each note: `{pitch [0-127], start (sec), duration (sec), velocity [0-127]}` |
| `time_signature` | string | Always `"4/4"` |
| `tempo_changes` | list | Each entry: `{time (sec), bpm (int)}` |

## 3. Inclusion/Exclusion Criteria

- **Include**: Segments with ≥32 bars, ≥2 simultaneous notes, explicit tempo, 4/4 time signature
- **Exclude**: Segments with missing chord labels, non‑4/4 time signatures, corrupted audio

## 4. Data Versioning

- Naming: `v{major}.{minor}` (e.g., `v1.0`)
- Each dataset version is tracked via Git LFS (or DVC) and linked to a specific commit in `config.yaml`
- Version history is maintained in `CHANGELOG.md`

## 5. Labeling (Automatic)

- Chord labels extracted programmatically using `pychord`
- No human annotation involved
- Quality: verified by cross‑checking with ground‑truth key annotations from source datasets

## 6. Data Distribution

- **Key distribution**: 65% major, 35% minor
- **Genre distribution**: pop ~25%, classical ~25%, jazz ~25%, rock ~25%
- **Mood distribution**: balanced across 4 moods
- **Training strategy**: inverse frequency weighted loss used for class imbalance

## 7. Sample Size

- `audio_features.csv`: 20 rows (sample dataset)
- `note_sequences.jsonl`: 20 JSON lines (sample dataset)
- Full production dataset (not included here) contains 1856 segments total.