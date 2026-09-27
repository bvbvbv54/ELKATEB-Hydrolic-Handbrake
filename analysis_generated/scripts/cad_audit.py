#!/usr/bin/env python3
"""Read-only CAD/mesh inventory and geometry audit.

All outputs are written below analysis_generated/. Source files are only opened.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import re
import sys
import zipfile
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "analysis_generated"
PKGS = OUT / "python_packages"
if str(PKGS) not in sys.path:
    sys.path.insert(0, str(PKGS))

CAD_EXTS = {
    ".step", ".stp", ".stl", ".obj", ".sldprt", ".sldasm", ".slddrw",
    ".iges", ".igs", ".x_t", ".f3d", ".dxf", ".dwg", ".3mf", ".fcstd",
}
DOC_EXTS = {".pdf", ".md", ".txt", ".rtf", ".csv", ".xlsx", ".xls", ".json", ".xml"}
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".bmp", ".webp"}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def project_dirs() -> list[Path]:
    return sorted(p for p in ROOT.iterdir() if p.is_dir() and ".snapshot." in p.name)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def classify_file(path: Path) -> str:
    ext = path.suffix.lower()
    name = path.name.lower()
    if ext in CAD_EXTS:
        return "CAD"
    if ext in IMAGE_EXTS:
        return "image/render"
    if ext in DOC_EXTS or any(k in name for k in ("readme", "license", "copying", "bom", "hardware")):
        return "documentation/data"
    if ext == ".zip":
        return "archive"
    return "other"


def make_inventory() -> list[dict]:
    rows: list[dict] = []
    for project in project_dirs():
        for path in sorted(p for p in project.rglob("*") if p.is_file()):
            rows.append({
                "project": project.name,
                "relative_path": rel(path),
                "filename": path.name,
                "extension": path.suffix.lower() or "[none]",
                "category": classify_file(path),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            })
    out = OUT / "model_inventory.csv"
    with out.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    return rows


def zip_listing(path: Path) -> dict:
    try:
        with zipfile.ZipFile(path) as zf:
            return {
                "valid_zip": True,
                "members": [
                    {"name": i.filename, "bytes": i.file_size, "compressed_bytes": i.compress_size}
                    for i in zf.infolist()
                ],
            }
    except Exception as exc:
        return {"valid_zip": False, "error": repr(exc)}


def neutral_header(path: Path) -> dict:
    text = path.read_text(encoding="latin-1", errors="replace")
    head = text[:120000]
    data: dict = {}
    if path.suffix.lower() in {".step", ".stp"}:
        m = re.search(r"FILE_NAME\s*\((.*?)\);", head, re.I | re.S)
        if m:
            data["file_name_record"] = re.sub(r"\s+", " ", m.group(1)).strip()
        m = re.search(r"FILE_SCHEMA\s*\((.*?)\);", head, re.I | re.S)
        if m:
            data["schema"] = re.sub(r"\s+", " ", m.group(1)).strip()
        data["unit_tokens"] = sorted(set(re.findall(
            r"(?:SI_UNIT|CONVERSION_BASED_UNIT)\s*\([^;]{0,160}", text, re.I
        )))[:30]
        data["products"] = re.findall(r"PRODUCT\s*\(\s*'([^']*)'\s*,\s*'([^']*)'", text, re.I)[:200]
        data["application_contexts"] = sorted(set(re.findall(r"APPLICATION_CONTEXT\s*\(\s*'([^']*)'", text, re.I)))
    elif path.suffix.lower() in {".igs", ".iges"}:
        data["header_excerpt"] = head[:5000]
    return data


def count_topology(shape) -> dict:
    from OCP.TopAbs import (
        TopAbs_VERTEX, TopAbs_EDGE, TopAbs_WIRE, TopAbs_FACE, TopAbs_SHELL,
        TopAbs_SOLID, TopAbs_COMPSOLID, TopAbs_COMPOUND,
    )
    from OCP.TopExp import TopExp_Explorer

    kinds = {
        "vertices": TopAbs_VERTEX, "edges": TopAbs_EDGE, "wires": TopAbs_WIRE,
        "faces": TopAbs_FACE, "shells": TopAbs_SHELL, "solids": TopAbs_SOLID,
        "compsolids": TopAbs_COMPSOLID, "compounds": TopAbs_COMPOUND,
    }
    result = {}
    for name, kind in kinds.items():
        exp, n = TopExp_Explorer(shape, kind), 0
        while exp.More():
            n += 1
            exp.Next()
        result[name] = n
    return result


def shape_bbox(shape) -> list[float]:
    from OCP.Bnd import Bnd_Box
    from OCP.BRepBndLib import BRepBndLib

    box = Bnd_Box()
    BRepBndLib.Add_s(shape, box, True)
    x0, y0, z0, x1, y1, z1 = box.Get()
    return [float(x0), float(y0), float(z0), float(x1), float(y1), float(z1)]


def shape_props(shape) -> dict:
    from OCP.BRepCheck import BRepCheck_Analyzer
    from OCP.BRepGProp import BRepGProp
    from OCP.GProp import GProp_GProps

    vol = GProp_GProps()
    area = GProp_GProps()
    BRepGProp.VolumeProperties_s(shape, vol)
    BRepGProp.SurfaceProperties_s(shape, area)
    c = vol.CentreOfMass()
    return {
        "valid_brep": bool(BRepCheck_Analyzer(shape).IsValid()),
        "volume_mm3_assuming_kernel_mm": float(vol.Mass()),
        "surface_area_mm2_assuming_kernel_mm": float(area.Mass()),
        "center_of_mass": [float(c.X()), float(c.Y()), float(c.Z())],
    }


def cylindrical_faces(shape) -> list[dict]:
    from OCP.BRepAdaptor import BRepAdaptor_Surface
    from OCP.GeomAbs import GeomAbs_Cylinder
    from OCP.TopAbs import TopAbs_FACE
    from OCP.TopExp import TopExp_Explorer
    from OCP.TopoDS import TopoDS

    found = []
    exp = TopExp_Explorer(shape, TopAbs_FACE)
    while exp.More():
        face = TopoDS.Face_s(exp.Current())
        surf = BRepAdaptor_Surface(face, True)
        if surf.GetType() == GeomAbs_Cylinder:
            cyl = surf.Cylinder()
            ax = cyl.Axis()
            loc, direction = ax.Location(), ax.Direction()
            found.append({
                "radius_mm_assuming_kernel_mm": float(cyl.Radius()),
                "diameter_mm_assuming_kernel_mm": float(2 * cyl.Radius()),
                "axis_location": [float(loc.X()), float(loc.Y()), float(loc.Z())],
                "axis_direction": [float(direction.X()), float(direction.Y()), float(direction.Z())],
            })
        exp.Next()
    return found


def solid_records(shape) -> list[dict]:
    from OCP.TopAbs import TopAbs_SOLID
    from OCP.TopExp import TopExp_Explorer
    from OCP.TopoDS import TopoDS

    out = []
    exp = TopExp_Explorer(shape, TopAbs_SOLID)
    i = 0
    while exp.More():
        i += 1
        solid = TopoDS.Solid_s(exp.Current())
        bb = shape_bbox(solid)
        rec = {"solid_index": i, "bbox": bb, "extents": [bb[3]-bb[0], bb[4]-bb[1], bb[5]-bb[2]]}
        rec.update(shape_props(solid))
        out.append(rec)
        exp.Next()
    return out


def load_neutral(path: Path):
    ext = path.suffix.lower()
    if ext in {".step", ".stp"}:
        from OCP.STEPControl import STEPControl_Reader
        reader = STEPControl_Reader()
    elif ext in {".iges", ".igs"}:
        from OCP.IGESControl import IGESControl_Reader
        reader = IGESControl_Reader()
    else:
        raise ValueError(ext)
    status = reader.ReadFile(str(path))
    transferred = reader.TransferRoots()
    return reader.OneShape(), int(status), int(transferred)


def xcaf_name(label) -> str | None:
    from OCP.TDataStd import TDataStd_Name

    attr = TDataStd_Name()
    if label.FindAttribute(TDataStd_Name.GetID_s(), attr):
        return attr.Get().ToExtString()
    return None


def xcaf_step_occurrences(path: Path) -> dict:
    """Read STEP product/occurrence names and located shapes through XCAF."""
    from OCP.STEPCAFControl import STEPCAFControl_Reader
    from OCP.TCollection import TCollection_ExtendedString
    from OCP.TDF import TDF_Label, TDF_LabelSequence
    from OCP.TDocStd import TDocStd_Document
    from OCP.XCAFDoc import XCAFDoc_DocumentTool, XCAFDoc_ShapeTool

    doc = TDocStd_Document(TCollection_ExtendedString("cad-audit"))
    reader = STEPCAFControl_Reader()
    reader.SetNameMode(True)
    status = reader.ReadFile(str(path))
    transferred = reader.Transfer(doc)
    tool = XCAFDoc_DocumentTool.ShapeTool_s(doc.Main())
    free = TDF_LabelSequence()
    tool.GetFreeShapes(free)
    roots = []
    occurrences = []
    for i in range(1, free.Length() + 1):
        root = free.Value(i)
        roots.append({
            "name": xcaf_name(root),
            "is_assembly": bool(XCAFDoc_ShapeTool.IsAssembly_s(root)),
            "component_count": int(XCAFDoc_ShapeTool.NbComponents_s(root)),
        })
        comps = TDF_LabelSequence()
        if XCAFDoc_ShapeTool.GetComponents_s(root, comps, False):
            for j in range(1, comps.Length() + 1):
                comp = comps.Value(j)
                referred = TDF_Label()
                has_ref = XCAFDoc_ShapeTool.GetReferredShape_s(comp, referred)
                shape = XCAFDoc_ShapeTool.GetShape_s(comp)
                bb = shape_bbox(shape)
                rec = {
                    "occurrence_index": j,
                    "occurrence_name": xcaf_name(comp),
                    "referred_name": xcaf_name(referred) if has_ref else None,
                    "bbox": bb,
                    "extents": [bb[3]-bb[0], bb[4]-bb[1], bb[5]-bb[2]],
                    "topology": count_topology(shape),
                    "cylindrical_faces": cylindrical_faces(shape),
                }
                rec.update(shape_props(shape))
                occurrences.append(rec)
    return {
        "read_status": str(status),
        "transfer_ok": bool(transferred),
        "free_shape_count": int(free.Length()),
        "roots": roots,
        "occurrences": occurrences,
    }


def analyze_neutral(path: Path) -> dict:
    try:
        shape, status, transferred = load_neutral(path)
        bb = shape_bbox(shape)
        cyls = cylindrical_faces(shape)
        diameter_counts = Counter(round(c["diameter_mm_assuming_kernel_mm"], 4) for c in cyls)
        record = {
            "path": rel(path),
            "format": path.suffix.lower(),
            "reader_status": status,
            "roots_transferred": transferred,
            "header": neutral_header(path),
            "bbox": bb,
            "extents": [bb[3]-bb[0], bb[4]-bb[1], bb[5]-bb[2]],
            "topology": count_topology(shape),
            "properties": shape_props(shape),
            "cylindrical_face_diameter_counts": [
                {"diameter": d, "face_count": n} for d, n in sorted(diameter_counts.items())
            ],
            "cylindrical_faces": cyls,
            "solids": solid_records(shape),
        }
        if path.suffix.lower() in {".step", ".stp"}:
            record["xcaf"] = xcaf_step_occurrences(path)
        return record
    except Exception as exc:
        return {"path": rel(path), "format": path.suffix.lower(), "error": repr(exc)}


def analyze_stl(path: Path) -> dict:
    import numpy as np
    import trimesh

    try:
        loaded = trimesh.load(path, force="scene", process=False)
        if isinstance(loaded, trimesh.Scene):
            geometries = list(loaded.geometry.values())
            mesh = trimesh.util.concatenate(tuple(g.copy() for g in geometries)) if geometries else None
        else:
            geometries, mesh = [loaded], loaded
        if mesh is None:
            raise ValueError("no mesh geometry")
        areas = mesh.area_faces
        degenerate = int(np.count_nonzero(areas < 1e-12))
        unique_count = int(mesh.unique_faces().sum())
        # Binary STL commonly repeats all three vertices per facet.  Validate a
        # welded/processed copy as well as reporting the untouched raw counts.
        checked = mesh.copy()
        checked.process(validate=True)
        components = checked.split(only_watertight=False)
        bounds = mesh.bounds.astype(float).tolist()
        extents = mesh.extents.astype(float).tolist()
        return {
            "path": rel(path),
            "format": ".stl",
            "unit_metadata": "STL has no intrinsic units; numeric coordinates reported as file units",
            "geometry_count": len(geometries),
            "raw_vertices": int(len(mesh.vertices)),
            "raw_faces": int(len(mesh.faces)),
            "validated_vertices_after_weld": int(len(checked.vertices)),
            "validated_faces": int(len(checked.faces)),
            "connected_components": int(len(components)),
            "watertight": bool(checked.is_watertight),
            "winding_consistent": bool(checked.is_winding_consistent),
            "is_volume": bool(checked.is_volume),
            "euler_number": int(checked.euler_number),
            "degenerate_faces_area_lt_1e-12": degenerate,
            "duplicate_faces": int(len(mesh.faces) - unique_count),
            "bounds_file_units": bounds,
            "extents_file_units": extents,
            "surface_area_file_units2": float(checked.area),
            "signed_volume_file_units3": float(checked.volume),
            "component_extents_file_units": [c.extents.astype(float).tolist() for c in components[:100]],
        }
    except Exception as exc:
        return {"path": rel(path), "format": ".stl", "error": repr(exc)}


DXF_UNITS = {
    0: "unitless", 1: "inch", 2: "foot", 3: "mile", 4: "mm", 5: "cm", 6: "m",
    7: "km", 8: "microinch", 9: "mil", 10: "yard", 11: "angstrom", 12: "nm",
    13: "micron", 14: "dm", 15: "dam", 16: "hm", 17: "Gm", 18: "AU",
}


def analyze_dxf(path: Path) -> dict:
    import ezdxf
    from ezdxf import bbox

    try:
        doc = ezdxf.readfile(path)
        msp = doc.modelspace()
        cache = bbox.Cache()
        ext = bbox.extents(msp, cache=cache)
        entities = Counter(e.dxftype() for e in msp)
        circles = []
        for e in msp.query("CIRCLE"):
            circles.append({
                "center": [float(e.dxf.center.x), float(e.dxf.center.y), float(e.dxf.center.z)],
                "radius": float(e.dxf.radius), "diameter": float(2 * e.dxf.radius),
            })
        arcs = []
        for e in msp.query("ARC"):
            arcs.append({
                "center": [float(e.dxf.center.x), float(e.dxf.center.y), float(e.dxf.center.z)],
                "radius": float(e.dxf.radius),
                "start_angle_deg": float(e.dxf.start_angle),
                "end_angle_deg": float(e.dxf.end_angle),
            })
        ins = int(doc.header.get("$INSUNITS", 0))
        return {
            "path": rel(path), "format": ".dxf", "dxf_version": doc.dxfversion,
            "insunits_code": ins, "units": DXF_UNITS.get(ins, f"unknown-code-{ins}"),
            "entity_counts": dict(entities),
            "bbox": [float(ext.extmin.x), float(ext.extmin.y), float(ext.extmin.z),
                     float(ext.extmax.x), float(ext.extmax.y), float(ext.extmax.z)],
            "extents": [float(ext.size.x), float(ext.size.y), float(ext.size.z)],
            "circles": circles,
            "arcs": arcs,
        }
    except Exception as exc:
        return {"path": rel(path), "format": ".dxf", "error": repr(exc)}


def extract_ole_metadata(path: Path) -> dict:
    import olefile

    data = {"path": rel(path), "format": path.suffix.lower(), "geometry_parsed": False}
    try:
        if not olefile.isOleFile(path):
            data["ole_container"] = False
            return data
        data["ole_container"] = True
        with olefile.OleFileIO(path) as ole:
            data["streams"] = ["/".join(s) for s in ole.listdir()]
            for stream_name in ("\x05SummaryInformation", "\x05DocumentSummaryInformation"):
                if ole.exists(stream_name):
                    try:
                        data[stream_name.encode("unicode_escape").decode()] = {
                            str(k): str(v) for k, v in ole.getproperties(stream_name).items()
                        }
                    except Exception as exc:
                        data[stream_name + "_error"] = repr(exc)
    except Exception as exc:
        data["error"] = repr(exc)
    return data


def analyze_all() -> dict:
    results: dict = {
        "methodology": {
            "neutral_cad": "OpenCascade 7.9.3.1 B-Rep import; kernel coordinates reported in mm after STEP/IGES unit conversion",
            "stl": "trimesh 4.11.5 with process=False; coordinates remain unitless until cross-validation",
            "dxf": "ezdxf 1.4.4; $INSUNITS reported explicitly",
            "solidworks": "OLE container metadata only; proprietary B-Rep not parsed",
        },
        "projects": {},
    }
    for project in project_dirs():
        pdata = {"files": []}
        for path in sorted(p for p in project.rglob("*") if p.is_file()):
            ext = path.suffix.lower()
            if ext in {".step", ".stp", ".iges", ".igs"}:
                record = analyze_neutral(path)
            elif ext == ".stl":
                record = analyze_stl(path)
            elif ext == ".dxf":
                record = analyze_dxf(path)
            elif ext in {".sldprt", ".sldasm", ".slddrw"}:
                record = extract_ole_metadata(path)
            elif ext in {".zip", ".f3d"}:
                record = {"path": rel(path), "format": ext, **zip_listing(path)}
            else:
                continue
            pdata["files"].append(record)
        results["projects"][project.name] = pdata
    out = OUT / "geometry_findings.json"
    out.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    return results


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inventory-only", action="store_true")
    args = parser.parse_args()
    OUT.mkdir(exist_ok=True)
    rows = make_inventory()
    print(f"Inventory: {len(rows)} files")
    if not args.inventory_only:
        data = analyze_all()
        print(f"Geometry projects: {len(data['projects'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
