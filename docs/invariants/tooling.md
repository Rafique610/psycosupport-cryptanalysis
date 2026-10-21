# Tooling

> Draft from AGENTS.md (PC-1). Fill in from INSTRUCTIONS.md after PC-3.

## Python: uv

- `uv` only (`pyproject.toml` + `uv.lock`). No pip installs into system Python, no Pixi, no conda.
- Add deps with `uv add <pkg>`; run scripts with `uv run <script>`.
- `.venv/` is git-ignored.

## Task runner: Taskfile

- Common commands live in `Taskfile.yml` (go-task) so they're repeatable.

## Kali paths

- Repo root: `~/Desktop/Info A1` (user-confirmed in PC-1; the card's default was
  `~/psycosupport-cryptanalysis`). The path contains a space: always quote it.
- Platform: Kali Linux. Client/server executables are Linux-only.
- Everything runs offline over loopback `127.0.0.1`.
