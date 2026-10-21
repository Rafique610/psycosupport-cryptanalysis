"""Feed each row of test_cases.csv to the real PsycoSupport client, one session at a time."""

import csv
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CASES = Path(__file__).with_name("test_cases.csv")
PAUSE_SECONDS = 5  # gap between sessions so the TCP streams are clearly separate

for row in csv.DictReader(CASES.open()):
    print(f"--- case {row['case_id']} ({row['username']}, {row['mood']})", flush=True)
    answers = f"{row['username']}\n{row['mood']}\n{row['concern']}\n"
    subprocess.run([sys.executable, "psycare_lab/client.py"], input=answers, text=True, cwd=ROOT, check=True)
    time.sleep(PAUSE_SECONDS)
