# Dataset Card — Chinese Folk Music AI Generation Sample

## 1. Dataset Description

This dataset is a **sample** (20 segments) designed for a Chinese folk music AI generation project. It contains two modalities:
- **Audio features** (CSV): pre‑extracted features per segment (MFCCs, chroma, spectral contrast, tempo, etc.).
- **Note sequences** (JSONL): symbolic piano‑roll representations (pitch, start time, duration, velocity).

The full dataset (not included here) is constructed from two public sources: **POP909** (Chinese pop piano MIDI) and **MAESTRO v3.0.0** (classical piano performances), both under CC BY‑NC‑SA 4.0.

## 2. Purpose & Intended Use

- **Designed for**: Training and evaluating models that generate folk‑style piano music given audio features or symbolic conditioning.
- **Can be used for**: Music generation, style transfer, melody harmonization, genre classification (4 genres).
- **Not suitable for**: Voice synthesis, lyrics generation, music with complex instrumentation beyond solo piano.

## 3. Composition & Splits

| Split | Number of segments | Description |
|-------|-------------------|-------------|
| Sample (this card) | 20 | Balance across genres (pop, classical, jazz, rock) and moods (sad, calm, energetic, happy) |
| Full production | 1856 | Detailed split files in `data/splits/` (train/val/test at 80/10/10) |

Each segment is a 4/4 time signature, 40–200 BPM, 5–30 seconds long.

## 4. Collection & Processing

- **Source 1 — POP909**: 909 Chinese pop piano MIDI files. Filtered to 832 segments that meet: ≥32 bars, ≥2 simultaneous notes, explicit tempo, 4/4 time.
- **Source 2 — MAESTRO v3.0.0**: Over 200 hours of classical piano performances. Filtered to 1024 segments with same criteria.
- **Audio feature extraction**: Using `librosa` – MFCC (13 bands), chroma (12), spectral contrast (7), tempo, zero‑crossing rate, spectral centroid/bandwidth/rolloff.
- **Label extraction**: Genre, mood, key labels are derived from original metadata (POP909 includes style tags; MAESTRO includes composer/era mood mapping).

## 5. Annotation Method

- **Fully automatic**: No human annotators.
- Key and chord labels extracted via `pychord` library.
- Genre/mood mapping: based on rule‑based heuristics from source metadata (e.g., pieces marked “sad” in MAESTRO are tagged as `mood=sad`).
- Quality assured by manual spot‑check of 5% of full dataset (not needed for sample).

## 6. Known Limitations & Biases

- **Genre coverage**: Only 4 genres (pop, classical, jazz, rock). Folk‑specific styles (e.g., guzheng, erhu) are **not** yet represented in this version.
- **Mood imbalance**: While balanced in sample, full dataset may show minor skew toward energetic moods due to source material.
- **Instrument**: All recordings are solo piano. No multi‑instrument or vocal data.
- **Cultural bias**: POP909 and MAESTRO are Western / Chinese‑pop oriented; traditional Chinese folk music is underrepresented.
- **Key distribution**: 65% major keys – minor keys may be less represented, affecting minor‑key generation performance.
- **Duration**: Segments are short (5–30s), limiting ability to generate long‑form compositions.

## 7. Versions

| Version | Date | Changes |
|---------|------|---------|
| v1.0 | 2025-03-19 | Initial sample release (20 segments) for HW3 validation |
| v1.1 (planned) | TBD | Full 1856‑segment release; add traditional Chinese instrument labels |

---

**Contact**: Project team (see repository README)  
**License**: CC BY‑NC‑SA 4.0 (inherited from source datasets)