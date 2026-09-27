"""Independent round-trip verification of exported P1 files."""

from __future__ import annotations

import json
from pathlib import Path

import cadquery as cq
import ezdxf
import trimesh
from PIL import Image

from common import ROOT


def main():
    records = []
    failed = []
    for path in sorted((ROOT / "step").glob("*.step")) + sorted((ROOT / "coupons").glob("*.step")):
        try:
            obj = cq.importers.importStep(str(path)).val()
            bb = obj.BoundingBox()
            rec = {"path": str(path.relative_to(ROOT)), "format": "STEP", "valid": obj.isValid(),
                   "solids": len(obj.Solids()), "xlen": bb.xlen, "ylen": bb.ylen, "zlen": bb.zlen}
            if not rec["valid"] or rec["solids"] < 1: failed.append(rec)
        except Exception as exc:
            rec = {"path": str(path.relative_to(ROOT)), "format": "STEP", "valid": False, "error": str(exc)}
            failed.append(rec)
        records.append(rec)

    for path in sorted((ROOT / "stl").glob("*.stl")) + sorted((ROOT / "coupons").glob("*.stl")):
        try:
            loaded = trimesh.load(path, force="scene")
            geometries = list(loaded.geometry.values())
            bounds = loaded.bounds
            rec = {"path": str(path.relative_to(ROOT)), "format": "STL", "valid": bool(geometries),
                   "mesh_components": len(geometries), "watertight_all": all(g.is_watertight for g in geometries),
                   "faces": int(sum(len(g.faces) for g in geometries)),
                   "xlen": float(bounds[1][0] - bounds[0][0]), "ylen": float(bounds[1][1] - bounds[0][1]),
                   "zlen": float(bounds[1][2] - bounds[0][2])}
            if not rec["valid"] or not rec["watertight_all"]: failed.append(rec)
        except Exception as exc:
            rec = {"path": str(path.relative_to(ROOT)), "format": "STL", "valid": False, "error": str(exc)}
            failed.append(rec)
        records.append(rec)

    for path in sorted((ROOT / "dxf").glob("*.dxf")):
        try:
            doc = ezdxf.readfile(path)
            rec = {"path": str(path.relative_to(ROOT)), "format": "DXF", "valid": True,
                   "units_code": doc.units, "entities": len(doc.modelspace())}
            if doc.units != ezdxf.units.MM: rec["valid"] = False; failed.append(rec)
        except Exception as exc:
            rec = {"path": str(path.relative_to(ROOT)), "format": "DXF", "valid": False, "error": str(exc)}
            failed.append(rec)
        records.append(rec)

    for path in sorted((ROOT / "renders").glob("*.png")):
        try:
            with Image.open(path) as im:
                rec = {"path": str(path.relative_to(ROOT)), "format": "PNG", "valid": im.width >= 800 and im.height >= 600,
                       "width": im.width, "height": im.height}
            if not rec["valid"]: failed.append(rec)
        except Exception as exc:
            rec = {"path": str(path.relative_to(ROOT)), "format": "PNG", "valid": False, "error": str(exc)}
            failed.append(rec)
        records.append(rec)

    report = {"records": records, "summary": {"files": len(records), "failed": len(failed)}, "failed": failed}
    (ROOT / "reports" / "export_roundtrip.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    lines = ["# Export round-trip verification\n\n",
             f"Files checked: **{len(records)}**. Failures: **{len(failed)}**.\n\n",
             "|Format|Files|Valid|\n|---|---:|---:|\n"]
    for fmt in ("STEP", "STL", "DXF", "PNG"):
        group = [r for r in records if r["format"] == fmt]
        lines.append(f"|{fmt}|{len(group)}|{sum(bool(r['valid']) for r in group)}|\n")
    if failed:
        lines.append("\n## Failures\n\n```json\n" + json.dumps(failed, indent=2) + "\n```\n")
    (ROOT / "reports" / "EXPORT_ROUNDTRIP.md").write_text("".join(lines), encoding="utf-8")
    print(json.dumps(report["summary"], indent=2))
    raise SystemExit(1 if failed else 0)


if __name__ == "__main__":
    main()
