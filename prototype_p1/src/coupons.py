"""Quick-print calibration and structural coupons required before P1 structural prints."""

import math

import cadquery as cq

from common import box_at, cylinder_axis
from parameters import v


def bearing_coupon(depth):
    diameters = (21.8, 22.0, 22.1, 22.2, 22.3, 22.4)
    block = box_at(0, 0, 0, 150, 34, depth + 4)
    for i, dia in enumerate(diameters):
        x = 14 + i * 24
        block = block.cut(cylinder_axis((x, 17, 4), dia / 2, depth + 0.1))
    return block


def round_hole_coupon(name):
    values = (8.0, 8.2, 8.4, 8.6) if name == "M8" else (6.0, 6.2, 6.4, 6.6)
    block = box_at(0, 0, 0, 72, 24, 8)
    for i, dia in enumerate(values):
        block = block.cut(cylinder_axis((12 + i * 16, 12, -0.1), dia / 2, 8.2))
    return block


def nut_trap_coupon():
    af_values = (10.0, 10.2, 10.4, 10.6)
    block = box_at(0, 0, 0, 80, 26, 8)
    for i, af in enumerate(af_values):
        circ = af / math.cos(math.radians(30))
        cut = cq.Workplane("XY", origin=(13 + i * 18, 13, 3)).polygon(6, circ).extrude(5.1)
        block = block.cut(cut)
    return block


def magnet_coupon():
    sx, sz, sy = v("magnet_size")
    block = box_at(0, 0, 0, 70, 22, sy + 4)
    for i, offset in enumerate((0.0, 0.1, 0.2, 0.3)):
        x = 5 + i * 17
        block = block.cut(box_at(x, 6, 4, sx + offset, sz + offset, sy + offset + 0.1))
    return block


def hall_gap_jig():
    gaps = (3, 5, 8, 10, 12, 15)
    jig = None
    x = 0.0
    for gap in gaps:
        # Two opposing tabs define each exact air gap; common spine keeps one print.
        frame = box_at(x, 0, 0, 14, 5, 18)
        frame = frame.union(box_at(x, 0, 0, 5, 20 + gap, 4))
        frame = frame.union(box_at(x + 9, 0, 0, 5, 20 + gap, 4))
        frame = frame.union(box_at(x, 0, 14, 5, 20 + gap, 4))
        frame = frame.union(box_at(x + 9, 0, 14, 5, 20 + gap, 4))
        jig = frame if jig is None else jig.union(frame)
        x += 18
    return jig.union(box_at(0, 0, 0, 104, 5, 4))


def loaded_bearing_wall_coupon():
    # Represents the P1 hub radial wall and a bolt-loaded lug for proof testing.
    body = cylinder_axis((25, 0, 25), v("hub_radius"), 20, (0, 1, 0))
    body = body.cut(cylinder_axis((25, -0.1, 25), v("bearing_pocket") / 2, 7.2, (0, 1, 0)))
    body = body.cut(cylinder_axis((25, -0.1, 25), v("pivot_clearance") / 2, 20.2, (0, 1, 0)))
    lug = box_at(45, 0, 17, 35, 20, 16)
    lug = lug.cut(cylinder_axis((68, -0.1, 25), 3.3, 20.2, (0, 1, 0)))
    return body.union(lug)


def parts():
    return {
        "COUPON_608_POCKETS_DEPTH_7": bearing_coupon(7.0),
        "COUPON_608_POCKETS_DEPTH_14": bearing_coupon(14.0),
        "COUPON_M8_CLEARANCE": round_hole_coupon("M8"),
        "COUPON_M6_CLEARANCE": round_hole_coupon("M6"),
        "COUPON_M6_NUT_TRAPS": nut_trap_coupon(),
        "COUPON_MAGNET_POCKETS": magnet_coupon(),
        "COUPON_HALL_GAP_JIG": hall_gap_jig(),
        "COUPON_LOADED_BEARING_WALL": loaded_bearing_wall_coupon(),
    }
