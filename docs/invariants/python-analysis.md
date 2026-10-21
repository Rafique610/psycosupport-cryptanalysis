# Python analysis scripts

Stack-specific rules for everything under `scripts/`. Sources: INSTRUCTIONS.md §2, §4, §6, §9;
the PC-1 card (matplotlib for charts, pandas optional).

- Run through uv: `uv run scripts/<feature>/<script>.py`, wrapped in a `Taskfile.yml` task.
- One script per job, grouped by feature folder (§2):
  - `scripts/capture/`: pcap to ciphertext extraction (writes `ciphertexts.csv`).
  - `scripts/frequency/`: letter-frequency counts, tables, and charts compared with English.
  - `scripts/cipher/`: affine key recovery (modular inverse) and decryption.
- Standard library first (§9): `csv`, `collections.Counter`, `string`, `math.gcd`, `pow(a, -1, 26)`.
  matplotlib for charts (saved as PNG to `report/figures/`). pandas only if it clearly simplifies a script.
- Scripts read real inputs (pcap, `ciphertexts.csv`); never hard-code results.
- Each script runs on its own, prints what it wrote, and stays under ~300 lines (§4).
