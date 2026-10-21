# Core rules (always loaded)

> Draft from AGENTS.md (PC-1). Fill in from INSTRUCTIONS.md after PC-3.

## Folder structure

- Feature-based: code lives with the feature it serves (`scripts/capture/`, `scripts/frequency/`, `scripts/cipher/`), not split by file type.
- Project-specific layout is recorded in `docs/domain/<project>/index.md`, not here.

## File size

- Keep files small and single-purpose. Split a file when it starts to do two jobs.
  (Exact limits: TODO from INSTRUCTIONS.md.)

## Real data only

- Never fake results, outputs, or evidence. Every table, chart, and decryption
  must come from a real run over real captured data.
- No placeholder numbers in deliverables.

## Ponytail ladder

- Simplest solution, shortest working diff. Active by default for all code.
  (Full ladder: TODO from INSTRUCTIONS.md.)

## Docs first

- Check docs before reading source. Go into source only when docs don't answer,
  the user asks, or to verify something the docs say before implementing it.
