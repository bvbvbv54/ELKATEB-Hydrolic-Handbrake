"""P1-010 moving magnet holder and P1-011 adjustable stationary Hall mount."""

import math

from common import box_at, cylinder_axis, rotate_about_pivot, slot_cut_xy, translate
from lever_hub import place_rotating
from parameters import v


MAGNET_LOCAL_ANGLE = -105.0


def magnet_center_local():
    a = math.radians(MAGNET_LOCAL_ANGLE)
    return (v("magnet_radius") * math.cos(a), 0.0, v("magnet_radius") * math.sin(a))


def magnet_holder_local():
    mx, _, mz = magnet_center_local()
    # Plate contacts the rotating hub face at y=+14; the pocket opens outward.
    holder = box_at(mx - 8.0, 14.0, mz - 6.0, 16.0, 8.0, 12.0)
    # The arm stays inside the 2 mm axial support gap; only the cup steps
    # outward after it is radially clear of the pivot tower.
    arm = rotate_about_pivot(box_at(18.0, 10.0, -5.0, 41.0, 4.0, 10.0), MAGNET_LOCAL_ANGLE)
    holder = holder.union(arm)
    magnet_x, magnet_z, magnet_y = v("magnet_size")
    pocket = box_at(mx - magnet_x / 2 - 0.15, 18.7, mz - magnet_z / 2 - 0.15,
                    magnet_x + 0.3, magnet_y + 0.3, magnet_z + 0.3)
    holder = holder.cut(pocket)
    # Two M3 attachment bores plus a transverse M3 keeper screw across the pocket.
    for angle in (MAGNET_LOCAL_ANGLE - 10.0, MAGNET_LOCAL_ANGLE + 10.0):
        a = math.radians(angle)
        hx, hz = 21.0 * math.cos(a), 21.0 * math.sin(a)
        holder = holder.cut(cylinder_axis((hx, 9.9, hz), 1.7, 4.2, (0, 1, 0)))
    holder = holder.cut(cylinder_axis((mx - 8.1, 20.5, mz), 1.7, 16.2, (1, 0, 0)))
    return holder


def magnet_holder_at(angle_deg):
    return place_rotating(magnet_holder_local(), angle_deg)


def magnet_solid_at(angle_deg):
    mx, _, mz = magnet_center_local()
    sx, sz, sy = v("magnet_size")
    magnet = box_at(mx - sx / 2, 18.8, mz - sz / 2, sx, sy, sz)
    return place_rotating(magnet, angle_deg)


def fixed_bracket():
    # Outer mounting plate plus two inboard rails. Slots are along Y and allow
    # the separate sensor sled to clamp at any 3-15 mm test gap.
    plate = box_at(58, 76, 10, 20, 4, 24)
    lower = box_at(75, 65, 17, 14, 15, 3)
    upper = box_at(75, 65, 42, 14, 15, 3)
    outer_bridge = box_at(75, 76, 17, 14, 4, 28)
    bracket = plate.union(lower).union(upper).union(outer_bridge)
    for x, z in ((66, 18), (66, 26)):
        bracket = bracket.cut(cylinder_axis((x, 75.9, z), 2.25, 4.2, (0, 1, 0)))
    # Clamp slots through the rails: 14 mm long along Y.
    for x, z0 in ((78, 16.9), (86, 16.9), (78, 41.9), (86, 41.9)):
        cut = box_at(x - 1.7, 66, z0, 3.4, 11, 3.2)
        cut = cut.union(cylinder_axis((x, 66, z0), 1.7, 3.2))
        cut = cut.union(cylinder_axis((x, 77, z0), 1.7, 3.2))
        bracket = bracket.cut(cut)
    return bracket


def sensor_sled(gap=None):
    if gap is None:
        gap = v("hall_nominal_gap")
    # Nominal magnet outer face is y=64.0; board sensing face is offset by gap.
    face_y = 64.0 + gap
    sled = box_at(75, face_y + 1.6, 21, 14, 3, 20)
    sled = sled.union(box_at(75, 65, 20, 14, face_y + 4.6 - 65, 3))
    sled = sled.union(box_at(75, 65, 39, 14, face_y + 4.6 - 65, 3))
    # PCB mounting and rail clamp holes.
    for x in (78, 86):
        sled = sled.cut(cylinder_axis((x, face_y + 1.5, 31), 1.25, 3.2, (0, 1, 0)))
        for z in (20, 39):
            sled = sled.cut(cylinder_axis((x, 64.9, z), 1.7, face_y + 4.8 - 65, (0, 1, 0)))
    return sled


def sensor_pcb(gap=None):
    if gap is None:
        gap = v("hall_nominal_gap")
    # Board is vertical: 10 mm in X and 20 mm in Z, centred on the full-pull magnet.
    return box_at(77, 64.0 + gap, 21, 10, 1.6, 20)


def parts():
    return {
        "P1-010_MAGNET_HOLDER": magnet_holder_local(),
        "P1-011A_HALL_FIXED_BRACKET": fixed_bracket(),
        "P1-011B_HALL_SENSOR_SLED": sensor_sled(),
    }
