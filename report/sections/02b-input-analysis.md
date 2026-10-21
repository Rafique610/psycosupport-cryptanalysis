# Input Analysis

**What the client sends.** Every session is one HTTP `POST /submit` with three JSON fields, and one response
with a single `reply` field. Only the letters inside the JSON *values* are encrypted; the request line, headers,
JSON keys, digits, punctuation, spaces and letter case all travel in the clear (Section 2.5).

| Field | Direction | Length in this lab | Encrypted letters | Role in the attack |
| --- | --- | --- | --- | --- |
| `username` | client→server | 8 chars | 6 per session | Digits `01`–`05` stay plain, which maps streams to cases |
| `mood` | client→server | 6–11 chars | one English adjective | Short; readable once a few letters are known |
| `concern` | client→server | 155–208 chars | ~120–160 | Patient's private text, the main secret |
| `reply` | server→client | 645–800 chars | 509–636 | Long, fluent English: the richest statistical signal |

**How input length and variety fed the attack.** Frequency analysis needs enough letters for the English
profile to show through. The five sessions gave 3,663 encrypted letters in total, and the volume was the
difference between a clean break and a guess. Re-running the χ² key search on different slices of the capture
shows this directly (lower χ² = more clearly English; all slices recover the correct key (17, 8)):

| Slice | Encrypted letters | Winning key | Winner χ² | Runner-up χ² | Margin |
| --- | --- | --- | --- | --- | --- |
| All ciphertext | 3,663 | (17, 8) | 163.4 | 5,296.7 | 32× |
| Client→Server only | 775 | (17, 8) | 72.4 | 1,252.3 | 17× |
| Server→Client only | 2,888 | (17, 8) | 173.8 | 4,019.2 | 23× |
| A single reply (session 1) | 593 | (17, 8) | — | — | — |

Every slice breaks, including **one reply on its own** (≈500–640 letters). That is the key finding of the
input analysis: the long LLM responses carry most of the signal. Each reply is several hundred letters of
grammatical English with the same vocabulary patterns as the training corpus behind the standard frequency
table, so even a single intercepted answer is enough. The short request fields alone would also have worked
(775 letters, 17× margin), but they are the patient's private words, which is exactly what should have been
hardest to read.

**Why variety still mattered.** Five different concerns kept the attack honest: the letter counts come from
distinct messages, not one sentence repeated, so the recovered key is not an artefact of a single input.
Variety also exposed the determinism of the cipher: because several replies open with the same words, those
openings produced identical ciphertext across sessions (Section 3.3.3), a pattern that only becomes visible
when the inputs differ but some output does not.

**The attacker's shortcut.** None of this statistical work was strictly necessary. Because the request fields
keep their structure, an attacker reads word lengths and common words straight from the wire, and because
every reply ends in the same fixed disclaimer, two guessed letter pairs from that known sentence pin the key
outright (Section 3.2). Long, predictable input is what makes an affine cipher indefensible here.
