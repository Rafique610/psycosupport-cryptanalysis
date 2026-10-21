"""Structural patterns in the ciphertext: n-grams, common words, and text repeated across sessions.

Writes report/figures/patterns.md (tables for the report) and report/figures/candidate_mapping.csv
(cipher letter of rank i paired with the English letter of rank i).
"""

import csv
import re
from collections import Counter
from pathlib import Path

from count import FIGURES, ciphertexts, letter_counts, table
from english import ENGLISH, ENGLISH_RANKED

WORD = re.compile(r"[a-z]+(?:'[a-z]+)?")


def ngrams(texts, n):
    return Counter(w[i:i + n] for t in texts for w in WORD.findall(t.lower()) for i in range(len(w) - n + 1))


def longest_shared(texts):
    """Longest substring present in every text (the replies' shared boilerplate)."""
    first, best = texts[0], ""
    for i in range(len(first)):
        for j in range(len(first), i + len(best), -1):
            if all(first[i:j] in t for t in texts[1:]):
                best = first[i:j]
                break
    return best


def index_of_coincidence(counts):
    n = sum(counts.values())
    return sum(c * (c - 1) for c in counts.values()) / (n * (n - 1))


def md_table(header, rows):
    lines = ["| " + " | ".join(header) + " |", "| " + " | ".join("---" for _ in header) + " |"]
    return "\n".join(lines + ["| " + " | ".join(str(c) for c in row) + " |" for row in rows])


if __name__ == "__main__":
    texts, replies = ciphertexts(), ciphertexts("server_to_client")
    words = Counter(w for t in texts for w in WORD.findall(t.lower()))
    one_letter = Counter(w for t in texts for w in re.findall(r"\b[a-z]\b", t.lower()))
    shared = longest_shared(replies)
    ranked = sorted(table(letter_counts(texts)), key=lambda r: r["rank"])

    with (FIGURES / "candidate_mapping.csv").open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["rank", "cipher", "cipher_percent", "english", "english_percent"])
        for r, eng in zip(ranked, ENGLISH_RANKED):
            writer.writerow([r["rank"], r["symbol"], r["percent"], eng, ENGLISH[eng]])

    ioc = {name: index_of_coincidence(letter_counts(ciphertexts(d)))
           for name, d in [("all", None), ("client_to_server", "client_to_server"), ("server_to_client", "server_to_client")]}
    english_ioc = sum((p / 100) ** 2 for p in ENGLISH.values())
    sections = [
        "## Index of coincidence\n\n" + md_table(["text", "IC"], [(k, f"{v:.4f}") for k, v in ioc.items()]
            + [("English (from Lewand table)", f"{english_ioc:.4f}"), ("uniform random letters", f"{1 / 26:.4f}")]),
        "## Most frequent cipher words\n\n" + md_table(["word", "count"], words.most_common(12)),
        "## One-letter cipher words\n\n" + md_table(["word", "count"], one_letter.most_common()),
        "## Top bigrams (within words)\n\n" + md_table(["bigram", "count"], ngrams(texts, 2).most_common(10)),
        "## Top trigrams (within words)\n\n" + md_table(["trigram", "count"], ngrams(texts, 3).most_common(10)),
        f"## Longest text shared by all {len(replies)} replies\n\n{len(shared)} characters:\n\n```\n{shared.strip()}\n```",
    ]
    (FIGURES / "patterns.md").write_text("\n\n".join(sections) + "\n")
    print(f"wrote patterns.md and candidate_mapping.csv; shared reply text: {len(shared)} chars")
