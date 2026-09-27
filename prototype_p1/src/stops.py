"""P1-008/P1-009 adjustable hard-stop blocks and steel stop hardware."""

import math

from common import box_at, cylinder_axis, rotate_about_pivot, translate
from parameters import v


def pin_point(angle_deg):
    # Stop pin is 90 degrees clockwise from the lever axis.
    a = math.radians(angle_deg - 90.0)
    return (
        v("pivot_x") + v("stop_pin_radius") * math.cos(a),
        v("pivot_y"),
        v("pivot_z") + v("stop_pin_radius") * math.sin(a),
    )


def _block(angle_deg, release):
    p = pin_point(angle_deg)
    # At release the block arrests increasing angle; at full pull it arrests
    # decreasing angle. The M6 screw axis is tangent to the pin arc.
    direction_deg = angle_deg if release else angle_deg - 180.0
    local = box_at(2.0, 0.0, -7.0, 20.0, 8.0, 14.0)
    local = local.cut(cylinder_axis((-0.1, 4.0, 0.0), 3.3, 22.2, (1, 0, 0)))
    for x in (9.0, 17.0):
        local = local.cut(cylinder_axis((x, -0.1, 0.0), 2.25, 8.2, (0, 1, 0)))
    oriented = rotate_about_pivot(local, direction_deg)
    return translate(oriented, (p[0], 0.0, p[2]))


def mount_centres(angle_deg, release):
    p = pin_point(angle_deg)
    direction_deg = angle_deg if release else angle_deg - 180.0
    a = math.radians(direction_deg)
    return [(p[0] + r * math.cos(a), p[2] + r * math.sin(a)) for r in (9.0, 17.0)]


def release_stop():
    return _block(v("lever_released_angle"), True)


def full_stop():
    return _block(v("lever_full_angle"), False)


def stop_pin(angle_deg):
    p = pin_point(angle_deg)
    # A through M6 bolt/pin crosses the hub and left support arc window.
    return cylinder_axis((p[0], 2.0, p[2]), 3.0, 40.0, (0, 1, 0))


def stop_screws():
    result = []
    for angle, release in ((v("lever_released_angle"), True), (v("lever_full_angle"), False)):
        p = pin_point(angle)
        d = angle if release else angle - 180.0
        # Start 3 mm from pin centre so the two M6 cylinders are tangent at
        # the commanded endpoint instead of occupying the same volume.
        local = cylinder_axis((3, 4, 0), 3.0, 15.0, (1, 0, 0))
        result.append(translate(rotate_about_pivot(local, d), (p[0], 0, p[2])))
    return result


def parts():
    return {
        "P1-008_RELEASE_STOP": release_stop(),
        "P1-009_FULL_PULL_STOP": full_stop(),
    }
