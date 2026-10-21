"""Count ciphertext letters (A-Z, case-folded) from ciphertexts.csv and write frequency tables.

Writes report/figures/freq_table.csv (all ciphertexts) plus freq_table_client_to_server.csv and
freq_table_server_to_client.csv, each with columns symbol, count, percent, rank.
"""

import csv
import json
import string
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIGURES = ROOT / "report/figures"


def ciphertexts(direction=None):
    """Ciphertext strings from ciphertexts.csv with JSON escapes undone (so the n of \\n isn't counted)."""
    with (ROOT / "ciphertexts.csv").open() as f:
        return [json.loads(f'"{r["ciphertext"]}"') for r in csv.DictReader(f)
                if direction in (None, r["direction"])]


def letter_counts(texts):
    counts = Counter(ch for text in texts for ch in text.lower() if ch in string.ascii_lowercase)
    return {letter: counts[letter] for letter in string.ascii_lowercase}


def table(counts):
    total = sum(counts.values())
    ranked = sorted(counts, key=lambda s: (-counts[s], s))
    rows = [{"symbol": s, "count": counts[s], "percent": round(100 * counts[s] / total, 3),
             "rank": ranked.index(s) + 1} for s in string.ascii_lowercase]
    assert abs(sum(r["percent"] for r in rows) - 100) <= 0.1, "percentages must add up to 100"
    return rows


def write(rows, path):
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["symbol", "count", "percent", "rank"])
        writer.writeheader()
        writer.writerows(sorted(rows, key=lambda r: r["rank"]))


if __name__ == "__main__":
    FIGURES.mkdir(parents=True, exist_ok=True)
    for direction, name in [(None, "freq_table.csv"),
                            ("client_to_server", "freq_table_client_to_server.csv"),
                            ("server_to_client", "freq_table_server_to_client.csv")]:
        counts = letter_counts(ciphertexts(direction))
        write(table(counts), FIGURES / name)
        print(f"{name}: {sum(counts.values())} letters")
