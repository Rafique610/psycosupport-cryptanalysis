"""Affine cipher toolkit for the attack: E(x) = (a*x + b) mod 26 on letters, case kept, other characters unchanged."""

M = 26


def egcd(a, b):
    """Extended Euclidean Algorithm. Returns (g, s, t, rows) with g = gcd(a, b) = s*a + t*b.

    rows holds one tuple (r_prev, r, q, remainder, s, t) per division, for printing the working.
    """
    r0, r1, s0, s1, t0, t1, rows = a, b, 1, 0, 0, 1, []
    while r1:
        q = r0 // r1
        rows.append((r0, r1, q, r0 - q * r1, s1, t1))
        r0, r1, s0, s1, t0, t1 = r1, r0 - q * r1, s1, s0 - q * s1, t1, t0 - q * t1
    return r0, s0, t0, rows


def modinv(a, m=M):
    g, s, _, _ = egcd(a % m, m)
    if g != 1:
        raise ValueError(f"{a} has no inverse mod {m} (gcd = {g})")
    return s % m


def _map(text, f):
    out = []
    for ch in text:
        if ch.isascii() and ch.isalpha():
            base = ord("A") if ch.isupper() else ord("a")
            out.append(chr(base + f(ord(ch) - base) % M))
        else:
            out.append(ch)
    return "".join(out)


def encrypt(text, a, b):
    return _map(text, lambda x: a * x + b)


def decrypt(text, a, b):
    a_inv = modinv(a)
    return _map(text, lambda y: a_inv * (y - b))
