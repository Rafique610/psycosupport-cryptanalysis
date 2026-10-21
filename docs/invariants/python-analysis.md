# Python analysis scripts

Stack-specific rules for everything under `scripts/`.

- Python run through `uv` (`uv run scripts/<feature>/<script>.py`). Deps declared in `pyproject.toml`.
- Charts: matplotlib. Save figures to `report/figures/` as PNG.
- Tables/CSV: standard library `csv` first; pandas only if it clearly simplifies the script.
- One script per job, grouped by feature folder:
  - `scripts/capture/`: pcap to ciphertext extraction (writes `ciphertexts.csv`).
  - `scripts/frequency/`: letter-frequency counts, tables, and charts compared with English.
  - `scripts/cipher/`: affine key recovery (modular inverse) and decryption.
- Scripts read real inputs (pcap, `ciphertexts.csv`); never hard-code results.
- Each script is runnable on its own and prints what it wrote.
