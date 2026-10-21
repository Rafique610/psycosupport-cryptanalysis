"""Charts for the frequency analysis: ciphertext letter frequencies and a ranked comparison with English."""

import csv
import string

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from count import FIGURES
from english import ENGLISH, ENGLISH_RANKED

CIPHER, ENGLISH_COLOR = "#2a78d6", "#eb6834"  # categorical slots 1 and 2 (dataviz reference palette)
SURFACE, INK, MUTED = "#fcfcfb", "#0b0b0b", "#52514e"

plt.rcParams.update({
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
    "axes.edgecolor": MUTED, "axes.labelcolor": INK, "xtick.color": MUTED, "ytick.color": MUTED,
    "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "axes.grid.axis": "y",
    "grid.color": "#e4e3df", "grid.linewidth": 0.6, "axes.axisbelow": True, "font.size": 10,
})


def load(name):
    with (FIGURES / name).open() as f:
        return {r["symbol"]: r for r in csv.DictReader(f)}


def cipher_freq():
    rows = load("freq_table.csv")
    total = sum(int(r["count"]) for r in rows.values())
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.bar(list(string.ascii_lowercase), [float(rows[s]["percent"]) for s in string.ascii_lowercase],
           color=CIPHER, width=0.72, edgecolor=SURFACE, linewidth=1)
    ax.set_title(f"Ciphertext letter frequency, all 20 ciphertexts ({total:,} letters)", loc="left", color=INK)
    ax.set_xlabel("Ciphertext letter (case-folded)")
    ax.set_ylabel("Share of letters (%)")
    fig.tight_layout()
    fig.savefig(FIGURES / "cipher_freq.png", dpi=200)


def compare_ranked():
    ranked = sorted(load("freq_table.csv").values(), key=lambda r: int(r["rank"]))
    x = range(1, 27)
    fig, ax = plt.subplots(figsize=(11, 4.6))
    w = 0.4
    cb = ax.bar([i - w / 2 for i in x], [float(r["percent"]) for r in ranked], w,
                color=CIPHER, edgecolor=SURFACE, linewidth=1, label="Ciphertext")
    eb = ax.bar([i + w / 2 for i in x], [ENGLISH[e] for e in ENGLISH_RANKED], w,
                color=ENGLISH_COLOR, edgecolor=SURFACE, linewidth=1, hatch="///", label="English (Lewand 2000)")
    for bar, r in zip(cb, ranked):
        ax.annotate(r["symbol"].upper(), (bar.get_x() + bar.get_width() / 2, bar.get_height()),
                    xytext=(0, 2), textcoords="offset points", ha="center", fontsize=8, color=INK, weight="bold")
    for bar, e in zip(eb, ENGLISH_RANKED):
        ax.annotate(e.upper(), (bar.get_x() + bar.get_width() / 2, bar.get_height()),
                    xytext=(0, 2), textcoords="offset points", ha="center", fontsize=8, color=MUTED)
    ax.set_xticks(list(x))
    ax.set_xlabel("Frequency rank (1 = most common)")
    ax.set_ylabel("Share of letters (%)")
    ax.set_title("Ciphertext letters vs English letters, matched by rank", loc="left", color=INK)
    ax.legend(frameon=False, loc="upper right")
    fig.tight_layout()
    fig.savefig(FIGURES / "compare_ranked.png", dpi=200)


if __name__ == "__main__":
    cipher_freq()
    compare_ranked()
    print("wrote report/figures/cipher_freq.png and compare_ranked.png")
