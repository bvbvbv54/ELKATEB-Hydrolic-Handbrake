"""Package released P1.0 STL files and selected renders for Amine.

This script copies released artifacts only. It never regenerates or edits CAD.
"""

from __future__ import annotations

import csv
import hashlib
import shutil
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HANDOFF = ROOT / "printer_handoff_amine"
ZIP_PATH = ROOT / "AMINE_P1_PRINT_CHECK.zip"
MATERIAL_CSV = ROOT / "reports" / "print_material_estimate.csv"
RELEASE_MANIFEST = ROOT / "reports" / "final_manifest.csv"
PRINT_MANIFEST = HANDOFF / "PRINT_FILE_MANIFEST.csv"

BATCHES = {
    "A": "01_CALIBRATION_FIRST",
    "B": "02_MECHANICAL_CORE_AFTER_CALIBRATION",
    "C": "03_SENSOR_AND_ELECTRONICS",
    "D": "04_TABLE_CLAMP",
}

EXPECTED_COUNTS = {"A": 8, "B": 8, "C": 5, "D": 6}

REFERENCE_IMAGES = {
    "01_ISOMETRIC_ASSEMBLY.png": "assembly overview",
    "09_EXPLODED_VIEW.png": "exploded view",
    "08_PIVOT_SECTION.png": "pivot section",
    "10_DESK_CLAMP_INSTALLED.png": "desk clamp installed",
}


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def read_release_hashes() -> dict[str, str]:
    with RELEASE_MANIFEST.open(newline="", encoding="utf-8-sig") as handle:
        return {
            row["relative_path"].replace("\\", "/"): row["sha256"]
            for row in csv.DictReader(handle)
        }


def read_part_rows() -> list[dict[str, str]]:
    with MATERIAL_CSV.open(newline="", encoding="utf-8-sig") as handle:
        rows = [row for row in csv.DictReader(handle) if row["record_type"] == "part"]
    actual = {code: sum(row["category_code"] == code for row in rows) for code in BATCHES}
    if actual != EXPECTED_COUNTS:
        raise RuntimeError(f"Released P1.0 part-count discrepancy: expected {EXPECTED_COUNTS}, found {actual}")
    if len(rows) != 27:
        raise RuntimeError(f"Expected 27 released STL rows, found {len(rows)}")
    return rows


def oriented_bounds(row: dict[str, str]) -> tuple[float, float, float]:
    x = float(row["bbox_x_mm"])
    y = float(row["bbox_y_mm"])
    z = float(row["bbox_z_mm"])
    axis = row["build_vertical_axis"]
    if axis == "Z":
        return x, y, z
    if axis == "Y":
        return x, z, y
    if axis == "X":
        return y, z, x
    raise ValueError(f"Unsupported build axis {axis!r} for {row['filename']}")


def ensure_clean_layout() -> None:
    HANDOFF.mkdir(parents=True, exist_ok=True)
    allowed_top_files = {
        "README_FOR_AMINE.md",
        "MATERIAL_AND_PRINTING_NOTES.md",
        "MESSAGE_TO_AMINE.txt",
        "PRINT_FILE_MANIFEST.csv",
    }
    allowed_dirs = {*BATCHES.values(), "REFERENCE_IMAGES"}
    unexpected = [
        item.name
        for item in HANDOFF.iterdir()
        if (item.is_file() and item.name not in allowed_top_files)
        or (item.is_dir() and item.name not in allowed_dirs)
    ]
    if unexpected:
        raise RuntimeError(f"Unexpected files in handoff folder; refusing to remove them: {unexpected}")
    for folder in (*BATCHES.values(), "REFERENCE_IMAGES"):
        (HANDOFF / folder).mkdir(exist_ok=True)


def copy_parts(rows: list[dict[str, str]], release_hashes: dict[str, str]) -> list[dict[str, object]]:
    manifest_rows: list[dict[str, object]] = []
    for row in rows:
        code = row["category_code"]
        source = ROOT / Path(row["source_path"])
        source_rel = source.relative_to(ROOT).as_posix()
        source_hash = digest(source)
        released_hash = release_hashes.get(source_rel)
        if not released_hash or source_hash != released_hash:
            raise RuntimeError(f"Source STL does not match released P1.0 manifest: {source_rel}")

        destination = HANDOFF / BATCHES[code] / row["filename"]
        shutil.copy2(source, destination)
        copy_hash = digest(destination)
        if copy_hash != source_hash:
            raise RuntimeError(f"Copied STL hash mismatch: {destination}")

        width, depth, height = oriented_bounds(row)
        manifest_rows.append(
            {
                "batch": BATCHES[code],
                "part_id": row["part_id"],
                "filename": row["filename"],
                "quantity": 1,
                "print_now": "YES - CALIBRATION FIRST" if code == "A" else "NO - SLICER CHECK ONLY UNTIL CALIBRATION",
                "oriented_width_mm": f"{width:.1f}",
                "oriented_depth_mm": f"{depth:.1f}",
                "oriented_height_mm": f"{height:.1f}",
                "native_bbox_x_mm": row["bbox_x_mm"],
                "native_bbox_y_mm": row["bbox_y_mm"],
                "native_bbox_z_mm": row["bbox_z_mm"],
                "recommended_orientation": row["recommended_print_orientation"],
                "support_or_brim_review": row["likely_support_requirement"],
                "exact_stl_volume_cm3": row["mesh_volume_cm3"],
                "engineering_estimate_50pct_g": row["estimated_g_50pct"],
                "estimate_status": "ENGINEERING ESTIMATE ONLY - REPLACE WITH REAL SLICER RESULT",
                "source_relative_path": source_rel,
                "handoff_relative_path": destination.relative_to(HANDOFF).as_posix(),
                "source_sha256": source_hash,
                "copy_sha256": copy_hash,
                "hashes_match": True,
            }
        )
    return manifest_rows


def copy_images() -> None:
    output = HANDOFF / "REFERENCE_IMAGES"
    for filename in REFERENCE_IMAGES:
        source = ROOT / "renders" / filename
        if not source.is_file():
            raise FileNotFoundError(source)
        destination = output / filename
        shutil.copy2(source, destination)
        if digest(source) != digest(destination):
            raise RuntimeError(f"Copied image hash mismatch: {destination}")


def write_manifest(rows: list[dict[str, object]]) -> None:
    with PRINT_MANIFEST.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def create_zip() -> list[str]:
    files = sorted(path for path in HANDOFF.rglob("*") if path.is_file())
    with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in files:
            archive.write(path, path.relative_to(HANDOFF).as_posix())
    with zipfile.ZipFile(ZIP_PATH) as archive:
        names = archive.namelist()
        bad = archive.testzip()
        if bad:
            raise RuntimeError(f"ZIP CRC failure: {bad}")
    return names


def validate(rows: list[dict[str, object]], zip_names: list[str]) -> None:
    files = [path for path in HANDOFF.rglob("*") if path.is_file()]
    stls = [path for path in files if path.suffix.lower() == ".stl"]
    images = [path for path in files if path.suffix.lower() == ".png"]
    required_docs = {
        "README_FOR_AMINE.md",
        "MATERIAL_AND_PRINTING_NOTES.md",
        "MESSAGE_TO_AMINE.txt",
        "PRINT_FILE_MANIFEST.csv",
    }
    top_docs = {path.name for path in files if path.parent == HANDOFF}
    if len(files) != 35 or len(zip_names) != 35:
        raise RuntimeError(f"Expected 35 handoff files and ZIP entries; found {len(files)} and {len(zip_names)}")
    if len(stls) != 27 or len(images) != 4 or top_docs != required_docs:
        raise RuntimeError(
            f"Handoff composition invalid: stls={len(stls)}, images={len(images)}, top_docs={sorted(top_docs)}"
        )
    if len(rows) != 27 or len({row["filename"] for row in rows}) != 27:
        raise RuntimeError("Manifest does not contain 27 unique STL rows")


def main() -> None:
    ensure_clean_layout()
    rows = read_part_rows()
    release_hashes = read_release_hashes()
    manifest_rows = copy_parts(rows, release_hashes)
    copy_images()
    write_manifest(manifest_rows)
    zip_names = create_zip()
    validate(manifest_rows, zip_names)

    largest = max(
        manifest_rows,
        key=lambda row: max(
            float(row["oriented_width_mm"]),
            float(row["oriented_depth_mm"]),
            float(row["oriented_height_mm"]),
        ),
    )
    print(f"Handoff folder: {HANDOFF}")
    print(f"ZIP: {ZIP_PATH}")
    print("Verified released counts: A=8, B=8, C=5, D=6; final=19; complete=27")
    print("Handoff files: 35; STL files: 27; reference images: 4; top-level documents: 4")
    print(
        "Largest oriented part: "
        f"{largest['filename']} "
        f"{largest['oriented_width_mm']} x {largest['oriented_depth_mm']} x {largest['oriented_height_mm']} mm"
    )
    print(f"ZIP SHA-256: {digest(ZIP_PATH)}")


if __name__ == "__main__":
    main()
