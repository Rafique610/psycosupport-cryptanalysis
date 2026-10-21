"""Build the Google Classroom submission ZIP with the Python standard library (no zip/rsync needed).

Contents: report.pdf, ciphertexts.csv, scripts/, evidence/. Excludes caches, the git-ignored upstream
binaries, and placeholder files.
"""

import shutil
import zipfile
from pathlib import Path

ZIP_NAME = "23i-0747_InfoSec_A1.zip"
ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
STAGE = DIST / "submission"
EXCLUDE_DIRS = {"__pycache__", "upstream", ".venv"}
EXCLUDE_NAMES = {".gitkeep"}
EXCLUDE_SUFFIX = {".pyc"}


def keep(path: Path) -> bool:
    if any(part in EXCLUDE_DIRS for part in path.parts):
        return False
    return path.name not in EXCLUDE_NAMES and path.suffix not in EXCLUDE_SUFFIX


if __name__ == "__main__":
    if DIST.exists():
        shutil.rmtree(DIST)
    STAGE.mkdir(parents=True)

    for name in ("report.pdf", "ciphertexts.csv"):
        shutil.copy2(ROOT / name, STAGE / name)

    for folder in ("scripts", "evidence"):
        for src in sorted((ROOT / folder).rglob("*")):
            if src.is_file() and keep(src.relative_to(ROOT)):
                dst = STAGE / src.relative_to(ROOT)
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)

    zip_path = DIST / ZIP_NAME
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(STAGE.rglob("*")):
            if f.is_file():
                z.write(f, f.relative_to(DIST))

    files = [f for f in STAGE.rglob("*") if f.is_file()]
    print(f"built dist/{ZIP_NAME}: {len(files)} files, {zip_path.stat().st_size / 1024:.0f} KB")
    for f in sorted(files):
        print(f"  {f.relative_to(STAGE)}")
