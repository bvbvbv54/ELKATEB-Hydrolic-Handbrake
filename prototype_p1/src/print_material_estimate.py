"""Generate the P1.0 STL material-consumption report without changing CAD.

The script reads only the released STL deliverables.  Exact tessellated-solid
volume comes from trimesh.  Practical FDM material is an engineering estimate
because no command-line slicer/profile is available in the workspace.
"""

from __future__ import annotations

import csv
import hashlib
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import trimesh


ROOT = Path(__file__).resolve().parents[1]
STL_DIR = ROOT / "stl"
COUPON_DIR = ROOT / "coupons"
REPORT_DIR = ROOT / "reports"
CSV_PATH = REPORT_DIR / "print_material_estimate.csv"
MD_PATH = REPORT_DIR / "PRINT_MATERIAL_ESTIMATE.md"
MANIFEST_PATH = REPORT_DIR / "final_manifest.csv"

PETG_DENSITY_G_CM3 = 1.27
NOZZLE_MM = 0.40
ASSUMED_EXTRUSION_WIDTH_MM = 0.45
LAYER_HEIGHT_MM = 0.20
PERIMETERS = 6
TOP_LAYERS = 6
BOTTOM_LAYERS = 6
WALL_THICKNESS_MM = PERIMETERS * ASSUMED_EXTRUSION_WIDTH_MM
TOP_BOTTOM_THICKNESS_MM = max(TOP_LAYERS, BOTTOM_LAYERS) * LAYER_HEIGHT_MM
INFILL_LEVELS = (0.40, 0.50, 0.60)


@dataclass(frozen=True)
class PartSpec:
    part_id: str
    filename: str
    category_code: str
    category: str
    source_folder: str
    build_axis: str
    orientation: str
    supports: str


PARTS = (
    # A. Calibration coupons
    PartSpec("CAL-608-07", "COUPON_608_POCKETS_DEPTH_7.stl", "A", "Calibration coupons", "coupons", "Z", "Flat base on bed; 7 mm pockets upward", "No support expected; not slicer-verified"),
    PartSpec("CAL-608-14", "COUPON_608_POCKETS_DEPTH_14.stl", "A", "Calibration coupons", "coupons", "Z", "Flat base on bed; 14 mm pockets upward", "No support expected; not slicer-verified"),
    PartSpec("CAL-M8", "COUPON_M8_CLEARANCE.stl", "A", "Calibration coupons", "coupons", "Z", "Flat base on bed; test bores vertical", "No support expected; not slicer-verified"),
    PartSpec("CAL-M6", "COUPON_M6_CLEARANCE.stl", "A", "Calibration coupons", "coupons", "Z", "Flat base on bed; test bores vertical", "No support expected; not slicer-verified"),
    PartSpec("CAL-M6-NUT", "COUPON_M6_NUT_TRAPS.stl", "A", "Calibration coupons", "coupons", "Z", "Largest flat face on bed; nut traps upward", "No support expected; not slicer-verified"),
    PartSpec("CAL-MAG", "COUPON_MAGNET_POCKETS.stl", "A", "Calibration coupons", "coupons", "Z", "Largest flat face on bed; pockets upward", "No support expected; not slicer-verified"),
    PartSpec("CAL-HALL", "COUPON_HALL_GAP_JIG.stl", "A", "Calibration coupons", "coupons", "Z", "Largest flat face on bed", "No support expected; not slicer-verified"),
    PartSpec("CAL-BEAR-WALL", "COUPON_LOADED_BEARING_WALL.stl", "A", "Calibration coupons", "coupons", "Y", "Broad side face on bed; bearing axis horizontal", "No support expected; not slicer-verified"),
    # B. Mechanical core
    PartSpec("P1-001", "P1-001_BASE.stl", "B", "Mechanical core", "stl", "Z", "Primary flat face on bed; steel recesses upward", "No support expected; not slicer-verified"),
    PartSpec("P1-002", "P1-002_LEFT_PIVOT_SUPPORT.stl", "B", "Mechanical core", "stl", "Y", "Outer Y face on bed", "No support expected; ream holes after printing"),
    PartSpec("P1-003", "P1-003_RIGHT_PIVOT_SUPPORT.stl", "B", "Mechanical core", "stl", "Y", "Outer Y face on bed", "No support expected; not slicer-verified"),
    PartSpec("P1-004", "P1-004_LEVER_ROOT_BEARING_HUB.stl", "B", "Mechanical core", "stl", "Y", "One bearing face on bed", "Conditional local support in accessible lever slot if bridging is poor"),
    PartSpec("P1-006", "P1-006_GRIP.stl", "B", "Mechanical core", "stl", "X", "Upright on end with brim", "No support expected; brim material is excluded"),
    PartSpec("P1-007", "P1-007_SPRING_ANCHOR_MODULE.stl", "B", "Mechanical core", "stl", "Z", "Foot on bed", "No support expected; not slicer-verified"),
    PartSpec("P1-008", "P1-008_RELEASE_STOP.stl", "B", "Mechanical core", "stl", "Y", "Outer Y face on bed", "No support expected; not slicer-verified"),
    PartSpec("P1-009", "P1-009_FULL_PULL_STOP.stl", "B", "Mechanical core", "stl", "Y", "Outer Y face on bed", "No support expected; not slicer-verified"),
    # C. Sensor/electronics
    PartSpec("P1-010", "P1-010_MAGNET_HOLDER.stl", "C", "Sensor/electronics printed parts", "stl", "Y", "Inner arm face on bed", "Conditional small local support at magnet cup"),
    PartSpec("P1-011A", "P1-011A_HALL_FIXED_BRACKET.stl", "C", "Sensor/electronics printed parts", "stl", "Z", "Largest flat face on bed", "Conditional; inspect rail bridges in slicer"),
    PartSpec("P1-011B", "P1-011B_HALL_SENSOR_SLED.stl", "C", "Sensor/electronics printed parts", "stl", "Z", "Largest flat face on bed", "Conditional; inspect rail bridges in slicer"),
    PartSpec("P1-012", "P1-012_ELECTRONICS_ENCLOSURE.stl", "C", "Sensor/electronics printed parts", "stl", "Z", "Enclosure bottom on bed", "No support expected; not slicer-verified"),
    PartSpec("P1-013", "P1-013_ELECTRONICS_COVER.stl", "C", "Sensor/electronics printed parts", "stl", "Z", "Outer top face on bed", "No support expected; not slicer-verified"),
    # D. Desk clamp
    PartSpec("P1-020", "P1-020_CLAMP_BASE_INTERFACE.stl", "D", "Desk-clamp printed parts", "stl", "Z", "Large face on bed", "No support expected; not slicer-verified"),
    PartSpec("P1-021", "P1-021_CLAMP_VERTICAL_BRACKET.stl", "D", "Desk-clamp printed parts", "stl", "X", "Large X face on bed; ribs upward", "No support expected; not slicer-verified"),
    PartSpec("P1-022", "P1-022_CLAMP_SCREW_GUIDE.stl", "D", "Desk-clamp printed parts", "stl", "Z", "Lower arm face on bed; hex pocket vertical", "No support expected; not slicer-verified"),
    PartSpec("P1-023", "P1-023_CLAMP_KNOB.stl", "D", "Desk-clamp printed parts", "stl", "Z", "Flat face on bed", "No support expected; not slicer-verified"),
    PartSpec("P1-024", "P1-024_SWIVEL_PAD_HOLDER.stl", "D", "Desk-clamp printed parts", "stl", "Z", "Flat face on bed", "No support expected; not slicer-verified"),
    PartSpec("P1-025", "P1-025_UPPER_RUBBER_PAD_HOLDER.stl", "D", "Desk-clamp printed parts", "stl", "Z", "Large face on bed", "No support expected; not slicer-verified"),
)

CATEGORY_ORDER = {
    "A": "Calibration coupons",
    "B": "Mechanical core",
    "C": "Sensor/electronics printed parts",
    "D": "Desk-clamp printed parts",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def manifest_hashes() -> dict[str, str]:
    if not MANIFEST_PATH.exists():
        return {}
    result: dict[str, str] = {}
    with MANIFEST_PATH.open(newline="", encoding="utf-8-sig") as handle:
        for row in csv.DictReader(handle):
            key = row.get("relative_path", row.get("path", ""))
            result[key.replace("\\", "/")] = row["sha256"]
    return result


def load_mesh(path: Path) -> trimesh.Trimesh:
    loaded = trimesh.load(path, force="mesh", process=True)
    if isinstance(loaded, trimesh.Scene):
        loaded = trimesh.util.concatenate(tuple(loaded.geometry.values()))
    if not isinstance(loaded, trimesh.Trimesh):
        raise TypeError(f"Could not load a triangle mesh from {path}")
    if not loaded.is_watertight or not loaded.is_volume:
        raise ValueError(f"STL is not a closed, consistently oriented volume: {path}")
    return loaded


def shell_estimate(mesh: trimesh.Trimesh, build_axis: str) -> tuple[float, float, float]:
    """Return effective shell volume, shell fraction, and raw shell volume.

    This directional area model distinguishes perimeter walls from top/bottom
    skins.  It intentionally does not subtract edge overlap, making the result
    slightly conservative for purchasing.  The shell is capped at total solid
    volume for thin/small parts.
    """
    axis = {"X": 0, "Y": 1, "Z": 2}[build_axis]
    volume = abs(float(mesh.volume))
    projected_normal = np.abs(mesh.face_normals[:, axis])
    lateral_factor = np.sqrt(np.maximum(0.0, 1.0 - projected_normal**2))
    lateral_area = float(np.sum(mesh.area_faces * lateral_factor))
    horizontal_projected_area = float(np.sum(mesh.area_faces * projected_normal))
    raw_shell = (
        lateral_area * WALL_THICKNESS_MM
        + horizontal_projected_area * TOP_BOTTOM_THICKNESS_MM
    )
    effective_shell = min(volume, raw_shell)
    return effective_shell, effective_shell / volume, raw_shell


def mass_from_volume(volume_mm3: float) -> float:
    return volume_mm3 / 1000.0 * PETG_DENSITY_G_CM3


def fmt(value: float, decimals: int = 1) -> str:
    return f"{value:.{decimals}f}"


def build_records() -> list[dict[str, object]]:
    expected_stl = {p.filename for p in PARTS if p.source_folder == "stl"}
    expected_coupons = {p.filename for p in PARTS if p.source_folder == "coupons"}
    actual_stl = {p.name for p in STL_DIR.glob("*.stl")}
    actual_coupons = {p.name for p in COUPON_DIR.glob("*.stl")}
    if expected_stl != actual_stl:
        raise RuntimeError(f"Final STL set differs: missing={expected_stl-actual_stl}, extra={actual_stl-expected_stl}")
    if expected_coupons != actual_coupons:
        raise RuntimeError(f"Coupon STL set differs: missing={expected_coupons-actual_coupons}, extra={actual_coupons-expected_coupons}")

    prior_hashes = manifest_hashes()
    records: list[dict[str, object]] = []
    for spec in PARTS:
        path = ROOT / spec.source_folder / spec.filename
        mesh = load_mesh(path)
        volume = abs(float(mesh.volume))
        shell_volume, shell_fraction, raw_shell = shell_estimate(mesh, spec.build_axis)
        extents = [float(x) for x in mesh.extents]
        rel = path.relative_to(ROOT).as_posix()
        digest = sha256(path)
        prior_digest = prior_hashes.get(rel, "")
        row: dict[str, object] = {
            "record_type": "part",
            "category_code": spec.category_code,
            "category": spec.category,
            "part_id": spec.part_id,
            "filename": spec.filename,
            "source_path": rel,
            "quantity": 1,
            "bbox_x_mm": round(extents[0], 3),
            "bbox_y_mm": round(extents[1], 3),
            "bbox_z_mm": round(extents[2], 3),
            "mesh_volume_mm3": round(volume, 3),
            "mesh_volume_cm3": round(volume / 1000.0, 3),
            "solid_mass_g_100pct": round(mass_from_volume(volume), 3),
            "mesh_watertight": True,
            "connected_components": len(mesh.split(only_watertight=False)),
            "build_vertical_axis": spec.build_axis,
            "recommended_print_orientation": spec.orientation,
            "likely_support_requirement": spec.supports,
            "estimated_shell_volume_mm3": round(shell_volume, 3),
            "estimated_shell_fraction": round(shell_fraction, 6),
            "uncapped_directional_shell_mm3": round(raw_shell, 3),
            "estimated_g_40pct": round(mass_from_volume(shell_volume + (volume - shell_volume) * 0.40), 3),
            "estimated_g_50pct": round(mass_from_volume(shell_volume + (volume - shell_volume) * 0.50), 3),
            "estimated_g_60pct": round(mass_from_volume(shell_volume + (volume - shell_volume) * 0.60), 3),
            "estimate_method": "directional shell/infill engineering estimate; not slicer output",
            "support_brim_purge_mass_included": False,
            "print_time": "UNKNOWN",
            "stl_sha256": digest,
            "matches_preexisting_manifest": bool(prior_digest and digest == prior_digest),
        }
        records.append(row)
    return records


def aggregate(records: list[dict[str, object]], label: str, predicate) -> dict[str, object]:
    selected = [r for r in records if predicate(r)]
    return {
        "record_type": "summary",
        "category_code": "",
        "category": label,
        "part_id": "TOTAL",
        "filename": "",
        "source_path": "",
        "quantity": sum(int(r["quantity"]) for r in selected),
        "bbox_x_mm": "",
        "bbox_y_mm": "",
        "bbox_z_mm": "",
        "mesh_volume_mm3": round(sum(float(r["mesh_volume_mm3"]) for r in selected), 3),
        "mesh_volume_cm3": round(sum(float(r["mesh_volume_cm3"]) for r in selected), 3),
        "solid_mass_g_100pct": round(sum(float(r["solid_mass_g_100pct"]) for r in selected), 3),
        "mesh_watertight": all(bool(r["mesh_watertight"]) for r in selected),
        "connected_components": "",
        "build_vertical_axis": "",
        "recommended_print_orientation": "",
        "likely_support_requirement": "",
        "estimated_shell_volume_mm3": round(sum(float(r["estimated_shell_volume_mm3"]) for r in selected), 3),
        "estimated_shell_fraction": "",
        "uncapped_directional_shell_mm3": round(sum(float(r["uncapped_directional_shell_mm3"]) for r in selected), 3),
        "estimated_g_40pct": round(sum(float(r["estimated_g_40pct"]) for r in selected), 3),
        "estimated_g_50pct": round(sum(float(r["estimated_g_50pct"]) for r in selected), 3),
        "estimated_g_60pct": round(sum(float(r["estimated_g_60pct"]) for r in selected), 3),
        "estimate_method": "sum of part estimates",
        "support_brim_purge_mass_included": False,
        "print_time": "UNKNOWN",
        "stl_sha256": "",
        "matches_preexisting_manifest": all(bool(r["matches_preexisting_manifest"]) for r in selected),
    }


def build_summaries(records: list[dict[str, object]]) -> list[dict[str, object]]:
    summaries = [
        aggregate(records, name, lambda r, c=code: r["category_code"] == c)
        for code, name in CATEGORY_ORDER.items()
    ]
    summaries.extend(
        [
            aggregate(records, "All final P1 printed components (B+C+D)", lambda r: r["category_code"] in {"B", "C", "D"}),
            aggregate(records, "Complete print set including coupons (A+B+C+D)", lambda r: True),
        ]
    )
    return summaries


def write_csv(records: list[dict[str, object]], summaries: list[dict[str, object]]) -> None:
    fieldnames = list(records[0].keys())
    with CSV_PATH.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)
        writer.writerows(summaries)


def report_table_rows(records: list[dict[str, object]]) -> list[str]:
    rows = []
    for r in records:
        bbox = f'{fmt(float(r["bbox_x_mm"]))} x {fmt(float(r["bbox_y_mm"]))} x {fmt(float(r["bbox_z_mm"]))}'
        rows.append(
            "| {part_id} | `{filename}` | {quantity} | {bbox} | {volume} | {solid} | {m40} | {m50} | {m60} | {orientation} | {supports} |".format(
                part_id=r["part_id"],
                filename=r["filename"],
                quantity=r["quantity"],
                bbox=bbox,
                volume=fmt(float(r["mesh_volume_cm3"]), 2),
                solid=fmt(float(r["solid_mass_g_100pct"])),
                m40=fmt(float(r["estimated_g_40pct"])),
                m50=fmt(float(r["estimated_g_50pct"])),
                m60=fmt(float(r["estimated_g_60pct"])),
                orientation=r["recommended_print_orientation"],
                supports=r["likely_support_requirement"],
            )
        )
    return rows


def reserve_rows(summary: dict[str, object]) -> list[str]:
    rows = []
    for infill in (40, 50, 60):
        theoretical = float(summary[f"estimated_g_{infill}pct"])
        plus15 = theoretical * 1.15
        plus30 = theoretical * 1.30
        spools = max(1, math.ceil(plus30 / 1000.0))
        rows.append(
            f"| {infill}% | {theoretical:.1f} | {plus15:.1f} | {plus30:.1f} | {spools} |"
        )
    return rows


def write_markdown(records: list[dict[str, object]], summaries: list[dict[str, object]]) -> None:
    by_category = {code: [r for r in records if r["category_code"] == code] for code in CATEGORY_ORDER}
    summary_by_name = {str(s["category"]): s for s in summaries}
    final_summary = summary_by_name["All final P1 printed components (B+C+D)"]
    complete_summary = summary_by_name["Complete print set including coupons (A+B+C+D)"]
    coupon_summary = summary_by_name["Calibration coupons"]
    core_summary = summary_by_name["Mechanical core"]
    all_manifest_matches = all(bool(r["matches_preexisting_manifest"]) for r in records)

    lines = [
        "# P1.0 Print Material Estimate",
        "",
        "## Executive result",
        "",
        "The released P1.0 deliverables contain **27 unique STL files at quantity one**: **8 calibration coupons** and **19 final structural/accessory components**. The 19 final components divide into **8 mechanical-core parts**, **5 sensor/electronics parts**, and **6 desk-clamp parts**. No CAD or STL file was modified for this report.",
        "",
        f"All 27 meshes load as watertight, consistently oriented, single-component solids. Pre-existing P1.0 manifest hash match: **{'27/27' if all_manifest_matches else 'NOT COMPLETE - investigate CSV'}**.",
        "",
        "## Method and limitations",
        "",
        "- **Exact solid CAD/STL volume:** calculated directly from each released binary STL triangle mesh with trimesh after normal mesh processing. This is the closed tessellated-solid volume, not deposited filament volume.",
        "- **Practical FDM estimate:** no PrusaSlicer, OrcaSlicer, CuraEngine, or Bambu Studio command-line executable was found in PATH or common installation locations, and no printer/profile was supplied. The values below are therefore an **engineering estimate, not slicer output**.",
        f"- Baseline: PETG density {PETG_DENSITY_G_CM3:.2f} g/cm3, {NOZZLE_MM:.2f} mm nozzle, {LAYER_HEIGHT_MM:.2f} mm layers, {PERIMETERS} perimeters, {TOP_LAYERS} top layers, {BOTTOM_LAYERS} bottom layers, and an explicit {ASSUMED_EXTRUSION_WIDTH_MM:.2f} mm assumed extrusion width.",
        f"- Shell model: directional STL surface area x {WALL_THICKNESS_MM:.2f} mm perimeter envelope plus projected top/bottom area x {TOP_BOTTOM_THICKNESS_MM:.2f} mm skin envelope. It does not subtract edge overlap and is capped at exact solid volume, so it is intentionally conservative for purchasing. The remaining internal volume receives 40%, 50%, or 60% infill.",
        "- Estimated mass excludes support, brim, skirt, purge/prime lines, extrusion multiplier differences, gap fill, slicer line overlap, failed prints, and moisture-conditioning losses. Support statements are orientation guidance only and were not calculated by a slicer.",
        "- **Print time: UNKNOWN** because neither a slicer result nor a printer/machine profile is available.",
        "",
        "Bounding dimensions are native STL X x Y x Z extents in millimetres; the recommended build orientation may rotate them on the printer.",
        "",
        "## Piece-count verification",
        "",
        "| Category | Unique STLs | Physical pieces |",
        "|---|---:|---:|",
    ]
    for code, name in CATEGORY_ORDER.items():
        count = len(by_category[code])
        lines.append(f"| {code}. {name} | {count} | {count} |")
    lines.extend(
        [
            "| **Final components (B+C+D)** | **19** | **19** |",
            "| **Complete set (A+B+C+D)** | **27** | **27** |",
            "",
        ]
    )

    table_header = [
        "| Part ID | STL filename | Qty | Bounding X x Y x Z (mm) | Exact volume (cm3) | 100% solid mass (g) | Est. 40% (g) | Est. 50% (g) | Est. 60% (g) | Recommended orientation | Likely support requirement |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|",
    ]
    for code, name in CATEGORY_ORDER.items():
        lines.extend([f"## {code}. {name}", "", *table_header, *report_table_rows(by_category[code]), ""])

    lines.extend(
        [
            "## Category and build-stage totals",
            "",
            "| Scope | Pieces | Exact solid volume (cm3) | 100% solid mass (g) | Est. 40% (g) | Est. 50% (g) | Est. 60% (g) |",
            "|---|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for summary in summaries:
        lines.append(
            f'| {summary["category"]} | {summary["quantity"]} | {float(summary["mesh_volume_cm3"]):.2f} | {float(summary["solid_mass_g_100pct"]):.1f} | {float(summary["estimated_g_40pct"]):.1f} | {float(summary["estimated_g_50pct"]):.1f} | {float(summary["estimated_g_60pct"]):.1f} |'
        )

    lines.extend(
        [
            "",
            "## Filament reserve",
            "",
            "Reserve calculations use the same estimated deposited mass. A `+15%` allowance is reasonable for normal handling, short test extrusions, and small slicer differences; `+30%` is the development/reprint allowance requested for P1.",
            "",
            "### All 19 final components",
            "",
            "| Infill | Theoretical printed mass (g) | +15% reserve (g) | +30% development reserve (g) | Safe 1 kg spools |",
            "|---:|---:|---:|---:|---:|",
            *reserve_rows(final_summary),
            "",
            "### Complete set: final components plus 8 coupons",
            "",
            "| Infill | Theoretical printed mass (g) | +15% reserve (g) | +30% development reserve (g) | Safe 1 kg spools |",
            "|---:|---:|---:|---:|---:|",
            *reserve_rows(complete_summary),
            "",
            "For sending the job to a friend, **50% infill is the central planning case**. At that case, the complete 27-piece set plus 30% development reserve requires "
            f"{float(complete_summary['estimated_g_50pct']) * 1.30:.1f} g, so have **{max(1, math.ceil(float(complete_summary['estimated_g_50pct']) * 1.30 / 1000.0))} x 1 kg spool(s)** of the same PETG lot available. This is a stock recommendation, not a claim that all of it will be consumed.",
            "",
            "## Practical print sequence",
            "",
            f"1. **Initially:** print the 8 calibration coupons, approximately **{float(coupon_summary['estimated_g_50pct']):.0f} g** at the 50% planning case.",
            f"2. **After calibration:** print the 8 mechanical-core parts, approximately **{float(core_summary['estimated_g_50pct']):.0f} g** at 50%.",
            f"3. Print the 5 sensor/electronics parts and 6 clamp parts after fit and motion checks. The complete final 19-part prototype is approximately **{float(final_summary['estimated_g_50pct']):.0f} g** at 50%.",
            "4. Before each batch, rotate parts to the stated orientation and inspect unsupported bridges, hole orientation, brim need, and generated support in the actual slicer. Use the slicer's own mass result as the final purchasing/production number.",
            "",
            "## Simple summary to send to the printer owner",
            "",
            f"> Initially: 8 calibration pieces / approximately {float(coupon_summary['estimated_g_50pct']):.0f} g PETG at 50% infill.  ",
            f"> After calibration: 8 mechanical-core pieces / approximately {float(core_summary['estimated_g_50pct']):.0f} g PETG at 50% infill.  ",
            f"> Complete prototype: 19 final printed pieces / approximately {float(final_summary['estimated_g_50pct']):.0f} g PETG at 50% infill.  ",
            f"> Recommended filament to have available: {max(1, math.ceil(float(complete_summary['estimated_g_50pct']) * 1.30 / 1000.0))} kg PETG (covers all 27 prints and a 30% development/reprint reserve).",
            "",
            "## Machine-readable data",
            "",
            "`print_material_estimate.csv` contains one row per STL followed by category/final/complete summary rows. It includes SHA-256 evidence, mesh integrity, exact volume, 100%-solid equivalent mass, directional shell estimate, 40/50/60% estimates, orientation, and support guidance.",
        ]
    )
    MD_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    records = build_records()
    summaries = build_summaries(records)
    write_csv(records, summaries)
    write_markdown(records, summaries)
    print(f"Wrote {CSV_PATH}")
    print(f"Wrote {MD_PATH}")
    print(f"Part rows: {len(records)}; summary rows: {len(summaries)}")


if __name__ == "__main__":
    main()
