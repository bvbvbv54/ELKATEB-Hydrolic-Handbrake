"""P1-001 structural base and optional P1-030/P1-031 steel backing strips."""

import cadquery as cq

from common import box_at, cylinder_axis, slot_cut_xy
from parameters import v


SUPPORT_X = (32.0, 68.0)
SUPPORT_Y = (18.0, 66.0)
CLAMP_X = (125.0, 165.0)
RIG_SLOT_Y = (32.0, 52.0)


def build_base():
    base = box_at(0, 0, 0, v("base_length"), v("base_width"), v("base_thickness"))

    # Recesses let two 3 mm steel strips sit flush with the underside.
    for yc in SUPPORT_Y:
        recess = box_at(2, yc - 12.7, -0.1, 176, 25.4, 3.3)
        base = base.cut(recess)

    # Pivot-tower and clamp loads go through printed base and steel strips.
    for x in SUPPORT_X + CLAMP_X:
        for y in SUPPORT_Y:
            base = base.cut(cylinder_axis((x, y, -0.1), v("structural_clearance_m6") / 2, 10.2))

    # Spring anchor through-holes with underside washer access.
    for x in (96.0, 120.0):
        base = base.cut(cylinder_axis((x, 42.0, -0.1), v("structural_clearance_m6") / 2, 10.2))

    # Independent rig slots do not intersect clamp/backing-strip fasteners.
    for y in RIG_SLOT_Y:
        base = base.cut(slot_cut_xy(136.0, y, -0.1, v("rig_slot_length"), v("rig_slot_width"), 10.2))

    # Light-duty electronics and Hall-bracket mounting holes.
    for x, y in ((136, 51), (170, 51), (136, 78), (170, 78), (84, 78), (94, 78)):
        base = base.cut(cylinder_axis((x, y, -0.1), v("light_clearance_m4") / 2, 10.2))
    return base


def build_backing_strip(y_center, part_id):
    strip = box_at(0, y_center - 12.5, 0, 180, 25, 3)
    for x in SUPPORT_X + CLAMP_X:
        strip = strip.cut(cylinder_axis((x, y_center, -0.1), 3.3, 3.2))
    return strip


def parts():
    return {
        "P1-001_BASE": build_base(),
        "P1-030_LEFT_BACKING_STRIP": build_backing_strip(18.0, "P1-030"),
        "P1-031_RIGHT_BACKING_STRIP": build_backing_strip(66.0, "P1-031"),
    }
