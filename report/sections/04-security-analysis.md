# 4. Security Engineering Analysis

PsycoSupport promises "end-to-end encryption" for patients' mental-health concerns. In this lab an
unprivileged observer on the same machine recovered the key in under a second and read every message.
This section explains why, and how local inter-process communication (IPC) should be protected instead.

## 4.1 Why LLM output breaks classical ciphers

The affine cipher is a **monoalphabetic substitution**: each plaintext letter always maps to the same
ciphertext letter, and nothing else changes. LLM-generated text is close to the worst possible input for
such a cipher, because it is long, fluent and formulaic.

**1. Text that looks like the textbook.** Five replies gave 2,888 cipher letters whose index of coincidence
(0.0646) matches English (0.0655) almost exactly (Section 3.1.3). The most frequent cipher letter `y` sat at
11.8 % against English *e* at 12.7 %, and cipher `t` at 9.06 % against English *t* at 9.06 %. The first two
ranks were enough to solve for the key (Section 3.2).

**2. Boilerplate is known plaintext.** Every reply ended with the same 118-character sentence (Section 3.1.4),
which encrypted to the same ciphertext in all five sessions (Section 3.3.3):

| Plaintext (repeated by the model or the app) | Sessions | Ciphertext, identical every time |
| --- | --- | --- |
| *This is not a substitute for professional help.* | 1–5 | `Txoc oc vmt i ckzctotkty pml dlmpyccomvin xynd.` |
| *It sounds like you're feeling* | 1, 4, 5 | `Ot cmkvhc nowy amk'ly pyynovg` |
| *It's normal to* | 1, 4, 5 | `Ot'c vmlein tm` |

An attacker who guesses the standard disclaimer gets dozens of plaintext–ciphertext letter pairs for free:
a **known-plaintext attack**. Only **two** independent pairs are needed, because the key (a, b) is the solution
of two linear congruences.

**3. Deterministic encryption.** There is no IV, nonce or per-message randomness. Equal plaintext always gives
equal ciphertext, so repeated openers, list markers (`* `), and line breaks (`\n\n`) form visible patterns
even before the key is known.

**4. Structure survives.** Spaces, punctuation, digits and letter case pass through unchanged. Word lengths
and common words (`ivh` = *and*, 33 times; `ovg` = *-ing*, 48 times; `txy` = *the*) were readable straight
from the capture.

**5. A tiny keyspace.** With m = 26 there are only 12 × 26 = **312** keys. Trying every one of them on the full
4,574-character capture took **0.14 s** on the lab laptop, and a χ² test picked the right key with a score
32 times better than the runner-up (Section 3.2.6). Frequency analysis is not even necessary: brute force alone
breaks this cipher instantly.

## 4.2 Other failures observed

| Failure | Evidence from this lab | Consequence |
| --- | --- | --- |
| **Metadata in the clear** | HTTP request line, `Host: muhammadrafique:5000`, `User-Agent: python-requests/2.34.2`, `Server: BaseHTTP/0.6 Python/3.14.6`, JSON keys `username`/`mood`/`concern`/`reply`, exact `Content-Length` (Section 2.5) | An observer learns who talks to whom, which software runs, which field is which, and how long each message is, without decrypting anything |
| **No integrity or authentication** | Any ciphertext can be altered and re-sent; the server accepts any `POST /submit` from any local process; nothing proves the reply came from the real server | With the recovered key an attacker can forge requests or replace a reply with harmful "advice" undetected. Even without the key, bytes can be altered or replayed |
| **Loopback is not private** | `dumpcap` captured all 70 packets as an ordinary user in the `wireshark` group, no root needed (Section 2.1) | Any account or process with capture rights on the machine can read every session |
| **Homemade cryptography** | A classical cipher hard-coded in `affine.py`, shared between client and server | Violates Kerckhoffs's principle: security rests on the scheme staying secret, and the "key" is in the source code. Once seen, every past and future message is exposed, with no key rotation or forward secrecy |
| **Sensitive data at stake** | Usernames, moods and concerns such as panic before exams or loneliness (Section 3.3.2) | Mental-health information is special-category personal data. A leak harms patients directly |

## 4.3 Protecting local IPC: alternatives

### 4.3.1 Alternative 1: UNIX domain socket with file permissions

**How it works.** Client and server talk through a socket file such as `/run/user/1000/psycare.sock`
instead of TCP port 5000. The kernel copies data directly between the two processes. Nothing is ever sent
over a network interface, so a capture on `lo` sees nothing. Access is controlled by ordinary file
permissions: with mode `0600`, only the owning user can connect. Over the open connection, the server can ask
the kernel who the peer is with `SO_PEERCRED`, which returns the client's PID, UID and GID, and refuse
anyone unexpected (`man 7 unix`).

**What it fixes.** Sniffing on `lo` (the attack in Task 2), connections from other users' processes, and
spoofed clients. It needs no certificates or keys.

**Setup sketch** (Python standard library):

```python
import os, socket, struct

PATH = f"/run/user/{os.getuid()}/psycare.sock"   # per-user runtime directory, mode 0700
srv = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
os.umask(0o177)                                  # socket file is created as 0600
srv.bind(PATH)
srv.listen()
conn, _ = srv.accept()
pid, uid, gid = struct.unpack("3i", conn.getsockopt(
    socket.SOL_SOCKET, socket.SO_PEERCRED, struct.calcsize("3i")))
if uid != os.getuid():
    conn.close()                                 # only our own user may talk to the server
```

The client connects with `socket.AF_UNIX` to the same path. HTTP can run on top unchanged; for example,
uvicorn has `--uds`.

**Residual risk.** No encryption: root, or anything able to attach to either process (ptrace, eBPF), can
still read the data. It only works on one machine.

### 4.3.2 Alternative 2: TLS 1.3 with a self-signed certificate

**How it works.** The client and server keep using TCP, but wrap it in TLS 1.3 (RFC 8446). The handshake
uses ephemeral (EC)DHE key exchange, so every session gets fresh keys and **forward secrecy**. All records are
protected with an AEAD cipher (AES-GCM or ChaCha20-Poly1305), which provides confidentiality and integrity
together. On loopback, a self-signed certificate is enough, as long as the client **pins** it: it trusts only
that exact certificate, not the system CA store.

**What it fixes.** Reading traffic on `lo` (the capture would show only encrypted TLS records), tampering
and forgery (the AEAD tag check fails), server impersonation (certificate pinning), and replay. Identical
plaintexts no longer produce identical ciphertexts. HTTP headers and JSON keys are encrypted too.

**Setup sketch:**

```bash
openssl req -x509 -newkey ed25519 -nodes -days 365 \
  -keyout server.key -out server.crt \
  -subj "/CN=muhammadrafique" -addext "subjectAltName=DNS:muhammadrafique,IP:127.0.0.1"
chmod 600 server.key
```

```python
import ssl
# server
ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ctx.minimum_version = ssl.TLSVersion.TLSv1_3
ctx.load_cert_chain("server.crt", "server.key")
httpd.socket = ctx.wrap_socket(httpd.socket, server_side=True)
# client: trust only this certificate
requests.post("https://muhammadrafique:5000/submit", json=payload, verify="server.crt")
```

The lab machine's OpenSSL 3.6.3 supports TLS 1.3. For **mutual TLS**, also issue a client certificate and set
`ctx.verify_mode = ssl.CERT_REQUIRED` on the server, so only the real client can connect.

**Residual risk.** The private key must be protected (`0600`, never committed). An observer still sees that
a connection exists and roughly how large it is. Certificates need renewal.

### 4.3.3 Alternative 3 (optional): authenticated encryption in the application

If the transport cannot change, the affine cipher can be replaced inside the JSON with a modern AEAD such as
**AES-256-GCM** (NIST SP 800-38D) or **ChaCha20-Poly1305** (RFC 8439), for example `AESGCM` from the Python
`cryptography` package. Each message gets a fresh random 96-bit nonce, sent alongside the ciphertext, and
decryption fails loudly if a single bit was changed. A nonce must **never** be reused with the same key. The key
has to come from a proper exchange or a protected file, not the source code. This fixes confidentiality and
integrity of the fields. Unlike TLS, it leaves headers, JSON keys and message timing visible, and makes key
management the application's problem.

## 4.4 Comparison

| Option | Threats addressed | Effort | Residual risk |
| --- | --- | --- | --- |
| Current affine cipher | None in practice: broken in 0.14 s | — | Everything readable and forgeable |
| **UNIX domain socket, 0600 + `SO_PEERCRED`** | Sniffing on `lo`; other local users; spoofed clients | Low: change bind/connect, stdlib only | No encryption against root or ptrace; single host only |
| **TLS 1.3, self-signed + pinning** (opt. mTLS) | Eavesdropping, tampering, impersonation, replay; metadata hidden inside the tunnel | Medium: certificate generation and handling | Key file protection; connection timing and size still visible |
| AEAD fields (AES-GCM / ChaCha20-Poly1305) | Confidentiality and integrity of the encrypted values | Medium: key management, nonce discipline | Metadata and headers in clear; nonce reuse is catastrophic |
| **UDS + TLS** (defence in depth) | All of the above on one host | Medium | Compromise of the user account or root |

**Recommendation.** For a local-only service like PsycoSupport, use a **UNIX domain socket with `0600`
permissions and `SO_PEERCRED` checks**: it removes the traffic from the network stack entirely, and it is the
smallest change. Where client and server might ever run on separate hosts or VMs, as the upstream README
allows, use **TLS 1.3 with a pinned certificate** (and mTLS). In both cases, delete the homemade cipher and its
hard-coded key.

## 4.5 Sources

- E. Rescorla, *The Transport Layer Security (TLS) Protocol Version 1.3*, RFC 8446, IETF, August 2018.
- Y. Nir, A. Langley, *ChaCha20 and Poly1305 for IETF Protocols*, RFC 8439, IETF, June 2018.
- M. Dworkin, *Recommendation for Block Cipher Modes of Operation: Galois/Counter Mode (GCM) and GMAC*,
  NIST SP 800-38D, November 2007.
- `unix(7)` (`man 7 unix`), Linux man-pages: `AF_UNIX` sockets, socket file permissions, `SO_PEERCRED`.
- Python Software Foundation, `ssl` module documentation: `SSLContext`, `TLSVersion.TLSv1_3`.
- A. Kerckhoffs, "La cryptographie militaire", *Journal des sciences militaires*, vol. IX, 1883.
- Own measurements: Sections 2–3 of this report (`evidence/task2/`, `report/figures/`).
