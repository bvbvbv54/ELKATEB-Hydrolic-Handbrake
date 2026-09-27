"""Parametric P1-C parts and assembly state geometry."""

from __future__ import annotations
import math
import cadquery as cq

from common import COLORS, between, box_at, capsule_xz, cyl, prism_xz, rotate_y, shape, slot_xy
from parameters import magnet_center, opposite_lever_point, v


SIDE_PROFILE = [(18, 3), (114, 3), (109, 27), (91, 57), (76, 88),
                (42, 88), (31, 55), (22, 29)]
ACCENT_PROFILE = [(29, 17), (106, 17), (97, 38), (77, 79),
                  (45, 79), (36, 53)]


def _holes_z(obj, coords, diameter, z0=-0.1, depth=4.0):
    for x, y in coords:
        obj = obj.cut(cyl((x, y, z0), diameter / 2, depth))
    return obj


def base_tray():
    t, L, W, h = v("base_sheet"), v("base_length"), v("base_width"), v("base_flange_height")
    floor = box_at(0, 0, 0, L, W, t)
    left = box_at(0, 0, t, L, t, h)
    right = box_at(0, W - t, t, L, t, h)
    rear = box_at(L - t, t, t, t, W - 2 * t, h)
    tray = floor.union(left).union(right).union(rear)
    # Side-frame feet, electronics pod, and removable clamp use through bolts.
    holes = [(32, 14), (96, 14), (32, 74), (96, 74),
             (139, 9), (181, 9), (139, 79), (181, 79),
             (140, 20), (180, 20), (140, 68), (180, 68)]
    tray = _holes_z(tray, holes[:8], v("m6_clearance"), -0.1, t + 0.2)
    tray = _holes_z(tray, holes[8:], v("m4_clearance"), -0.1, t + 0.2)
    tray = _holes_z(tray, [(112, 44), (128, 44)], v("m6_clearance"), -0.1, t + 0.2)
    for y in (17.0, 71.0):
        tray = tray.cut(slot_xy(119.0, y, -0.1, v("rig_slot_length"), v("rig_slot_width"), t + 0.2))
    return tray


def _side_frame(y0, right=False):
    t = v("side_sheet")
    plate = prism_xz(SIDE_PROFILE, y0, t)
    # One-bend foot goes outward; through bolts create a direct base load path.
    if right:
        foot = box_at(18, y0 + t, 3, 96, v("side_foot_width"), t)
        foot_y = 74
    else:
        foot = box_at(18, y0 - v("side_foot_width"), 3, 96, v("side_foot_width"), t)
        foot_y = 14
    part = plate.union(foot)
    part = part.cut(cyl((v("pivot_x"), y0 - 0.1, v("pivot_z")), v("pivot_clearance") / 2, t + 0.2, (0, 1, 0)))
    for x in (32.0, 96.0):
        part = part.cut(cyl((x, foot_y, 2.9), v("m6_clearance") / 2, t + 0.3))
    # M4 accent fasteners.
    for x, z in ((36, 25), (84, 68), (103, 25)):
        part = part.cut(cyl((x, y0 - 0.1, z), v("m4_clearance") / 2, t + 0.2, (0, 1, 0)))
    if right:
        # Full magnet trajectory plus adjustment clearance.  This intentionally
        # removes ferromagnetic steel from between magnet and Hall sensor.
        p_rel = magnet_center(v("released_angle")); p_full = magnet_center(v("full_angle"))
        window = capsule_xz((p_full[0], p_full[2]), (p_rel[0], p_rel[2]),
                            v("magnetic_window_width") / 2, y0 - 0.1, t + 0.2)
        part = part.cut(window)
        for x, z in ((84, 27), (107, 50)):
            part = part.cut(cyl((x, y0 - 0.1, z), v("m3_clearance") / 2, t + 0.2, (0, 1, 0)))
    else:
        # Access window for stop locknuts and spring anchor.
        part = part.cut(capsule_xz((48, 38), (89, 30), 10, y0 - 0.1, t + 0.2))
    return part


def left_side_frame():
    return _side_frame(v("side_left_y"), False)


def right_side_frame():
    return _side_frame(v("side_right_y"), True)


def _accent(y0, right=False):
    t = v("accent_sheet")
    panel = prism_xz(ACCENT_PROFILE, y0, t)
    panel = panel.cut(cyl((v("pivot_x"), y0 - 0.1, v("pivot_z")), 10.5, t + 0.2, (0, 1, 0)))
    # Controlled original aperture and two small round details.
    panel = panel.cut(capsule_xz((52, 42), (80, 55), 8.0, y0 - 0.1, t + 0.2))
    for x, z in ((36, 25), (84, 68), (103, 25)):
        panel = panel.cut(cyl((x, y0 - 0.1, z), v("m4_clearance") / 2, t + 0.2, (0, 1, 0)))
    # The right accent intentionally remains continuous. Aluminium is
    # non-ferromagnetic, so the steel-frame Hall window can be cosmetically
    # covered without putting steel in the magnetic path or splitting the
    # laser-cut accent into disconnected islands.
    return panel


def left_accent():
    return _accent(20.0, False)


def right_accent():
    return _accent(66.0, True)


def lever_local():
    # Original tapered profile.  Root holes clamp into the hidden bearing hub;
    # decorative holes remain well away from the highest-moment root section.
    profile = [(18, -14), (88, -14), (300, -11), (300, 11), (88, 14), (18, 14)]
    lever = prism_xz(profile, -v("lever_sheet") / 2, v("lever_sheet"))
    for x, dia in ((42, 6.6), (70, 6.6), (116, 10.0), (146, 10.0), (176, 10.0), (286, 5.2)):
        lever = lever.cut(cyl((x, -v("lever_sheet") / 2 - 0.1, 0), dia / 2,
                              v("lever_sheet") + 0.2, (0, 1, 0)))
    return lever


def hub_local():
    w = v("hub_width")
    hub = cyl((0, -w / 2, 0), v("hub_radius"), w, (0, 1, 0))
    hub = hub.union(box_at(12, -w / 2, -18, 68, w, 36))
    hub = hub.union(box_at(-52, -10, -10, 34, 20, 20))
    hub = hub.union(box_at(-9, -10, -43, 18, 20, 28))
    # Lever slot and two M6 clamp bolts.
    hub = hub.cut(box_at(17, -2.8, -14.4, 66, 5.6, 28.8))
    for x in (42, 70):
        hub = hub.cut(cyl((x, -w / 2 - 0.1, 0), 3.3, w + 0.2, (0, 1, 0)))
    # Dual replaceable 608 pockets and continuous M8 clearance.
    hub = hub.cut(cyl((0, -w / 2 - 0.1, 0), v("bearing_pocket") / 2,
                      v("hub_pocket_depth") + 0.1, (0, 1, 0)))
    hub = hub.cut(cyl((0, w / 2 + 0.1, 0), v("bearing_pocket") / 2,
                      v("hub_pocket_depth") + 0.1, (0, -1, 0)))
    hub = hub.cut(cyl((0, -w / 2 - 0.1, 0), v("pivot_clearance") / 2, w + 0.2, (0, 1, 0)))
    hub = hub.cut(cyl((-v("moving_anchor_radius"), -10.1, 0), 3.3, 20.2, (0, 1, 0)))
    hub = hub.cut(cyl((0, -10.1, -v("stop_pin_radius")), 3.3, 20.2, (0, 1, 0)))
    return hub


def place_moving(obj, angle):
    return rotate_y(obj, angle).translate((v("pivot_x"), v("pivot_y"), v("pivot_z")))


def lever_at(angle):
    return place_moving(lever_local(), angle)


def hub_at(angle):
    return place_moving(hub_local(), angle)


def grip_local():
    core = cyl((v("grip_start_radius"), 0, 0), v("grip_core_od") / 2,
               v("grip_length"), (1, 0, 0))
    rubber = cyl((v("grip_start_radius"), 0, 0), v("grip_od") / 2,
                 v("grip_length"), (1, 0, 0))
    bore = cyl((v("grip_start_radius") - 0.1, 0, 0), v("grip_core_od") / 2 + 0.3,
               v("grip_length") + 0.2, (1, 0, 0))
    return core, rubber.cut(bore)


def grip_at(angle):
    c, r = grip_local()
    return place_moving(c, angle), place_moving(r, angle)


def grip_trim_at(angle):
    rings=[]
    for x in (v("grip_start_radius")-1.0, v("grip_start_radius")+v("grip_length")-3.0):
        ring=cyl((x,0,0),18.0,4.0,(1,0,0)).cut(cyl((x-.1,0,0),v("grip_core_od")/2+.4,4.2,(1,0,0)))
        rings.append(place_moving(ring,angle))
    return rings


def spring_bracket():
    # Bent steel L bracket with three M6 anchor positions.
    plate = box_at(108, 32, 3, 24, 24, v("side_sheet"))
    upright = box_at(122, 32, 3, v("side_sheet"), 24, 30)
    for x in (112, 128):
        plate = plate.cut(cyl((x, 44, 2.9), 3.3, v("side_sheet") + 0.2))
    for z in (21, 25, 29):
        upright = upright.cut(cyl((121.9, 44, z), 3.3, v("side_sheet") + 0.2, (1, 0, 0)))
    return plate.union(upright)


def spring_points(angle):
    return opposite_lever_point(v("moving_anchor_radius"), angle), (v("fixed_anchor_x"), v("pivot_y"), v("fixed_anchor_z"))


def spring_envelope(angle):
    a, b = spring_points(angle)
    return between(a, b, v("spring_od") / 2)


def _align_z(obj, start, end):
    """Align a local +Z solid to a global start->end vector."""
    a, b = cq.Vector(*start), cq.Vector(*end)
    d = b - a; z = cq.Vector(0, 0, 1); unit = d.normalized()
    dot = max(-1.0, min(1.0, z.dot(unit)))
    angle = math.degrees(math.acos(dot)); axis = z.cross(unit)
    out = obj
    if axis.Length > 1e-9:
        out = cq.Workplane(obj=shape(out)).rotate((0, 0, 0), axis.toTuple(), angle)
    elif dot < 0:
        out = cq.Workplane(obj=shape(out)).rotate((0, 0, 0), (1, 0, 0), 180)
    return cq.Workplane(obj=shape(out)).translate(start)


def spring_solid(angle):
    a, b = spring_points(angle); length = math.dist(a, b)
    coil_len = max(12.0, length - 12.0); pitch = coil_len / 11.0
    coil_radius = v("spring_od") / 2 - 1.2
    path = cq.Wire.makeHelix(pitch, coil_len, coil_radius)
    # Start plane is normal to the helix tangent; this creates a true solid
    # wire rather than a zero-volume swept shell.
    plane = cq.Plane(origin=(coil_radius,0,0), xDir=(1,0,0),
                     normal=(0,coil_radius,pitch/(2*math.pi)))
    wire = cq.Workplane(plane).circle(1.05).sweep(path, isFrenet=True)
    return _align_z(wire, a, b)


def spring_collar_at(angle):
    a, b = spring_points(angle); av, bv = cq.Vector(*a), cq.Vector(*b)
    d = (av - bv).normalized(); start = (bv + d * 4.0).toTuple(); end = (bv + d * 14.0).toTuple()
    local = spring_collar()
    return _align_z(local, start, end)


def spring_length(angle):
    return math.dist(*spring_points(angle))


def stop_pin_at(angle):
    a = math.radians(angle - 90)
    p = (v("pivot_x") + v("stop_pin_radius") * math.cos(a), 29.0,
         v("pivot_z") + v("stop_pin_radius") * math.sin(a))
    return cyl(p, 3.0, 30.0, (0, 1, 0))


def stop_bolts():
    out = []
    for angle, release in ((v("released_angle"), True), (v("full_angle"), False)):
        a = math.radians(angle - 90)
        px = v("pivot_x") + v("stop_pin_radius") * math.cos(a)
        pz = v("pivot_z") + v("stop_pin_radius") * math.sin(a)
        tangent = math.radians(angle if release else angle - 180)
        # 6 mm centre offset makes two Ø6 cylinders tangent at endpoint.
        x = px + 6 * math.cos(tangent); z = pz + 6 * math.sin(tangent)
        local = cyl((x, 19.0, z), 3.0, 12.0, (0, 1, 0))
        out.append(local)
    return out


def magnet_holder_local():
    a = math.radians(v("magnet_local_angle")); r = v("magnet_radius")
    mx, mz = r * math.cos(a), r * math.sin(a)
    cup = box_at(mx - 8, 15, mz - 6, 16, 10, 12)
    arm = rotate_y(box_at(18, 11, -5, 41, 4, 10), v("magnet_local_angle"))
    holder = cup.union(arm)
    sx, sz, sy = v("magnet_size")
    holder = holder.cut(box_at(mx - sx / 2 - .15, 20.0, mz - sz / 2 - .15,
                               sx + .3, sy + .3, sz + .3))
    holder = holder.cut(cyl((mx - 8.1, 22.5, mz), 1.7, 16.2, (1, 0, 0)))
    return holder


def magnet_holder_at(angle):
    return place_moving(magnet_holder_local(), angle)


def magnet_at(angle):
    a = math.radians(v("magnet_local_angle")); r = v("magnet_radius")
    mx, mz = r * math.cos(a), r * math.sin(a)
    sx, sz, sy = v("magnet_size")
    return place_moving(box_at(mx - sx / 2, 20.1, mz - sz / 2, sx, sy, sz), angle)


def hall_window_insert():
    p_rel = magnet_center(v("released_angle")); p_full = magnet_center(v("full_angle"))
    # Non-ferromagnetic printed rim occupies only the edge of the steel cutout.
    outer = capsule_xz((p_full[0], p_full[2]), (p_rel[0], p_rel[2]), 18.0, 64.2, 3.0)
    inner = capsule_xz((p_full[0], p_full[2]), (p_rel[0], p_rel[2]), 14.0, 64.1, 3.2)
    rim = outer.cut(inner)
    for x, z in ((84, 27), (107, 50)):
        rim = rim.cut(cyl((x, 64.1, z), 1.7, 3.2, (0, 1, 0)))
    return rim


def hall_sled(gap=None):
    if gap is None: gap = v("hall_gap")
    full = magnet_center(v("full_angle")); magnet_face_y = 69.0
    board_y = magnet_face_y + gap
    # Rails sit above and below the complete magnet carrier envelope; nothing
    # crosses the sensing gap or acts as a mechanical stop.
    rail_y = 70.5
    rail_depth = board_y - rail_y + 3.0
    sled = box_at(full[0] - 11, rail_y, full[2] - 18, 22, rail_depth, 4)
    sled = sled.union(box_at(full[0] - 11, rail_y, full[2] + 14, 22, rail_depth, 4))
    sled = sled.union(box_at(full[0] - 11, board_y + 1.6, full[2] - 18, 22, 3, 36))
    for x in (full[0] - 5, full[0] + 5):
        for z in (full[2] - 16, full[2] + 16):
            sled = sled.cut(cyl((x, rail_y - .1, z), 1.7, board_y - rail_y + 4.8, (0, 1, 0)))
    return sled


def hall_pcb(gap=None):
    if gap is None: gap = v("hall_gap")
    full = magnet_center(v("full_angle")); sx, sz, sy = v("hall_pcb")
    return box_at(full[0] - sx / 2, 69.0 + gap, full[2] - sz / 2, sx, sy, sz)


def electronics_pod():
    x, y, z = v("electronics_origin"); lx, ly, lz = v("electronics_outer"); wall = v("electronics_wall")
    # A tapered nose makes the pod read as part of the tray, not an added box.
    outer = box_at(x + 8, y, z, lx - 8, ly, lz).union(prism_xz([(x, z), (x + 8, z), (x + 8, z + lz), (x, z + 18)], y, ly))
    inner = box_at(x + 10, y + wall, z + wall, lx - 12, ly - 2 * wall, lz - wall + .2)
    pod = outer.cut(inner)
    pod = pod.cut(box_at(x + lx - wall - .1, y + 22, z + 8, wall + .2, 20, 11))
    pod = pod.cut(cyl((x - .1, y + 14, z + 10), 3.2, 10, (1, 0, 0)))
    for hx, hy in ((140, 20), (180, 20), (140, 68), (180, 68)):
        pod = pod.cut(cyl((hx, hy, z - .1), 2.25, 5.0))
    return pod


def electronics_lid():
    x, y, z = v("electronics_origin"); lx, ly, lz = v("electronics_outer")
    lid = box_at(x + 8, y, z + lz, lx - 8, ly, 3.0)
    # Branding-ready flat top; no permanent mark in manufacturing geometry.
    for hx, hy in ((143, 17), (183, 17), (143, 71), (183, 71)):
        lid = lid.cut(cyl((hx, hy, z + lz - .1), 1.7, 3.2))
    return lid


def cable_guide():
    # Open U-channel: the M3 mounting floor is below the cable path, so the
    # screw bores cannot create non-manifold intersections or touch the cable.
    floor = box_at(112, 63.5, 4, 22, 12, 4)
    lower_rail = box_at(112, 63.5, 8, 22, 3, 5)
    upper_rail = box_at(112, 72.5, 8, 22, 3, 5)
    guide = floor.union(lower_rail).union(upper_rail)
    for x in (116, 130):
        guide = guide.cut(cyl((x, 69.5, 3.9), 1.7, 4.2))
    return guide


def clamp_bracket():
    t = v("clamp_sheet")
    upper = box_at(142, 10, -t, 48, 68, t)
    vertical = box_at(187, 10, -105, t, 68, 105)
    lower = box_at(110, 10, -105, 80, 68, t)
    bracket = upper.union(vertical).union(lower)
    for x in (150, 181):
        for y in (18, 70):
            bracket = bracket.cut(cyl((x, y, -t - .1), 3.3, t + .2))
    bracket = bracket.cut(cyl((v("clamp_screw_x"), 44, -105.1), 5.5, t + .2))
    return bracket


def clamp_knob():
    knob = cyl((0, 0, 0), 17, 18)
    for i in range(6):
        a = math.radians(i * 60)
        knob = knob.union(cyl((18 * math.cos(a), 18 * math.sin(a), 0), 8, 18))
    knob = knob.cut(cyl((0, 0, -.1), 5.3, 18.2))
    return knob.cut(cq.Workplane("XY").polygon(6, 19.8).extrude(7))


def clamp_pad():
    return cyl((0, 0, 0), v("clamp_pad_od") / 2, 8).cut(cyl((0, 0, -.1), 5.4, 8.2))


def spring_collar():
    return cyl((0, 0, 0), 11, 10).cut(cyl((0, 0, -.1), v("spring_od") / 2 + .6, 10.2))


def clamp_state(desk_thickness):
    contact_z = -3.0
    pad_z = contact_z - desk_thickness - 8.0
    screw_top = pad_z + 8.0
    screw_bottom = screw_top - v("clamp_screw_length")
    screw = cyl((v("clamp_screw_x"), 44, screw_bottom), 5, v("clamp_screw_length"))
    pad = clamp_pad().translate((v("clamp_screw_x"), 44, pad_z))
    knob = clamp_knob().translate((v("clamp_screw_x"), 44, screw_bottom - 18))
    desk = box_at(35, 0, contact_z - desk_thickness, 155, 88, desk_thickness)
    return screw, pad, knob, desk


def bearing_ring(y0):
    return cyl((v("pivot_x"), y0, v("pivot_z")), 11, 7, (0, 1, 0)).cut(
        cyl((v("pivot_x"), y0 - .1, v("pivot_z")), 4, 7.2, (0, 1, 0)))


def button_head(center, axis=(0, 1, 0), diameter=8.0, height=2.6):
    head = cyl(center, diameter / 2, height, axis)
    # Visual hex recess only; commodity fastener remains specified in BOM.
    recess_start = cq.Vector(*center) + cq.Vector(*axis).normalized() * (height - .8)
    recess = cq.Workplane("XY", origin=recess_start.toTuple()).polygon(6, diameter * .36).extrude(.9)
    if axis != (0, 0, 1):
        # Hex recess is omitted on non-Z heads; outer head geometry remains exact.
        return head
    return head.cut(recess)


def accent_hardware():
    items=[]
    for x,z in ((36,25),(84,68),(103,25)):
        items.append((f"LEFT_M4_{x}",cyl((x,22.0,z),4.0,2.0,(0,1,0)),"aluminium"))
        items.append((f"LEFT_HEAD_{x}",cyl((x,17.4,z),3.8,2.6,(0,1,0)),"steel"))
        items.append((f"RIGHT_M4_{x}",cyl((x,64.0,z),4.0,2.0,(0,1,0)),"aluminium"))
        items.append((f"RIGHT_HEAD_{x}",cyl((x,68.0,z),3.8,2.6,(0,1,0)),"steel"))
    return items


def components(angle=None, clamp_desk=None, material_view=False):
    if angle is None: angle = v("released_angle")
    items = []
    def add(name, obj, cat): items.append({"name": name, "shape": obj, "category": cat})
    add("P1C-S001_BASE_TRAY", base_tray(), "steel")
    add("P1C-S002_LEFT_SIDE_FRAME", left_side_frame(), "steel")
    add("P1C-S003_RIGHT_SIDE_FRAME", right_side_frame(), "steel")
    add("P1C-S005_SPRING_BRACKET", spring_bracket(), "steel")
    add("P1C-A001_LEFT_ACCENT", left_accent(), "aluminium")
    add("P1C-A002_RIGHT_ACCENT", right_accent(), "aluminium")
    add("P1C-P001_BEARING_HUB", hub_at(angle), "printed")
    add("P1C-S004_STEEL_LEVER", lever_at(angle), "steel")
    core, rubber = grip_at(angle)
    add("HW_GRIP_CORE", core, "aluminium"); add("HW_RUBBER_GRIP", rubber, "rubber")
    for i,ring in enumerate(grip_trim_at(angle),1): add(f"HW_GRIP_TRIM_RING_{i}",ring,"aluminium")
    add("HW_EXTENSION_SPRING", spring_solid(angle), "steel")
    add("P1C-P010_SPRING_COLLAR", spring_collar_at(angle), "red")
    add("HW_STOP_PIN", stop_pin_at(angle), "steel")
    for i, obj in enumerate(stop_bolts(), 1): add(f"HW_M6_STOP_{i}", obj, "steel")
    add("P1C-P002_MAGNET_CARRIER", magnet_holder_at(angle), "printed")
    add("HW_MAGNET", magnet_at(angle), "magnet")
    add("P1C-P003_HALL_WINDOW", hall_window_insert(), "printed")
    add("P1C-P004_HALL_SLED", hall_sled(), "printed")
    add("HW_HALL_PCB", hall_pcb(), "sensor")
    add("P1C-P005_ELECTRONICS_POD", electronics_pod(), "printed")
    add("P1C-P006_ELECTRONICS_LID", electronics_lid(), "printed")
    add("P1C-P007_CABLE_GUIDE", cable_guide(), "printed")
    add("HW_608_LEFT", bearing_ring(29), "bearing")
    add("HW_608_RIGHT", bearing_ring(52), "bearing")
    add("HW_M8_PIVOT", cyl((v("pivot_x"), 4, v("pivot_z")), 4, v("pivot_bolt_length"), (0, 1, 0)), "steel")
    add("HW_PIVOT_WASHER_LEFT", cyl((v("pivot_x"), 16.8, v("pivot_z")), 10.5, 3.2, (0, 1, 0)).cut(cyl((v("pivot_x"),16.7,v("pivot_z")),4.2,3.4,(0,1,0))), "aluminium")
    add("HW_PIVOT_WASHER_RIGHT", cyl((v("pivot_x"), 68.0, v("pivot_z")), 10.5, 3.2, (0, 1, 0)).cut(cyl((v("pivot_x"),67.9,v("pivot_z")),4.2,3.4,(0,1,0))), "aluminium")
    add("HW_M8_BOLT_HEAD", cyl((v("pivot_x"), 12.0, v("pivot_z")), 6.5, 4.8, (0,1,0)), "steel")
    add("HW_M8_NYLOC", cq.Workplane("XZ", origin=(v("pivot_x"),71.2,v("pivot_z"))).polygon(6,15.0).extrude(-7.0), "steel")
    for name,obj,cat in accent_hardware(): add(f"HW_{name}",obj,cat)
    for x,y in ((32,14),(96,14),(32,74),(96,74)):
        add(f"HW_M6_FRAME_{x}_{y}",cyl((x,y,6.0),5.0,3.0),"steel")
    x0,y0,z0=v("electronics_origin"); _,_,lz=v("electronics_outer")
    for x,y in ((143,17),(183,17),(143,71),(183,71)):
        add(f"HW_M3_LID_{x}_{y}",cyl((x,y,z0+lz+3.0),3.0,2.0),"steel")
    if clamp_desk is not None:
        add("P1C-S006_CLAMP_BRACKET", clamp_bracket(), "steel")
        screw, pad, knob, desk = clamp_state(clamp_desk)
        nut = cq.Workplane("XY", origin=(v("clamp_screw_x"),44,v("clamp_nut_z"))).polygon(6,19.8).extrude(30.0)
        add("HW_M10_CLAMP_SCREW", screw, "steel")
        add("HW_M10_COUPLING_NUT", nut, "steel")
        add("P1C-P009_SWIVEL_PAD", pad, "printed")
        add("P1C-P008_CLAMP_KNOB", knob, "printed")
        add("HW_UPPER_RUBBER_PAD", box_at(100,15,-3,80,58,3), "rubber")
        add("FIXTURE_DESK", desk, "desk")
    return items


def exportable_parts():
    return {
        "P1C-S001_BASE_TRAY": (base_tray(), "steel", False),
        "P1C-S002_LEFT_SIDE_FRAME": (left_side_frame(), "steel", False),
        "P1C-S003_RIGHT_SIDE_FRAME": (right_side_frame(), "steel", False),
        "P1C-S004_STEEL_LEVER": (lever_local(), "steel", False),
        "P1C-S005_SPRING_BRACKET": (spring_bracket(), "steel", False),
        "P1C-S006_CLAMP_BRACKET": (clamp_bracket(), "steel", False),
        "P1C-A001_LEFT_ACCENT": (left_accent(), "aluminium", False),
        "P1C-A002_RIGHT_ACCENT": (right_accent(), "aluminium", False),
        "P1C-P001_BEARING_HUB": (hub_local(), "printed", True),
        "P1C-P002_MAGNET_CARRIER": (magnet_holder_local(), "printed", True),
        "P1C-P003_HALL_WINDOW": (hall_window_insert(), "printed", True),
        "P1C-P004_HALL_SLED": (hall_sled(), "printed", True),
        "P1C-P005_ELECTRONICS_POD": (electronics_pod(), "printed", True),
        "P1C-P006_ELECTRONICS_LID": (electronics_lid(), "printed", True),
        "P1C-P007_CABLE_GUIDE": (cable_guide(), "printed", True),
        "P1C-P008_CLAMP_KNOB": (clamp_knob(), "printed", True),
        "P1C-P009_SWIVEL_PAD": (clamp_pad(), "printed", True),
        "P1C-P010_SPRING_COLLAR": (spring_collar(), "printed", True),
    }


def make_assembly(name, angle=None, clamp_desk=None):
    assy = cq.Assembly(name=name)
    for item in components(angle, clamp_desk):
        assy.add(item["shape"], name=item["name"], color=COLORS[item["category"]])
    return assy


def exploded_components():
    out = []
    for item in components(v("released_angle"), None):
        s = item["shape"]; n = item["name"]
        if "LEFT_SIDE" in n or "LEFT_ACCENT" in n: s = s.translate((0, -35, 0))
        elif "RIGHT_SIDE" in n or "RIGHT_ACCENT" in n or "HALL" in n: s = s.translate((0, 35, 0))
        elif "ELECTRONICS" in n or "CABLE" in n: s = s.translate((30, 35, 20))
        elif "BASE" in n: s = s.translate((0, 0, -18))
        elif "LEVER" in n or "GRIP" in n: s = s.translate((0, 0, 18))
        out.append({**item, "shape": s})
    return out
