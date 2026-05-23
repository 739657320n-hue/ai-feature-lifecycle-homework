# Data Specification

## 1. Data Sources
- **POP909**: 909 Chinese pop piano MIDI, CC BY-NC-SA 4.0 (filtered to 832 usable)
- **MAESTRO v3.0.0**: >200h classical piano, CC BY-NC-SA 4.0 (filtered to 1024 records)

## 2. Schema & Semantic
Each note encoded as 5-tuple: `(pitch [0,127], onset_tick, duration_tick, velocity [0,127], chord_root)`
Tempo range: 60-140 BPM.
All sequences quantized at 96 ticks per quarter note.

## 3. Inclusion/Exclusion Criteria
- Include: ≥32 bars, ≥2 simultaneous notes, explicit tempo, 4/4 time signature
- Exclude: non-4/4, missing chord labels

## 4. Data Versioning
- Version format: `pop909_v1.0`, `maestro_v3.0.0` tracked via DVC or git-lfs.
- Every training run references exact data version in config.

## 5. Labeling (if human)
No human labeling needed; chord labels extracted automatically via `pychord`.

## 6. Data Distribution
- 65% major key, 35% minor.
- Inverse frequency weighted loss used during training.