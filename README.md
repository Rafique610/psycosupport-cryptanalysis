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
```

## Layout

- `psycare_lab/`: the app. `server.py` (HTTP + Ollama), `client.py` (terminal client), `affine.py` (shared cipher), `requirements.txt`.
- `scripts/`: analysis (capture, frequency, cipher). `evidence/`: captures and screenshots. `report/`: the write-up.
- `docs/`: rules and project facts. Assignment brief: `docs/domain/psycosupport/assignment-brief.md`.
