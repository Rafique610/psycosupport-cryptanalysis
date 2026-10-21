# 1. Offline Environment Deployment

## 1.1 What was installed

| Component | Version | How |
| --- | --- | --- |
| Kali GNU/Linux Rolling | kernel 7.1.5+kali-amd64 | host OS |
| Ollama | 0.40.7 | official script `curl -fsSL https://ollama.com/install.sh \| sh`, running as the `ollama` systemd service |
| Model `llama3.2` (3B) | ID `a80c4f17acd5`, 2.0 GB | `ollama pull llama3.2` |
| uv | 0.13.4 | Python environment from `pyproject.toml` + `uv.lock` (`ollama`, `requests`) |
| go-task | 3.54.0 | `Taskfile.yml` shortcuts (`task server`, `task client`, `task ollama-check`, `task offline-proof`) |

The brief's install command (`curl -fsSL https://ollama.com | sh`) downloads the Ollama web page, not the
installer; the real script lives at `/install.sh`.

## 1.2 Model choice

`llama3.2` (3B parameters) is the brief's first suggestion and fits the hardware comfortably, so `phi3` or
`llama3.2:1b` were not needed. It is a small instruction-tuned model, which keeps replies fast on a laptop
while still following the system prompt's style constraints.

## 1.3 Hardware

- CPU: 13th Gen Intel Core i5-13420H, 12 threads
- RAM: 15 GiB
- GPU: NVIDIA GeForce RTX 3050 6 GB Laptop GPU. Ollama detected it through Vulkan (open-source NVK driver),
  with about 5.4 GiB available for inference.

## 1.4 The PsycoSupport pipeline

The published repository contains only pre-built binaries whose server still calls the Groq cloud API, so
`psycare_lab/` was written to the brief's specification:

- `server.py`: HTTP server bound to `127.0.0.1:5000`, endpoint `POST /submit`. It decrypts the patient's
  username, mood and concern, sends them to the local `llama3.2` model with a restrictive system prompt,
  and returns the encrypted reply.
- `client.py`: terminal client that encrypts the three fields, sends them, and decrypts the answer.
- `affine.py`: the Affine cipher both sides use.

## 1.5 Offline proof

On 21 October 2026 at 6:38 PM (UTC+05:00 · 13:38 UTC), networking was switched off with `nmcli networking off`:

1. `nmcli networking` reported `disabled`, and `curl https://ollama.com` failed with
   *Could not resolve host* (no internet).
2. `ollama run llama3.2 "Say hi in five words"` still answered: *Hello from the digital realm*.
3. `server.py` started and listened on `127.0.0.1:5000` (`ss -ltnp`).
4. A full client request (mood *stressed*, concern about exams) returned HTTP 200. The reply crossed the
   loopback as ciphertext and decrypted to a complete supportive answer.

Networking was then switched back on.

Evidence (text logs, `evidence/task1/`):

- `01-ollama-list.txt`: Ollama version and installed model
- `02-offline-ollama-run.txt`: networking disabled, no DNS, model answers
- `03-server-start.txt`: server startup
- `04-ss-port-5000.txt`: server bound to `127.0.0.1:5000`
- `05-offline-end-to-end.txt`: offline request, ciphertext on the wire, decrypted reply

Screenshots (taken 21 October 2026, 7:54 to 7:55 PM, UTC+05:00 · 14:54 to 14:55 UTC):

![Figure 1.1: `task ollama-check`: llama3.2 installed (3.2B, Q4_K_M) and the Ollama API answering on localhost:11434](../../evidence/task1/06-ollama-check.png)

![Figure 1.2: `task offline-proof`: networking disabled, ollama.com unresolvable, llama3.2 still answers](../../evidence/task1/07-offline-proof.png)

![Figure 1.3: `task server`: PsycoSupport server started on 127.0.0.1:5000 with llama3.2](../../evidence/task1/08-server-start.png)

![Figure 1.4: `ss -ltnp`: the server listens only on the loopback address 127.0.0.1:5000](../../evidence/task1/09-ss-port-5000.png)
