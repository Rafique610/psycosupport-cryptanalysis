# PsycoSupport Cryptanalysis

InfoSec assignment (FAST-NUCES, Fall 2026). Target app:
<https://github.com/maadilrehman/PsycoSupport>. Everything runs offline on Kali
over loopback `127.0.0.1`.

Repo root: `~/Desktop/Info A1`.

Full assignment text: [assignment-brief.md](assignment-brief.md) (converted from the revised .docx; verbatim).

## Upstream (checked 21 October 2026, PC-5)

- Repo `maadilrehman/PsycoSupport` at commit `0b1cdbf83f4274a7073d6c83897826608e1741bd` (4 October 2025). No GitHub releases.
- Contents: `README.md`, `server` (14.6 MB), `client` (12.3 MB). Both are stripped x86-64 Linux ELF files,
  bundled Python 3.12 apps. No `server.py`, `client.py` or `requirements.txt`.
- The bundled `server` contains the `groq` client library (cloud API), i.e. the pre-revision version.
  The revised brief expects `psycare_lab/{server.py, client.py, requirements.txt}` with Groq swapped for local Ollama.
- The upstream README mentions no "host file".

## Our psycare_lab (decided 21 October 2026, PC-5)

The revised `server.py` / `client.py` aren't published anywhere, so the user chose to **write them ourselves to the brief**.
This differs from the PC-5 card, which assumed upstream files: the card's "diff server.py against upstream" check
becomes "server.py stays unchanged after PC-5".

- Files: `psycare_lab/server.py`, `client.py`, `affine.py` (shared cipher), `requirements.txt` (`ollama`, `requests`).
  `affine.py` is an addition to the brief's three-file tree so client and server share one cipher.
- Server: stdlib `http.server`, bound to `127.0.0.1:5000`. One endpoint: `POST /submit`.
- Request JSON: `{"username", "mood", "concern"}`, each value affine-encrypted. Response JSON: `{"reply"}`, affine-encrypted.
  Both directions travel as plain HTTP over loopback, so Follow TCP Stream shows the JSON with ciphertext values.
- LLM: `ollama.chat` with model `llama3.2` (constant `MODEL` in `server.py`). The system prompt limits replies to
  under 120 words of supportive advice, no diagnosis or medication, and a fixed closing disclaimer sentence
  (the "mandatory boilerplate" Task 3 exploits).
- Encryption: `psycare_lab/affine.py`, `E(x) = (a·x + b) mod 26`. Applied to ASCII letters only; case is kept;
  digits, spaces and punctuation pass through unchanged. Client encrypts the request and decrypts the reply; server the reverse.
  Key values are deliberately not recorded in docs: Task 3 must recover them from ciphertext alone.
- Host file: the client connects to `http://muhammadrafique:5000`, which needs the line `127.0.0.1 muhammadrafique`
  in `/etc/hosts` (user's name: Muhammad Rafique). It still resolves to loopback, so capture stays on `lo`.

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

- Setup: PC-1 to PC-4 approved and pushed.
- Task 1: PC-5 in review.
