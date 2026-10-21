# Security

> Draft from AGENTS.md (PC-1). Fill in from INSTRUCTIONS.md after PC-3.

- Never commit API keys, credentials, or `.env` files (`*.env`, `.env*` are git-ignored).
  The upstream Groq API key is ignored entirely: everything runs on local Ollama.
- Synthetic data only. No real personal or mental-health information in any test message.
- Capture tools (Wireshark, tcpdump, tshark) run only on the lab loopback interface (`lo`).
- Only analyse ciphertexts from our own PsycoSupport instance.
- Cite sources; no plagiarism.
