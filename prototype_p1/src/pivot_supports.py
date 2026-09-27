"""P1-002/P1-003 two-sided pivot towers."""

import math

from common import cylinder_axis, prism_xz
from parameters import v
from stops import mount_centres


PROFILE = [(22, 10), (78, 10), (72, 24), (64, 54), (62, 76), (38, 76), (36, 54), (28, 24)]


def _support(y0, left=False):
    body = prism_xz(PROFILE, y0, v("support_thickness"))
    boss = cylinder_axis((v("pivot_x"), y0, v("pivot_z")), 27.0, v("support_thickness"), (0, 1, 0))
    body = body.union(boss)
    # M8 pivot clearance.
    body = body.cut(cylinder_axis((v("pivot_x"), y0 - 0.1, v("pivot_z")), v("pivot_clearance") / 2, v("support_thickness") + 0.2, (0, 1, 0)))
    # Foot through-bolts.
    yc = y0 + v("support_thickness") / 2
    for x in (32.0, 68.0):
        body = body.cut(cylinder_axis((x, yc, 9.9), v("structural_clearance_m6") / 2, 14.0))
    if left:
        # Curved clearance for the M6 steel travel-stop pin; eight overlapping cuts.
        for deg in range(-46, -8, 5):
            a = math.radians(deg)
            x = v("pivot_x") + v("stop_pin_radius") * math.cos(a)
            z = v("pivot_z") + v("stop_pin_radius") * math.sin(a)
            body = body.cut(cylinder_axis((x, y0 - 0.1, z), 4.1, v("support_thickness") + 0.2, (0, 1, 0)))
        # Through-bolt holes for both replaceable stop blocks.
        pairs = (
            mount_centres(v("lever_released_angle"), True),
            mount_centres(v("lever_full_angle"), False),
        )
        for pair in pairs:
            for x, z in pair:
                body = body.cut(cylinder_axis((x, y0 - 0.1, z), 2.25, v("support_thickness") + 0.2, (0, 1, 0)))
    else:
        # Hall fixed-bracket through-bolts; no heat-set insert carries sensor load.
        for x, z in ((66.0, 18.0), (66.0, 26.0)):
            body = body.cut(cylinder_axis((x, y0 - 0.1, z), 2.25, v("support_thickness") + 0.2, (0, 1, 0)))
    return body


def parts():
    return {
        "P1-002_LEFT_PIVOT_SUPPORT": _support(8.0, left=True),
        "P1-003_RIGHT_PIVOT_SUPPORT": _support(58.0, left=False),
    }
