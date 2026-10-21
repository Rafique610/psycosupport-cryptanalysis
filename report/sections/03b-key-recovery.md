## 3.2 Recovering the affine key (a, b)

The key is derived from the ciphertext statistics of Section 3.1 alone. The complete working below is
printed by `task recover` (`scripts/cipher/recover_key.py`), which reads the two top-ranked letters from
`report/figures/candidate_mapping.csv` and stores its output in `report/figures/key_recovery.txt`.
Every run gives the same result.

### 3.2.1 Model

Letters are numbered a = 0, b = 1, …, z = 25 (Section 3.1.1 established m = 26). The affine cipher is

  E(x) = (a·x + b) mod 26,  D(y) = a⁻¹·(y − b) mod 26,

which is only decryptable when gcd(a, 26) = 1, so a ∈ {1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25}
(12 choices) and b ∈ {0, …, 25}: 12 × 26 = 312 possible keys.

### 3.2.2 Two equations from the frequency analysis

The two most frequent ciphertext letters (Table 3.1) are assumed to be the two most frequent English letters:

| Assumption | Cipher letter | c | Plain letter | p |
| --- | --- | --- | --- | --- |
| Rank 1 | y | 24 | e | 4 |
| Rank 2 | t | 19 | t | 19 |

Since E(p) = c:

  (1) 4a + b ≡ 24 (mod 26)
  (2) 19a + b ≡ 19 (mod 26)

Subtracting (2) from (1) removes b:

  (4 − 19)·a ≡ 24 − 19  ⇒  −15a ≡ 5  ⇒  **11a ≡ 5 (mod 26)**  (since −15 ≡ 11)

### 3.2.3 Inverse of 11 modulo 26 (Extended Euclidean Algorithm)

| Step | Division |
| --- | --- |
| 1 | 26 = 2 × 11 + 4 |
| 2 | 11 = 2 × 4 + 3 |
| 3 | 4 = 1 × 3 + 1 |
| 4 | 3 = 3 × 1 + 0 |

The last non-zero remainder is 1, so gcd(26, 11) = 1 and 11 is invertible. Back-substitution:

  1 = 4 − 1·3
   = 4 − (11 − 2·4)    = 3·4 − 11
   = 3·(26 − 2·11) − 11 = 3·26 − 7·11

So −7·11 ≡ 1 (mod 26), giving **11⁻¹ ≡ −7 ≡ 19 (mod 26)**.
Check: 11 × 19 = 209 = 8 × 26 + 1 ≡ 1. ✓

### 3.2.4 Solving for a and b

  a ≡ 19 × 5 = 95 = 3 × 26 + 17  ⇒  **a = 17**

  b ≡ 24 − 17 × 4 = 24 − 68 = −44 ≡ −44 + 52  ⇒  **b = 8**

Check both equations: E(4) = 17·4 + 8 = 76 = 2·26 + 24 → `y` ✓; E(19) = 17·19 + 8 = 331 = 12·26 + 19 → `t` ✓.
(The letter *t* is a fixed point of this key, which is why `t` appears unchanged in the ciphertext.)

### 3.2.5 Validity of a and the decryption key a⁻¹

gcd(17, 26) = 1, so a = 17 is a valid multiplier. Its inverse:

| Step | Division |
| --- | --- |
| 1 | 26 = 1 × 17 + 9 |
| 2 | 17 = 1 × 9 + 8 |
| 3 | 9 = 1 × 8 + 1 |
| 4 | 8 = 8 × 1 + 0 |

Back-substitution:

  1 = 9 − 8
   = 9 − (17 − 9)    = 2·9 − 17
   = 2·(26 − 17) − 17 = 2·26 − 3·17

So **a⁻¹ ≡ −3 ≡ 23 (mod 26)**. Proof: 17 × 23 = 391 = 15 × 26 + 1 ≡ 1 (mod 26). ✓

The decryption function is therefore

  **D(y) = 23·(y − 8) mod 26.**

### 3.2.6 Validation

**Independent letter checks.** Section 3.1.5 proposed seven more pairs from word structure, none of them
used to build the equations. The recovered key confirms all seven:

| Cipher | y | D(y) = 23(y − 8) mod 26 | Plain | Structural guess |
| --- | --- | --- | --- | --- |
| x | 23 | 23·15 = 345 ≡ 7 | h | *h* in `txy` = the ✓ |
| i | 8 | 23·0 = 0 | a | *a* ✓ |
| v | 21 | 23·13 = 299 ≡ 13 | n | *n* in `ivh` = and ✓ |
| h | 7 | 23·(−1) = −23 ≡ 3 | d | *d* in `ivh` = and ✓ |
| o | 14 | 23·6 = 138 ≡ 8 | i | *I* / *ing* ✓ |
| g | 6 | 23·(−2) = −46 ≡ 6 | g | *g* in `ovg` = ing ✓ |
| m | 12 | 23·4 = 92 ≡ 14 | o | *o* in `tm` = to ✓ |

**Decrypted samples.**

- Reply 1, `Ot cmkvhc nowy amk'ly pyynovg i nmt mp dlycckly…` →
  *It sounds like you're feeling a lot of pressure and anxiety about your exams. It's normal to feel this way…*
- The block shared by all five replies (Section 3.1.4) →
  *This is not a substitute for professional help. If you are in crisis, please contact your local emergency services.*

**Chi-squared cross-check.** As an independent check only, all 312 valid keys were tried on the full
ciphertext, and each decryption was scored against English letter frequencies with
χ² = Σ (observedᵢ − expectedᵢ)² / expectedᵢ (lower means more English-like):

| Rank | a | b | χ² |
| --- | --- | --- | --- |
| **1** | **17** | **8** | **163.4** (recovered key) |
| 2 | 15 | 24 | 5,296.7 |
| 3 | 7 | 24 | 5,777.4 |
| 4 | 1 | 6 | 6,364.8 |
| 5 | 23 | 0 | 6,920.0 |
| 6 | 15 | 11 | 7,228.1 |

The recovered key is the clear winner, about 32 times better than the runner-up. The script asserts that
the frequency-derived key and the χ² winner agree.

**Confirmation against the source.** Only after the derivation above was the key in
`psycare_lab/affine.py` inspected: `A = 17`, `B = 8`, `A_INV = 23`, identical to the recovered values.

**Recovered key: (a, b) = (17, 8), with decryption multiplier a⁻¹ = 23.**

### 3.2.7 Why this was easy

- **Two letters were enough.** The affine cipher has only 312 keys and is fully determined by two
  plaintext–ciphertext letter pairs. Frequency analysis supplied them from the first two ranks.
- **The LLM's output is predictable English.** Long, grammatical replies push the letter distribution
  towards textbook English (IC 0.0647 vs 0.0655), so the top-ranked letters land exactly where expected
  (`t` matches English *t* to two decimal places).
- **Boilerplate is free known plaintext.** The fixed 118-character disclaimer at the end of every reply
  turns a ciphertext-only attack into a known-plaintext one: an attacker who guesses the standard
  *This is not a substitute for professional help* can read off a dozen letter pairs and confirm the key
  without any statistics.
- **Structure leaks through.** Spaces, punctuation, case and JSON keys survive encryption, exposing word
  lengths and common words (*and*, *the*, *-ing*).

These failures are analysed further in Task 4.
