# Core rules (always loaded)

Sources: AGENTS.md; INSTRUCTIONS.md §2, §4, §4c, §9.

## Folder structure (§2)

- Feature-based: each feature gets its own folder with everything it needs
  (`scripts/capture/`, `scripts/frequency/`, `scripts/cipher/`). Never mix
  responsibilities across features.
- This project's concrete layout lives in `docs/domain/psycosupport/index.md`, not here.

## File size and responsibility (§4)

- No "god files". A file past ~300 lines has too much responsibility: split it.
- Use a design pattern only when needed, never overengineer, and tell the user
  which pattern and why.

## Real data only (§4c)

- Never show fabricated, mock, or guessed numbers. Every table, chart, key, and
  decryption must come from a real run over real captured data.
- If something can't be measured honestly, compute it properly, show only the real
  part, or omit it.

## Ponytail ladder (§9)

Simplest working solution, shortest working diff. Before writing code, stop at the first rung that works:

1. Does this need to exist at all? (YAGNI)
2. Already in this codebase? Reuse it.
3. Standard library does it? (`csv`, `collections.Counter`, `pathlib`, `math`, `pow(a, -1, 26)`)
4. Native platform feature covers it? (tshark, Wireshark)
5. Already-installed dependency solves it? Use it. No new packages without need.
6. Can it be one line? Make it one line.
7. Only then: write the minimum code that works.

- No unrequested abstractions. Bug fixes address root causes.
- Every non-trivial piece of code gets ONE minimal runnable verification check.

## Docs first (AGENTS.md)

- Check docs before reading source. Go into source only when docs don't answer,
  the user asks, or to verify something the docs say before implementing it.
