"""P1-020..P1-025 removable M10 steel-screw desk clamp."""

import cadquery as cq

from common import box_at, cylinder_axis, prism_xz
from parameters import v


SCREW_X = 112.0
SCREW_Y = 42.0
DESK_EDGE_X = 172.0
UPPER_CONTACT_Z = -11.0
NUT_Z0 = -116.0
NUT_Z1 = -86.0


def interface_plate():
    part = box_at(108, 6, -8, 64, 72, 8)
    for x in (125.0, 165.0):
        for y in (18.0, 66.0):
            part = part.cut(cylinder_axis((x, y, -8.1), 3.3, 8.2))
    # Horizontal bolts join the vertical bracket to the plate without overlap.
    for y in (20.0, 64.0):
        part = part.cut(cylinder_axis((160, y, -4), 3.3, 12.2, (1, 0, 0)))
    return part


def vertical_bracket():
    wall = box_at(172, 10, -122, 10, 64, 114)
    # Butt joints keep all three clamp prints non-overlapping; horizontal M6
    # through-bolts and washers carry the separable joints.
    for y in (20.0, 64.0):
        wall = wall.cut(cylinder_axis((167.9, y, -4), 3.3, 14.2, (1, 0, 0)))
    for y in (32.0, 52.0):
        wall = wall.cut(cylinder_axis((167.9, y, -114), 3.3, 14.2, (1, 0, 0)))
    # Two triangular ribs thicken the C-clamp corner without a monolithic shell.
    rib_profile = [(148, -122), (172, -122), (172, -88)]
    wall = wall.union(prism_xz(rib_profile, 12, 8)).union(prism_xz(rib_profile, 64, 8))
    return wall


def screw_guide():
    arm = box_at(96, 26, -122, 76, 32, 14)
    boss = cylinder_axis((SCREW_X, SCREW_Y, -122), 16.0, 38.0)
    part = arm.union(boss)
    # Captured M10 steel coupling nut; 19.8 mm circumscribed hex ~=17.15 AF.
    hex_cut = cq.Workplane("XY", origin=(SCREW_X, SCREW_Y, NUT_Z0)).polygon(6, 19.8).extrude(NUT_Z1 - NUT_Z0)
    part = part.cut(hex_cut)
    part = part.cut(cylinder_axis((SCREW_X, SCREW_Y, -122.1), 5.4, 38.2))
    for y in (32.0, 52.0):
        part = part.cut(cylinder_axis((167.9, y, -114), 3.3, 14.2, (1, 0, 0)))
    return part


def knob():
    z0 = 0.0
    knob = cylinder_axis((0, 0, z0), 17.0, 18.0)
    for i in range(6):
        a = i * 60.0
        x = 18.0 * __import__("math").cos(__import__("math").radians(a))
        y = 18.0 * __import__("math").sin(__import__("math").radians(a))
        knob = knob.union(cylinder_axis((x, y, z0), 8.0, 18.0))
    knob = knob.cut(cylinder_axis((0, 0, -0.1), 5.3, 18.2))
    head_pocket = cq.Workplane("XY", origin=(0, 0, 0)).polygon(6, 19.8).extrude(7.0)
    return knob.cut(head_pocket)


def swivel_pad_holder():
    # Printed carrier for a commodity M10 swivel foot/rounded-head assembly.
    pad = cylinder_axis((0, 0, 0), v("clamp_pad_diameter") / 2, 8.0)
    pad = pad.cut(cylinder_axis((0, 0, -0.1), 5.4, 8.2))
    pad = pad.cut(cylinder_axis((0, 0, 3.0), 9.5, 5.1))
    return pad


def upper_pad_holder():
    lx, ly, lz = v("upper_pad_size")
    holder = box_at(82, 11, -11, lx, ly, lz)
    # Eight shallow rubber-key pockets; adhesive supplements mechanical keys.
    for x in (92, 117, 142, 162):
        for y in (20, 64):
            holder = holder.cut(cylinder_axis((x, y, -11.1), 2.5, 1.6))
    return holder


def pad_z_for_desk(thickness):
    return UPPER_CONTACT_Z - thickness - 8.0


def screw_state(thickness):
    pad_z = pad_z_for_desk(thickness)
    screw_top = pad_z
    screw_bottom = screw_top - v("clamp_screw_length")
    screw = cylinder_axis((SCREW_X, SCREW_Y, screw_bottom), 5.0, v("clamp_screw_length"))
    pad = swivel_pad_holder().translate((SCREW_X, SCREW_Y, pad_z))
    hand_knob = knob().translate((SCREW_X, SCREW_Y, screw_bottom - 18.0))
    return screw, pad, hand_knob


def desk_placeholder(thickness):
    return box_at(42, 0, UPPER_CONTACT_Z - thickness, 130, 84, thickness)


def parts():
    return {
        "P1-020_CLAMP_BASE_INTERFACE": interface_plate(),
        "P1-021_CLAMP_VERTICAL_BRACKET": vertical_bracket(),
        "P1-022_CLAMP_SCREW_GUIDE": screw_guide(),
        "P1-023_CLAMP_KNOB": knob(),
        "P1-024_SWIVEL_PAD_HOLDER": swivel_pad_holder(),
        "P1-025_UPPER_RUBBER_PAD_HOLDER": upper_pad_holder(),
    }
