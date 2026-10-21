"""Affine cipher shared by client and server: E(x) = (a*x + b) mod 26 on A-Z/a-z, other characters unchanged."""

A, B = 17, 8  # gcd(A, 26) must be 1 so the key is invertible
A_INV = pow(A, -1, 26)


def _shift(text, f):
    out = []
    for ch in text:
        if ch.isascii() and ch.isalpha():
            base = ord("A") if ch.isupper() else ord("a")
            out.append(chr(base + f(ord(ch) - base) % 26))
        else:
            out.append(ch)
    return "".join(out)


def encrypt(text):
    return _shift(text, lambda x: A * x + B)


def decrypt(text):
    return _shift(text, lambda y: A_INV * (y - B))
