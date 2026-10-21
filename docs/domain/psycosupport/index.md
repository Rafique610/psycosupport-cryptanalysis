# PsycoSupport Cryptanalysis

InfoSec assignment (FAST-NUCES, Fall 2026). Target app:
<https://github.com/maadilrehman/PsycoSupport>. Everything runs offline on Kali
over loopback `127.0.0.1`.

Repo root: `~/Desktop/Info A1`.

## Deliverables (ZIP)

- `report.pdf`
- `ciphertexts.csv`
- `scripts/`
- `evidence/` (optional screenshots/pcap)

## Notes from the brief

- Client/server executables are **Linux only**.
- **For the host file, use the user's own name** (ask the user for it).
- **Do not change `server.py` functionality** (the Groq call was swapped for local Ollama).
- **Ignore the API key**: everything runs locally.

## Tasks

| Task | Marks | What |
| --- | --- | --- |
| 1 | 20 | Ollama with `llama3.2` or `phi3`, run `server.py` |
| 2 | 20 | Capture loopback `tcp.port == 5000`, 5 test cases, Client→Server and Server→Client ciphertexts via Follow TCP Stream |
| 3 | 40 | Frequency analysis vs English, recover affine key (a, b) with the modular inverse, full proofs, decrypt all 5 sessions |
| 4 | 20 | Security analysis + ≥2 local IPC protections (UNIX domain sockets, self-signed TLS 1.3) |

## Rubric

- ≥5 ciphertexts with evidence (20)
- Accurate tables/charts + reasoning + key mapping (40)
- Correct decryption of 3–5 (20)
- Clarity + input analysis + ethical reflection (20)

## Ethics

- Only analyse ciphertexts from our own PsycoSupport instance.
- Synthetic messages only.
- Never commit keys.
- Capture tools only on lab loopback.
- Cite sources, no plagiarism.

## Folder layout (confirmed by the user, 21 October 2026)

```
psycare_lab/          # upstream app (server.py, client.py, requirements.txt). server.py functionality untouched
scripts/
  capture/            # pcap -> ciphertext extraction
  frequency/          # frequency counts, tables, charts
  cipher/             # affine key recovery + decryption
evidence/             # screenshots, pcap snippets
report/               # report.md source + sections/ + figures/ -> report.pdf
ciphertexts.csv
docs/  AGENTS.md  INSTRUCTIONS.md  README.md  Taskfile.yml  pyproject.toml  uv.lock
```

## Card order (Synverk, key PC)

PC-1…PC-4 setup → PC-5/6 Task 1 → PC-7/8 Task 2 → PC-9/10/11 Task 3 → PC-12 Task 4 → PC-13 report → PC-14 ZIP.

## Phase status

- Setup: PC-1 in progress.
