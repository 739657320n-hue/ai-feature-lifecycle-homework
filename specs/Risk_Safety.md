# Risk, Safety & Privacy

## 1. Misuse Cases
- User requests explicit/offensive lyrics (model only outputs notes, but still reject with refusal)
- Attempt to generate music that mimics copyrighted works → risk flag

## 2. PII Handling
- Input prompts may contain text, but model processes only musical parameters, no personal data
- Output MIDI files contain no audio or identifiable information

## 3. High-Cost Errors
- **Must-not-happen**: generate music with extreme dissonance (e.g., all out-of-key notes)
- Mitigation: note-level refinement module + threshold gate

## 4. Human-in-the-Loop
- Generated pieces above rating threshold require manual review before public sharing
- Audit log: every generation is recorded with request ID, timestamp, metrics

## 5. Red-Team Tests (CI)
- Test prompts that try to bypass emotion contraints → must return refusal or safe fallback
- All red-team tests must pass in CI