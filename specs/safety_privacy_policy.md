# Safety & Privacy Policy – MusicGen Service

## 1. Scope and Boundaries
This policy applies to all versions of the MusicGen model deployed in production. The service generates musical audio from text prompts. It does **not**:
- Generate speech, lyrics, or sound effects
- Respond to commands outside music generation
- Access the internet, read user files, or modify system state

## 2. Ownership
- **Product Risk Owner**: Alice (alice@example.com)
- **Security Owner**: Bob (bob@example.com)
- **Engineering Owner**: Carol (carol@example.com)

Policy changes require explicit approval from Security Owner via PR.

## 3. Permitted Use Cases
- Creating original music for personal or commercial projects
- Educational demonstrations
- Non‑malicious entertainment

## 4. Forbidden Use Cases (Must‑reject)
- Generating music that includes copyrighted melodies or samples
- Creating music with hate speech or discriminatory themes
- Generating music that mimics specific artists without permission
- Using the service for harassment, impersonation, or misinformation

## 5. Data Privacy
- **PII**: No personally identifiable information is collected. User prompts are logged with request IDs, but raw text is redacted using Presidio before storage.
- **Retention**: Logs are retained for 90 days, then automatically deleted.
- **Deletion**: Users may request deletion of their prompt logs via a support ticket.

## 6. Logging Policy
- Only anonymized metadata (request duration, model version, success/failure) is logged.
- Raw prompts are never written to persistent storage outside of isolated debug mode (access restricted, 24‑hour retention).

## 7. Incident Response
Refer to the Incident Playbook (`docs/incident_playbook.md`). All incidents must be documented and reviewed within 5 business days.