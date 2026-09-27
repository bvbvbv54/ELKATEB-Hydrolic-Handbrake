"""P1-007 fixed anchor and virtual extension-spring envelope."""

import math

from common import box_at, cylinder_axis, cylinder_between, prism_xz
from parameters import opposite_lever_point, v


def anchor_module():
    foot = box_at(88, 30, 10, 40, 24, 8)
    tower = box_at(100, 32, 18, 16, 20, 14)
    left_rib = prism_xz([(90, 18), (100, 18), (100, 31), (95, 25)], 32, 4)
    right_rib = prism_xz([(116, 18), (126, 18), (121, 25), (116, 31)], 48, 4)
    part = foot.union(tower).union(left_rib).union(right_rib)
    for x in (96.0, 120.0):
        part = part.cut(cylinder_axis((x, 42, 9.9), 3.3, 8.2))
    # Three future M6 cross-bolt positions; centre used for P1.0.
    for x in (104.0, 108.0, 112.0):
        part = part.cut(cylinder_axis((x, 31.9, v("fixed_anchor_z")), 3.3, 20.2, (0, 1, 0)))
    return part


def moving_anchor(angle_deg):
    return opposite_lever_point(v("moving_anchor_radius"), angle_deg)


def fixed_anchor():
    return (v("fixed_anchor_x"), v("pivot_y"), v("fixed_anchor_z"))


def spring_length(angle_deg):
    a = moving_anchor(angle_deg)
    b = fixed_anchor()
    return math.dist(a, b)


def spring_envelope(angle_deg):
    return cylinder_between(moving_anchor(angle_deg), fixed_anchor(), v("spring_envelope_diameter") / 2)


def parts():
    return {"P1-007_SPRING_ANCHOR_MODULE": anchor_module()}
