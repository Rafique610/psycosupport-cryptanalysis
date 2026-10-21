# Docs index

Knowledge map for this repo. Start at `AGENTS.md`, then come here.

## Domain (what's true about this project)

- [PsycoSupport Cryptanalysis](../domain/psycosupport/index.md): assignment facts, deliverables, rubric, layout, card order.

## Invariants (rules; load only the one your task needs)

| Doc | Load when |
| --- | --- |
| [core.md](../invariants/core.md) | Always |
| [processes.md](../invariants/processes.md) | Plans, ADRs, cadence, README, `.memory/` log |
| [tooling.md](../invariants/tooling.md) | uv, Taskfile, Kali paths |
| [security.md](../invariants/security.md) | Credentials, keys, captured data, ethics |
| [python-analysis.md](../invariants/python-analysis.md) | Writing anything under `scripts/` |

`backend.md` and `frontend.md` are intentionally absent: this project builds no
FastAPI or Next.js app, and `psycare_lab/server.py` must not be changed.

## Plans

- `docs/plans/`: background and method. The Synverk board (project key PC) is the current plan.

## History

- `INSTRUCTIONS.md` (root, written in PC-2 + PC-3): history only. Where it disagrees with `AGENTS.md` or `docs/invariants/`, those win.
