"""Shared CadQuery utilities for P1-C."""

from pathlib import Path
import json
import math
import cadquery as cq

ROOT = Path(__file__).resolve().parents[1]


def shape(obj):
    return obj.val() if isinstance(obj, cq.Workplane) else obj


def wp(obj):
    return obj if isinstance(obj, cq.Workplane) else cq.Workplane(obj=shape(obj))


def box_at(x, y, z, dx, dy, dz):
    return cq.Workplane("XY", origin=(x, y, z)).box(dx, dy, dz, centered=(False, False, False))


def cyl(center, radius, length, direction=(0, 0, 1)):
    return cq.Workplane(obj=cq.Solid.makeCylinder(radius, length, cq.Vector(*center), cq.Vector(*direction)))


def prism_xz(points, y0, depth):
    return cq.Workplane("XZ", origin=(0, y0, 0)).polyline(points).close().extrude(-depth)


def rotate_y(obj, angle_deg, pivot=(0, 0, 0)):
    x, y, z = pivot
    return wp(obj).rotate((x, y, z), (x, y + 1, z), -angle_deg)


def slot_xy(cx, cy, z0, length, width, height):
    straight = length - width
    out = box_at(cx - straight / 2, cy - width / 2, z0, straight, width, height)
    out = out.union(cyl((cx - straight / 2, cy, z0), width / 2, height))
    return out.union(cyl((cx + straight / 2, cy, z0), width / 2, height))


def capsule_xz(p1, p2, radius, y0, depth):
    x1, z1 = p1; x2, z2 = p2
    dx, dz = x2 - x1, z2 - z1
    length = math.hypot(dx, dz)
    angle = math.degrees(math.atan2(dz, dx))
    local = box_at(0, y0, -radius, length, depth, 2 * radius)
    local = local.union(cyl((0, y0, 0), radius, depth, (0, 1, 0)))
    local = local.union(cyl((length, y0, 0), radius, depth, (0, 1, 0)))
    return rotate_y(local, angle).translate((x1, 0, z1))


def between(a, b, radius):
    av, bv = cq.Vector(*a), cq.Vector(*b)
    d = bv - av
    return cq.Workplane(obj=cq.Solid.makeCylinder(radius, d.Length, av, d.normalized()))


def validate(name, obj, material=""):
    s = shape(obj); bb = s.BoundingBox()
    return {"part_id": name, "material": material, "valid": bool(s.isValid()),
            "solids": len(s.Solids()), "volume_mm3": round(s.Volume(), 3),
            "bbox_x_mm": round(bb.xlen, 3), "bbox_y_mm": round(bb.ylen, 3), "bbox_z_mm": round(bb.zlen, 3)}


def overlap(a, b):
    try:
        return max(0.0, shape(a).intersect(shape(b)).Volume())
    except Exception:
        return math.nan


def save_json(path, data):
    Path(path).write_text(json.dumps(data, indent=2), encoding="utf-8")


COLORS = {
    "steel": cq.Color(0.045, 0.055, 0.065),
    "aluminium": cq.Color(0.68, 0.70, 0.72),
    "printed": cq.Color(0.10, 0.11, 0.13),
    "red": cq.Color(0.55, 0.025, 0.035),
    "bearing": cq.Color(0.72, 0.74, 0.76),
    "rubber": cq.Color(0.018, 0.02, 0.023),
    "sensor": cq.Color(0.05, 0.45, 0.17),
    "magnet": cq.Color(0.80, 0.15, 0.08),
    "desk": cq.Color(0.47, 0.29, 0.14, 0.42),
}
