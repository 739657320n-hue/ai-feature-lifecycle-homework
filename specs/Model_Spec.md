# Model Specification – Music Generation Transformer

## 1. Baseline Model: Random Music Generator

### 1.1 Description
- **Type**: Rule-based random generation
- **Purpose**: Provide a fixed, reproducible starting point for comparison
- **Performance** (measured on golden set, 5 runs):
  - Generation speed: 0.01 ms per note
  - Structure score: 0.30 ± 0.05 (0–1 scale, automated metric)
  - Style consistency: 0.20 ± 0.05 (0–1 scale, automated metric)

### 1.2 Implementation
- Notes drawn uniformly from MIDI pitch range 48–84
- Duration: random choice of quarter, half, or whole note
- Velocity: uniform in [60, 100]
- No training required – purely rule-based

### 1.3 Strengths & Limitations
- ✅ Extremely fast, deterministic, always works
- ❌ No musical structure, poor quality, random output

---

## 2. Challenger Model: Transformer Music Generator

### 2.1 Architecture
- **Model Type**: Transformer encoder-decoder with attention
- **Input**: Note embeddings (pitch, duration, velocity) + positional encoding
- **Layers**: 4 encoder, 4 decoder
- **Hidden Size**: 256
- **Attention Heads**: 8

### 2.2 Training Configuration (expected)
- **Training Data**: 20 music segments from HW3 (versioned)
- **Epochs**: 50
- **Batch Size**: 4
- **Learning Rate**: 1e-4
- **Loss**: Cross-entropy over note vocabulary
- **Validation**: 3 segments (fixed IDs)

### 2.3 Target Performance
- **Pitch Accuracy**: ≥99%
- **Out-of-key Note Ratio**: ≤0.5%
- **Chord Similarity (cosine)**: ≥0.90
- **Structural Correlation**: ≥0.85

---

## 3. Applicability Limits

### 3.1 Domain Constraints (hard limits)
- Music length: 8–15 seconds (as in HW3)
- Tempo: 80–160 BPM
- Supported genres: pop, classical, jazz, rock
- Output format: MIDI-like note sequences (pitch, start, duration, velocity)

### 3.2 Quality Thresholds (soft targets)
- Structure score > 0.6
- Style consistency > 0.5
- Generation time < 2 s per segment (on CPU)

### 3.3 Out-of-scope
- Vocals, lyrics, timbre, instrument selection
- Real-time generation (< 100 ms)
- Polyphonic with >4 simultaneous voices

---

## 4. Resource Envelope

### 4.1 Training
- **Time**: ≤5 minutes on a CPU (e.g., Intel i7)
- **Memory**: ≤1 GB RAM
- **Storage**: ≤50 MB for checkpoints + logs

### 4.2 Inference
- **Latency**: ≤1 s per 10‑second segment on CPU
- **Memory**: ≤200 MB RAM
- **Throughput**: ≥10 segments/second on GPU (optional)

---

## 5. Update Policy

### 5.1 Triggers
1. Performance degradation on golden set (any metric drops by >1% absolute)
2. Requirement for new genres (e.g., electronic)
3. Infrastructure or dependency changes that affect reproducibility

### 5.2 Testing Requirements
- Must pass golden set regression tests (see EvalPlan.md)
- Must not regress in generation speed beyond tolerance
- Must improve or maintain all four primary metrics vs baseline

### 5.3 Versioning
- Model checkpoints tagged with Git SHA + experiment ID
- Golden set versioned via `data/golden_set/metadata.json`