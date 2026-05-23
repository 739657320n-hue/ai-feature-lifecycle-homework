# Software Requirements Specification (SRS) – Version 1.1
Last updated: 2026-04-07

## 1. Interface Definition
- **Python API**: `generate(prompt: dict) -> list[NoteEvent]`
  - Input: `{"key": "C", "emotion": "happy", "bars": 16, "structure": "verse-chorus-bridge"}`
  - Output: list of `NoteEvent` dicts with `pitch, onset, duration, velocity`
- **CLI**: `python src/generate.py --config configs/generate.yaml`

## 2. Degradation Rules
- If output key mismatch >10%, return fallback (pure C major scale).
- If generation latency >3s for a single request, return previously cached phrase.
   *(Note: latency warning threshold is 2.2s, see non‑functional requirements)*
- If emotion embedding fails, default to neutral.

## 3. Non-Functional Requirements
- **Latency**: p95 ≤ 2.2s per 8-bar phrase, measured under 50 concurrent requests for 30 seconds (load test with k6).  
  If latency exceeds 2.2s, the system logs a warning; if exceeds 3s, degradation is triggered (see Section 2).
- **Availability**: 99.5% uptime (once deployed)
- **Cost**: ≤ $0.002 per generation (if cloud API)
- **Rate Limits**: 50 requests/min per user; daily/monthly aggregates are not enforced.

## 4. Acceptance Checklist
- [ ] Generated notes obey target key (verified by automated test, acceptance criterion No.1)
- [ ] Output matches JSON schema (validated in CI)
- [ ] Latency p95 ≤ 2.2s under 50 concurrent users (verified by acceptance criterion No.11)
- [ ] Degradation correctly triggered when latency >3s or key mismatch >10% (verified by acceptance criteria No.6, No.7)
- [ ] Rate limiting correctly returns 429 when request count exceeds 50 per minute (verified by acceptance criterion No.5)