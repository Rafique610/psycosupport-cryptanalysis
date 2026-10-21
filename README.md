# PsycoSupport Cryptanalysis

InfoSec assignment (FAST-NUCES, Fall 2026). We run the
[PsycoSupport](https://github.com/maadilrehman/PsycoSupport) chat app fully
offline on Kali Linux, capture its loopback traffic, break its Affine cipher
with Al-Kindi frequency analysis, and write up the results.

Working rules for agents: see [AGENTS.md](AGENTS.md) and [docs/docs/index.md](docs/docs/index.md).
[INSTRUCTIONS.md](INSTRUCTIONS.md) is the older rules file, kept as history only.

## Setup

Requirements: Kali Linux, git, [uv](https://docs.astral.sh/uv/), [Ollama](https://ollama.com), Wireshark/tshark.

```bash
cd ~/Desktop/"Info A1"
```

Further steps (uv environment, Ollama models, running the server) are added as
cards PC-5 and PC-6 land.
