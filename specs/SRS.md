# Software Requirements Specification (SRS)

## 1. Interface Definition
- **Python API**: `generate(prompt: dict) -> list[NoteEvent]`
  - Input: `{"key": "C", "emotion": "happy", "bars": 16, "structure": "verse-chorus-bridge"}`
  - Output: list of `NoteEvent` dicts with `pitch, onset, duration, velocity`
- **CLI**: `python src/generate.py --config configs/generate.yaml`

## 2. Degradation Rules
- If output key mismatch >10%, return fallback (pure C major scale).
- If latency >3s, return previously cached phrase.
- If emotion embedding fails, default to neutral.

## 3. Non-Functional Requirements
- Latency: p95 ≤ 2.2s per 8-bar phrase (load test with k6)
- Availability: 99.5% uptime (once deployed)
- Cost: ≤ $0.002 per generation (if cloud API)
- Rate limits: 50 requests/min per user

## 4. Acceptance Checklist
- [ ] Generated notes obey target key (test: `tests/test_pitch_accuracy.py`)
- [ ] Output matches JSON schema (validated in CI)
- [ ] Latency fails if above threshold (CI: `make eval-gate`)