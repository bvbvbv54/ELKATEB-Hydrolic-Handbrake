"""Confirm the five immutable reference packages still match the audit hashes."""

import csv
import hashlib
import json
from pathlib import Path


WORKSPACE = Path(__file__).resolve().parents[2]
INVENTORY = WORKSPACE / "analysis_generated" / "model_inventory.csv"
OUT = WORKSPACE / "prototype_p1" / "reports" / "reference_source_integrity.json"


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


rows = list(csv.DictReader(INVENTORY.open(encoding="utf-8-sig")))
mismatches = []
for row in rows:
    path = WORKSPACE / Path(row["relative_path"])
    actual = sha256(path) if path.is_file() else None
    if actual != row["sha256"]:
        mismatches.append({"path": row["relative_path"], "expected": row["sha256"], "actual": actual})
report = {"inventory": str(INVENTORY.relative_to(WORKSPACE)), "files_checked": len(rows),
          "mismatches": mismatches, "unchanged": not mismatches}
OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
raise SystemExit(1 if mismatches else 0)
