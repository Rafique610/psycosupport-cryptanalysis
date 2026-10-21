# Security

Sources: INSTRUCTIONS.md §5; the assignment's ethics rules (PC-1 card). §5b (ORM) does not apply:
this project has no database.

## Credentials (§5)

- Never commit or print API keys, credentials, or `.env` files (`*.env`, `.env*` are git-ignored).
  The upstream Groq API key is ignored entirely: everything runs on local Ollama.
- Never hardcode credentials in code, config, or scripts. If a script ever needs a setting from the
  environment, read it in one place, not scattered through the code.

## Data and capture (assignment ethics)

- Synthetic data only. No real personal or mental-health information in any test message.
- Capture tools (Wireshark, tcpdump, tshark) run only on the lab loopback interface (`lo`).
- Only analyse ciphertexts from our own PsycoSupport instance.
- Cite sources; no plagiarism.
