# Tooling

Sources: AGENTS.md ("Tooling is uv"); INSTRUCTIONS.md §6. Docker (§7) is not used in this project.

## Python: uv (§6)

- `uv` only: `pyproject.toml` + `uv.lock` track every dependency. No Pixi, no conda,
  no pip into system Python.
- Never call `python` directly for project commands: `uv run python ...` / `uv run <script>`.
- Add deps with `uv add <pkg>`. `.venv/` is git-ignored.

## Task runner: Taskfile (§6)

- Every repeatable command gets a `Taskfile.yml` entry (go-task) so the user runs
  `task <name>` instead of memorising raw commands.
- On this Kali box `uv` and `task` live in `~/.local/bin` (installed without sudo).

## Kali paths

- Repo root: `~/Desktop/Info A1` (user-confirmed in PC-1; the card's default was
  `~/psycosupport-cryptanalysis`). The path contains a space: always quote it.
- Platform: Kali Linux. Client/server executables are Linux-only.
- Everything runs offline over loopback `127.0.0.1`.
