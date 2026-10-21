# Appendix: Reproducing the Results

Everything in this report is produced by scripts in the repository, run through `uv` and wrapped as
`task` commands (`go-task`). All runs are offline on Kali Linux over loopback `127.0.0.1`.

## A.1 Setup

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh                       # Python env manager
sh -c "$(curl -fsSL https://taskfile.dev/install.sh)" -- -b ~/.local/bin   # task runner
curl -fsSL https://ollama.com/install.sh | sh && ollama pull llama3.2 # local LLM
echo "127.0.0.1 muhammadrafique" | sudo tee -a /etc/hosts             # host file (own name)
uv sync                                                               # project dependencies
```

## A.2 Pipeline

| Step | Command | Output |
| --- | --- | --- |
| Run the server | `task server` | HTTP server on `127.0.0.1:5000` |
| Capture loopback (terminal 1) | `task capture` | `evidence/task2/session_all.pcap` |
| Send 5 test cases (terminal 2) | `task run-cases` | 5 sessions through the real client |
| Extract ciphertexts | `task extract` | `ciphertexts.csv` (20 rows) |
| Frequency analysis | `task freq` | `report/figures/` tables + charts |
| Recover the key | `task recover` | (a, b) = (17, 8), full working |
| Decrypt everything | `task decrypt` | `report/figures/decrypted.csv`, 5/5 PASS |
| Build this PDF | `task report` | `report.pdf` |

## A.3 Scripts

| Path | Purpose |
| --- | --- |
| `psycare_lab/{server,client,affine}.py` | The app written to the brief (affine cipher + Ollama) |
| `scripts/capture/test_cases.csv`, `run_cases.py` | Five synthetic sessions and the runner |
| `scripts/capture/extract_ciphertexts.py` | pcap → `ciphertexts.csv` (standard library only) |
| `scripts/frequency/{english,count,patterns,plot}.py` | Letter frequencies, patterns, charts |
| `scripts/cipher/{affine,recover_key,decrypt_all}.py` | Attacker toolkit, key recovery, decryption |
| `scripts/report/build_report.py` | Assembles this PDF from `report/sections/` |

The affine key was recovered from intercepted ciphertext alone (Section 3.2); the key in
`psycare_lab/affine.py` was consulted only as a final confirmation.
