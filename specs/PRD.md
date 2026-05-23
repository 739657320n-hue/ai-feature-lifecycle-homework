# Product Requirements Document (PRD)

## 1. Problem Statement
Symbolic music generation faces low pitch accuracy, poor controllability, and high creation threshold. Existing models lack hierarchical structure and explicit emotional control.

## 2. Target Users & Value
- **Primary persona**: Music composers / producers who need high-quality piano backing tracks with specified emotion.
- **Secondary persona**: Game/movie soundtrack developers who require consistent emotional themes.
- **Value**: Reduce composition time by 80% while ensuring harmonic correctness and structural coherence.

## 3. Scope & Non-Goals
- **In scope**: 4/4 time, pop/classical piano, 16-32 bars, emotion labels (happy/sad/tense), hierarchical verse-chorus-bridge structure.
- **Non-goals**: waveform audio, real-time interaction, lyrics-to-melody, non-Western scales.

## 4. Key Performance Indicators (KPIs)
- Pitch Accuracy ≥ 99%
- Out-of-key Note Ratio ≤ 0.5%
- Chord Similarity ≥ 0.90
- Generation latency per 8-bar phrase ≤ 2s (single RTX 3080)
- Training memory ≤ 8 GB GPU

## 5. Risk Framing & Mitigations
| Risk | Mitigation |
|------|------------|
| Data bias (Chinese pop vs classical) | Evaluate on both styles; report segment metrics |
| High out-of-key ratio | Embed chord constraints in diffusion & refinement module |
| Unstable emotional expression | Explicit emotional guidance module with validation |
| Long-generation structure collapse | Global structure encoder + phrase-level decoder |

## 6. Sign-off
- Owner: Wangjingyi
- Reviewer: Instructor / TA
- Approval: PR review + CODEOWNERS (enforced)