"""Shared CadQuery helpers and export/validation utilities."""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Iterable

import cadquery as cq


ROOT = Path(__file__).resolve().parents[1]


def as_shape(obj):
    if isinstance(obj, cq.Workplane):
        return obj.val()
    return obj


def wp(obj):
    return obj if isinstance(obj, cq.Workplane) else cq.Workplane(obj=as_shape(obj))


def box_at(x, y, z, dx, dy, dz):
    return cq.Workplane("XY", origin=(x, y, z)).box(dx, dy, dz, centered=(False, False, False))


def cylinder_between(start, end, radius):
    a = cq.Vector(*start)
    b = cq.Vector(*end)
    d = b - a
    return cq.Workplane(obj=cq.Solid.makeCylinder(radius, d.Length, a, d.normalized()))


def cylinder_axis(center, radius, length, direction=(0, 0, 1), start_offset=0.0):
    p = cq.Vector(*center) + cq.Vector(*direction).normalized() * start_offset
    return cq.Workplane(obj=cq.Solid.makeCylinder(radius, length, p, cq.Vector(*direction)))


def prism_xz(points: Iterable[tuple[float, float]], y0: float, depth: float):
    # CadQuery's XZ plane has its positive normal along -Y, hence negative
    # extrusion advances from y0 toward +Y.
    return cq.Workplane("XZ", origin=(0, y0, 0)).polyline(list(points)).close().extrude(-depth)


def prism_xy(points: Iterable[tuple[float, float]], z0: float, depth: float):
    return cq.Workplane("XY", origin=(0, 0, z0)).polyline(list(points)).close().extrude(depth)


def rotate_about_pivot(obj, angle_deg, pivot=(0, 0, 0)):
    """Rotate +X toward +Z by angle_deg (negative RH rotation about +Y)."""
    x, y, z = pivot
    return wp(obj).rotate((x, y, z), (x, y + 1, z), -angle_deg)


def translate(obj, vec):
    return wp(obj).translate(vec)


def slot_cut_xy(center_x, center_y, z0, length, width, height):
    straight = max(0.0, length - width)
    mid = box_at(center_x - straight / 2, center_y - width / 2, z0, straight, width, height)
    left = cylinder_axis((center_x - straight / 2, center_y, z0), width / 2, height)
    right = cylinder_axis((center_x + straight / 2, center_y, z0), width / 2, height)
    return mid.union(left).union(right)


def validate_shape(name, obj):
    shape = as_shape(obj)
    bb = shape.BoundingBox()
    return {
        "name": name,
        "valid": bool(shape.isValid()),
        "solids": len(shape.Solids()),
        "volume_mm3": round(shape.Volume(), 3),
        "bbox_mm": {
            "xmin": round(bb.xmin, 3), "xmax": round(bb.xmax, 3), "xlen": round(bb.xlen, 3),
            "ymin": round(bb.ymin, 3), "ymax": round(bb.ymax, 3), "ylen": round(bb.ylen, 3),
            "zmin": round(bb.zmin, 3), "zmax": round(bb.zmax, 3), "zlen": round(bb.zlen, 3),
        },
    }


def export_part(name, obj, printable=True):
    shape = as_shape(obj)
    step_path = ROOT / "step" / f"{name}.step"
    cq.exporters.export(shape, str(step_path))
    if printable:
        stl_path = ROOT / "stl" / f"{name}.stl"
        cq.exporters.export(shape, str(stl_path), tolerance=0.08, angularTolerance=0.15)
    return validate_shape(name, shape)


def overlap_volume(a, b):
    try:
        common = as_shape(a).intersect(as_shape(b))
        return max(0.0, common.Volume())
    except Exception:
        return math.nan


def save_json(path, data):
    Path(path).write_text(json.dumps(data, indent=2), encoding="utf-8")


COLORS = {
    "printed": cq.Color(0.12, 0.35, 0.58),
    "printed_alt": cq.Color(0.12, 0.52, 0.42),
    "steel": cq.Color(0.58, 0.62, 0.66),
    "bearing": cq.Color(0.76, 0.77, 0.78),
    "rubber": cq.Color(0.08, 0.08, 0.09),
    "sensor": cq.Color(0.10, 0.52, 0.18),
    "magnet": cq.Color(0.72, 0.18, 0.13),
    "spring": cq.Color(0.86, 0.68, 0.16),
    "desk": cq.Color(0.58, 0.36, 0.18, 0.45),
}
