"""P1-004 replaceable dual-608 lever hub and P1-005 steel lever model."""

import cadquery as cq

from common import box_at, cylinder_axis, rotate_about_pivot, translate
from parameters import v


def hub_local():
    # Axis is global/local Y; hub faces are at y +/-14.
    hub = cylinder_axis((0, -v("hub_width") / 2, 0), v("hub_radius"), v("hub_width"), (0, 1, 0))
    clamp = box_at(10, -14, -18, 66, 28, 36)
    spring_lug = box_at(-48, -10, -10, 32, 20, 20)
    stop_lug = box_at(-8, -14, -40, 16, 20, 25)
    hub = hub.union(clamp).union(spring_lug).union(stop_lug)

    # Steel bar slot and two structural M6 clamp bolts.
    hub = hub.cut(box_at(18, -2.8, -12.8, 61, 5.6, 25.6))
    for x in (36.0, 60.0):
        hub = hub.cut(cylinder_axis((x, -14.1, 0), 3.3, 28.2, (0, 1, 0)))

    # Two independently replaceable 608 pockets and continuous M8 bore.
    hub = hub.cut(cylinder_axis((0, -14.1, 0), v("bearing_pocket") / 2, v("bearing_pocket_depth") + 0.1, (0, 1, 0)))
    hub = hub.cut(cylinder_axis((0, 14.1, 0), v("bearing_pocket") / 2, v("bearing_pocket_depth") + 0.1, (0, -1, 0)))
    hub = hub.cut(cylinder_axis((0, -14.1, 0), v("pivot_clearance") / 2, 28.2, (0, 1, 0)))

    # Steel moving spring anchor and travel-stop pin bores.
    hub = hub.cut(cylinder_axis((-v("moving_anchor_radius"), -10.1, 0), 3.3, 20.2, (0, 1, 0)))
    hub = hub.cut(cylinder_axis((0, -14.1, -v("stop_pin_radius")), 3.3, 20.2, (0, 1, 0)))
    return hub


def lever_local():
    bar = box_at(v("lever_bar_root_radius"), -v("lever_bar_thickness") / 2, -v("lever_bar_width") / 2,
                 v("lever_bar_length"), v("lever_bar_thickness"), v("lever_bar_width"))
    for x, dia in ((36.0, 6.6), (60.0, 6.6), (210.0, 4.5)):
        bar = bar.cut(cylinder_axis((x, -3.0, 0), dia / 2, 6.0, (0, 1, 0)))
    return bar


def place_rotating(obj, angle_deg):
    moved = rotate_about_pivot(obj, angle_deg)
    return translate(moved, (v("pivot_x"), v("pivot_y"), v("pivot_z")))


def hub_at(angle_deg):
    return place_rotating(hub_local(), angle_deg)


def lever_at(angle_deg):
    return place_rotating(lever_local(), angle_deg)


def parts():
    return {
        "P1-004_LEVER_ROOT_BEARING_HUB": hub_local(),
        "P1-005_STEEL_LEVER_TEMPLATE": lever_local(),
    }
