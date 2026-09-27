"""Create a SHA-256 manifest of user-facing P1 deliverables (tool cache excluded)."""

import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reports" / "final_manifest.csv"


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


paths = []
for path in ROOT.rglob("*"):
    rel = path.relative_to(ROOT)
    if not path.is_file() or rel == Path("reports/final_manifest.csv"):
        continue
    if rel.parts[0] == ".tools" or "__pycache__" in rel.parts:
        continue
    paths.append(path)

with OUT.open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(("relative_path", "bytes", "sha256"))
    for path in sorted(paths):
        w.writerow((path.relative_to(ROOT).as_posix(), path.stat().st_size, digest(path)))
print(f"manifested {len(paths)} deliverables")
