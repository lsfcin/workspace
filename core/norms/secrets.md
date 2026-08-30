---
name: secrets
description: A credential or someone else's personal data never enters a versioned file; it lives in a gitignored segredos.env and the text carries the label.
---

**SECRETS STAY OUT OF GIT**: a password, token, CPF/CNPJ or account number goes in a gitignored `<subtree>/segredos.env` and the versioned text names only the label — redact when transcribing, never drop the fact.
