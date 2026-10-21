"""Decrypt every intercepted ciphertext with the recovered key and verify it against ground truth.

- client_to_server: must equal the original inputs in scripts/capture/test_cases.csv
- server_to_client: must equal the reply the real client printed during capture (evidence/task2/client_runs.txt)
Writes report/figures/decrypted.csv (case_id, direction, field, ciphertext, plaintext; JSON escapes kept so each
row stays on one line).
"""

import csv
import json
from pathlib import Path

from affine import decrypt

A, B = 17, 8  # recovered from the ciphertext in PC-10 (report section 3.2)
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "report/figures/decrypted.csv"

if __name__ == "__main__":
    with (ROOT / "ciphertexts.csv").open() as f:
        rows = list(csv.DictReader(f))
    with (ROOT / "scripts/capture/test_cases.csv").open() as f:
        truth = {r["case_id"]: r for r in csv.DictReader(f)}
    client_log = (ROOT / "evidence/task2/client_runs.txt").read_text()

    results, failures = [], 0
    for r in rows:
        plain = decrypt(json.loads(f'"{r["ciphertext"]}"'), A, B)
        expected = truth[r["case_id"]][r["field"]] if r["direction"] == "client_to_server" else None
        ok = plain == expected if expected is not None else plain in client_log
        failures += not ok
        results.append({**{k: r[k] for k in ("case_id", "direction", "field", "ciphertext")},
                        "plaintext": json.dumps(plain)[1:-1], "ok": ok})

    with OUT.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["case_id", "direction", "field", "ciphertext", "plaintext"])
        writer.writeheader()
        writer.writerows({k: v for k, v in r.items() if k != "ok"} for r in results)

    for case_id in sorted(truth, key=int):
        case = [r for r in results if r["case_id"] == case_id]
        c2s = all(r["ok"] for r in case if r["direction"] == "client_to_server")
        s2c = all(r["ok"] for r in case if r["direction"] == "server_to_client")
        print(f"case {case_id}: client_to_server {'PASS' if c2s else 'FAIL'} (vs test_cases.csv) | "
              f"server_to_client {'PASS' if s2c else 'FAIL'} (vs client output in client_runs.txt)")

    replies = [json.loads(f'"{r["ciphertext"]}"') for r in rows if r["direction"] == "server_to_client"]
    tail = replies[0][replies[0].rfind("\n\n"):]
    print(f"identical disclaimer ciphertext in {sum(r.endswith(tail) for r in replies)}/{len(replies)} replies")
    print(f"wrote {len(results)} rows to {OUT.relative_to(ROOT)}")
    assert failures == 0, f"{failures} decryption(s) did not match ground truth"
