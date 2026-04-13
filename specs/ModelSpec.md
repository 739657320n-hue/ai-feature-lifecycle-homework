# Model Specification - Music Generation Transformer

## 1. Baseline Model: Random Music Generator
### 1.1 Implementation
- **Type**: Rule-based random generation
- **Algorithm**: Random notes with basic constraints
- **Parameters**: 
  - Pitch range: 48-84 (C3 to C6)
  - Duration: Random quarter, half, or whole notes
  - Velocity: Random between 60-100
- **Performance**: 
  - Generation speed: ~0.01ms per note
  - Structure score: ~0.3 (on 0-1 scale)
  - Style consistency: ~0.2 (random)

### 1.2 Strengths & Limitations
- **Strengths**: Extremely fast, always works, no training needed
- **Limitations**: No musical structure, poor quality, random output

## 2. Challenger Model: Transformer Music Generator
### 2.1 Architecture
- **Model Type**: Transformer with attention mechanism
- **Input Encoding**: 
  - Note embeddings (pitch, duration, velocity)
  - Positional encoding for timing
- **Layers**: 4 encoder layers, 4 decoder layers
- **Hidden Size**: 256
- **Heads**: 8 attention heads

### 2.2 Training Configuration
- **Dataset**: 20 music segments from HW3
- **Batch Size**: 4
- **Epochs**: 50
# Model Specification - Simulated Music Generation

## 1. Baseline Model: Random Music Generator (Simulated)
### 1.1 Model Description
- **Type**: Rule-based random generation (simulated)
- **Purpose**: Simple baseline for comparison
- **Simulated Performance**:
  - Generation speed: 0.5ms per note (simulated)
  - Structure score: 0.35 ± 0.1 (random normal)
  - Style consistency: 0.25 ± 0.1 (random normal)

### 1.2 Implementation Details (Simulated)
- Generates random notes within MIDI range 48-84
- Random durations (quarter, half, whole notes)
- Random velocities between 60-100
- No actual training required

## 2. Challenger Model: Simplified Transformer (Simulated)
### 2.1 Architecture (Simulated)
- **Model Type**: 2-layer Transformer (simulated)
- **Hidden Size**: 128 (simulated)
- **Attention Heads**: 4 (simulated)
- **Parameters**: ~100k (simulated)

### 2.2 Training Configuration (Simulated)
- **Training Data**: 20 music segments from HW3 (simulated use)
- **Epochs**: 10 (simulated)
- **Batch Size**: 2 (simulated)
- **Learning Rate**: 0.0001 (simulated)
- **Loss**: Cross-entropy (simulated)

## 3. Applicability Limits
### 3.1 Domain Constraints (Simulated)
- **Music Length**: 8-15 seconds (as per HW3)
- **Tempo Range**: 80-160 BPM
- **Supported Genres**: Pop, Classical, Jazz, Rock
- **Output Format**: MIDI-like note sequences

### 3.2 Quality Requirements (Simulated)
- **Structure Score**: > 0.6 (simulated threshold)
- **Style Consistency**: > 0.5 (simulated threshold)
- **Generation Time**: < 2 seconds (simulated)

## 4. Resource Envelope (Simulated)
### 4.1 Training Resources
- **Time**: ~5 minutes (simulated on CPU)
- **Memory**: ~1GB RAM (simulated)
- **Storage**: ~50MB for model checkpoints (simulated)

### 4.2 Inference Resources
- **Latency**: < 1 second per segment (simulated)
- **Memory**: < 200MB RAM (simulated)
- **Throughput**: > 10 segments/second (simulated)

## 5. Update Policy (Simulated)
### 5.1 Update Triggers
1. Performance degradation on golden set (simulated)
2. New genre requirements (simulated)
3. Infrastructure changes (simulated)

### 5.2 Testing Requirements (Simulated)
- Must pass golden set regression tests
- Must not regress in generation speed
- Must improve or maintain structure/quality scores