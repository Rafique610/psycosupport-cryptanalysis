"""Recover the affine key (a, b) from the frequency analysis, printing every step of the working.

1. Take the two most frequent cipher letters from report/figures/candidate_mapping.csv and assume
   they are English e and t.
2. Solve a*p1 + b = c1, a*p2 + b = c2 (mod 26) with the Extended Euclidean Algorithm.
3. Verify gcd(a, 26) = 1 and a*a^-1 = 1 (mod 26), decrypt samples, and cross-check every one of the
   312 valid keys with a chi-squared score against English.
The working is also written to report/figures/key_recovery.txt.
"""

import csv
import sys
from math import gcd
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "frequency"))

from affine import M, decrypt, egcd, encrypt, modinv
from count import FIGURES, ciphertexts, letter_counts
from english import ENGLISH

ROOT = Path(__file__).resolve().parents[2]
num = lambda ch: ord(ch) - ord("a")
out = []


def say(line=""):
    out.append(line)
    print(line)


def eea_working(x, m=M):
    g, s, t, rows = egcd(m, x)
    say(f"  Extended Euclidean Algorithm on ({m}, {x}):")
    say(f"  {'step':>4} | {'dividend':>8} = {'q':>2} x {'divisor':>7} + {'rem':>3}")
    for i, (r0, r1, q, rem, _, _) in enumerate(rows, 1):
        say(f"  {i:>4} | {r0:>8} = {q:>2} x {r1:>7} + {rem:>3}")
    say(f"  gcd({m}, {x}) = {g};  {g} = ({s})*{m} + ({t})*{x}")
    if g != 1:
        say(f"  -> {x} has no inverse mod {m}")
        return None
    inv = t % m
    say(f"  -> {x}^-1 = {t} = {inv} (mod {m});  check {x} x {inv} = {x * inv} = {x * inv // m}*{m} + {x * inv % m}")
    return inv


def chi_squared(text):
    counts = letter_counts([text])
    n = sum(counts.values())
    return sum((counts[l] - n * ENGLISH[l] / 100) ** 2 / (n * ENGLISH[l] / 100) for l in counts)


def solve(c1, p1, c2, p2):
    say(f"Assume cipher '{c1}' = plain '{p1}' and cipher '{c2}' = plain '{p2}'  (a=0 ... z=25)")
    C1, P1, C2, P2 = map(num, (c1, p1, c2, p2))
    say(f"  (1) a*{P1} + b = {C1} (mod {M})")
    say(f"  (2) a*{P2} + b = {C2} (mod {M})")
    dp, dc = (P1 - P2) % M, (C1 - C2) % M
    say(f"  (1)-(2): a*({P1}-{P2}) = {C1}-{C2}  ->  {dp}*a = {dc} (mod {M})")
    inv = eea_working(dp)
    if inv is None:
        return None
    a = dc * inv % M
    b = (C1 - a * P1) % M
    say(f"  a = {dc} x {inv} = {dc * inv} = {a} (mod {M})")
    say(f"  b = {C1} - {a}*{P1} = {C1 - a * P1} = {b} (mod {M})")
    return a, b


if __name__ == "__main__":
    with (FIGURES / "candidate_mapping.csv").open() as f:
        ranked = list(csv.DictReader(f))
    (r1, r2) = ranked[0], ranked[1]
    say("== Step 1: equations from the two most frequent letters ==")
    key = solve(r1["cipher"], "e", r2["cipher"], "t")
    a, b = key

    say("\n== Step 2: validity of a and the decryption inverse ==")
    say(f"  gcd({a}, {M}) = {gcd(a, M)}  ->  {'valid' if gcd(a, M) == 1 else 'INVALID'} multiplier")
    a_inv = eea_working(a)
    say(f"  Decryption: D(y) = {a_inv}*(y - {b}) mod {M}")

    sample = "Round-trip check: This is a Test, 2026."
    assert decrypt(encrypt(sample, a, b), a, b) == sample
    say("  Round-trip assert decrypt(encrypt(s)) == s: passed")

    texts = ciphertexts()
    replies = ciphertexts("server_to_client")
    say("\n== Step 3: decrypted samples ==")
    say(f"  reply 1 (start): {decrypt(replies[0][:160], a, b)}")
    shared = replies[0][replies[0].rfind("\n\n") + 2:]
    say(f"  shared disclaimer: {decrypt(shared, a, b)}")

    say("\n== Step 4: chi-squared cross-check over all 312 keys (lower = more English-like) ==")
    corpus = "".join(texts)
    scores = sorted((chi_squared(decrypt(corpus, ka, kb)), ka, kb)
                    for ka in range(1, M) if gcd(ka, M) == 1 for kb in range(M))
    say(f"  {'rank':>4} | {'a':>2} {'b':>2} | chi-squared")
    for i, (chi, ka, kb) in enumerate(scores[:6], 1):
        say(f"  {i:>4} | {ka:>2} {kb:>2} | {chi:10.1f}{'   <- recovered key' if (ka, kb) == key else ''}")
    say(f"  keys tested: {len(scores)};  best key = ({scores[0][1]}, {scores[0][2]})")
    assert (scores[0][1], scores[0][2]) == key, "frequency key and chi-squared winner disagree"

    say(f"\nRECOVERED KEY: a = {a}, b = {b}, a^-1 = {a_inv}")
    (FIGURES / "key_recovery.txt").write_text("\n".join(out) + "\n")
