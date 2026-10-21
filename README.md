# PsycoSupport Cryptanalysis

InfoSec assignment (FAST-NUCES, Fall 2026). We run the
[PsycoSupport](https://github.com/maadilrehman/PsycoSupport) chat app fully
offline on Kali Linux, capture its loopback traffic, break its Affine cipher
with Al-Kindi frequency analysis, and write up the results.

Working rules for agents: see [AGENTS.md](AGENTS.md) and [docs/docs/index.md](docs/docs/index.md).
[INSTRUCTIONS.md](INSTRUCTIONS.md) is the older rules file, kept as history only.

Repository: <https://github.com/Rafique610/psycosupport-cryptanalysis>

## Setup

Requirements: Kali Linux, git, [uv](https://docs.astral.sh/uv/), [Ollama](https://ollama.com), Wireshark/tshark.

```bash
cd ~/Desktop/"Info A1"
```

Tools (no sudo needed; both install to `~/.local/bin`):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
sh -c "$(curl -fsSL https://taskfile.dev/install.sh)" -- -b ~/.local/bin
```

Python environment and app:

```bash
uv sync                 # installs ollama + requests from pyproject.toml / uv.lock
task check-env          # prints: ok
echo "127.0.0.1 muhammadrafique" | sudo tee -a /etc/hosts   # "host file" name from the brief
```

Ollama (needs sudo once) and the model:

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.2
```

## Run

```bash
task server             # terminal 1: http://127.0.0.1:5000, POST /submit
task client             # terminal 2: asks for username, mood, concern
task ollama-check       # installed models + Ollama API on localhost:11434
task offline-proof      # network off, model still answers, network back on
task capture            # record loopback port 5000 to evidence/task2/session_all.pcap (Ctrl+C to stop)
task run-cases          # send the 5 synthetic test cases through the real client
task extract            # pcap -> ciphertexts.csv (20 ciphertexts, standard library only)
task freq               # letter frequencies, patterns, candidate mapping, charts -> report/figures/
task recover            # solve for the affine key (a, b) with full working + chi-squared check
task decrypt            # decrypt all 20 ciphertexts and verify them (5/5 PASS both directions)
task report             # assemble report.pdf from report/sections/*.md (WeasyPrint)
```

## Layout

- `psycare_lab/`: the app. `server.py` (HTTP + Ollama), `client.py` (terminal client), `affine.py` (shared cipher), `requirements.txt`.
- `ciphertexts.csv`: the 20 intercepted ciphertexts (deliverable).
- `report.pdf`: the final report (built from `report/sections/*.md`).
- `scripts/`: analysis. `capture/` has the test cases, the case runner and the pcap extractor; `frequency/` counts letters, finds patterns and draws the charts (matplotlib); `cipher/` holds the attacker's affine toolkit (EEA, modular inverse) and the key recovery. `evidence/`: captures and screenshots. `report/`: the write-up.
- `docs/`: rules and project facts. Assignment brief: `docs/domain/psycosupport/assignment-brief.md`.

## Reproduce everything

With the setup above done (uv, task, Ollama + llama3.2, the /etc/hosts entry):

```bash
task server      # terminal 1
task capture     # terminal 2: start capture, then in terminal 3:
task run-cases   # terminal 3: send the 5 sessions, then Ctrl+C the capture
task extract     # pcap -> ciphertexts.csv
task freq        # frequency tables + charts
task recover     # recover the affine key (a, b) = (17, 8)
task decrypt     # decrypt all 20 ciphertexts, 5/5 PASS
task report      # build report.pdf
task package     # build dist/23i-0747_InfoSec_A1.zip for submission
```

## Submission

`task package` builds `dist/23i-0747_InfoSec_A1.zip` containing `report.pdf`, `ciphertexts.csv`, `scripts/`
and `evidence/`. Upload that ZIP to Google Classroom.
