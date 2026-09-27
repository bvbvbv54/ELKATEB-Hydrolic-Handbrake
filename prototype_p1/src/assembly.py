"""P1.0 static assembly states and purchased-hardware placeholders."""

from __future__ import annotations

import cadquery as cq

import base
import clamp
import electronics_box
import grip
import hall_mount
import lever_hub
import pivot_supports
import spring_system
import stops
from common import COLORS, box_at, cylinder_axis
from parameters import v


def ring(center, od, id_, width, direction=(0, 1, 0)):
    outer = cylinder_axis(center, od / 2, width, direction)
    inner = cylinder_axis(center, id_ / 2, width, direction)
    return outer.cut(inner)


def purchased_pivot_hardware():
    px, py, pz = v("pivot_x"), v("pivot_y"), v("pivot_z")
    return {
        "HW_608_LEFT": ring((px, 28.2, pz), 22.0, 8.0, 7.0),
        "HW_608_RIGHT": ring((px, 48.8, pz), 22.0, 8.0, 7.0),
        "HW_INNER_RACE_SPACER": ring((px, 35.2, pz), 10.0, 8.4, v("inner_spacer_length")),
        "HW_AXIAL_SPACER_LEFT": ring((px, 26.0, pz), 16.0, 8.4, v("outer_axial_spacer_length")),
        "HW_AXIAL_SPACER_RIGHT": ring((px, 55.8, pz), 16.0, 8.4, v("outer_axial_spacer_length")),
        "HW_M8X90_PIVOT": cylinder_axis((px, -4.0, pz), 4.0, 90.0, (0, 1, 0)),
        "HW_M8_BOLT_HEAD": cylinder_axis((px, -10.0, pz), 6.5, 6.0, (0, 1, 0)),
        "HW_M8_NYLOC": cylinder_axis((px, 76.0, pz), 7.5, 8.0, (0, 1, 0)),
    }


def _component(name, shape, category="printed"):
    return {"name": name, "shape": shape, "category": category}


def components(angle_deg=None, clamp_thickness=None, include_desk=True):
    if angle_deg is None:
        angle_deg = v("lever_released_angle")
    items = []

    for name, shape in base.parts().items():
        category = "steel" if "BACKING" in name else "printed"
        items.append(_component(name, shape, category))
    for module in (pivot_supports, spring_system, stops, electronics_box):
        for name, shape in module.parts().items():
            items.append(_component(name, shape, "printed_alt" if "SUPPORT" in name else "printed"))

    items.extend([
        _component("P1-004_HUB", lever_hub.hub_at(angle_deg)),
        _component("P1-005_STEEL_LEVER", lever_hub.lever_at(angle_deg), "steel"),
        _component("P1-006_GRIP", grip.grip_at(angle_deg), "printed_alt"),
        _component("P1-010_MAGNET_HOLDER", hall_mount.magnet_holder_at(angle_deg), "printed_alt"),
        _component("HW_MAGNET", hall_mount.magnet_solid_at(angle_deg), "magnet"),
        _component("P1-011A_HALL_FIXED_BRACKET", hall_mount.fixed_bracket(), "printed_alt"),
        _component("P1-011B_HALL_SENSOR_SLED", hall_mount.sensor_sled(), "printed_alt"),
        _component("HW_HALL_PCB", hall_mount.sensor_pcb(), "sensor"),
        _component("HW_EXTENSION_SPRING_ENVELOPE", spring_system.spring_envelope(angle_deg), "spring"),
        _component("HW_STOP_PIN", stops.stop_pin(angle_deg), "steel"),
    ])
    for i, screw in enumerate(stops.stop_screws(), 1):
        items.append(_component(f"HW_M6_STOP_SCREW_{i}", screw, "steel"))
    for name, shape in purchased_pivot_hardware().items():
        items.append(_component(name, shape, "bearing" if "608" in name else "steel"))
    items.append(_component("HW_PRO_MICRO_ENVELOPE", electronics_box.pro_micro_placeholder(), "sensor"))

    if clamp_thickness is not None:
        for name, shape in clamp.parts().items():
            # State-specific pad and knob replace their export-position equivalents.
            if name in ("P1-023_CLAMP_KNOB", "P1-024_SWIVEL_PAD_HOLDER"):
                continue
            items.append(_component(name, shape, "printed_alt"))
        screw, pad, knob = clamp.screw_state(clamp_thickness)
        items.extend([
            _component("HW_M10_CLAMP_SCREW", screw, "steel"),
            _component("P1-024_SWIVEL_PAD_HOLDER", pad, "printed_alt"),
            _component("P1-023_CLAMP_KNOB", knob, "printed_alt"),
            _component("HW_M10_COUPLING_NUT", cq.Workplane("XY", origin=(clamp.SCREW_X, clamp.SCREW_Y, clamp.NUT_Z0)).polygon(6, 19.6).extrude(30.0), "steel"),
        ])
        if include_desk:
            items.append(_component(f"FIXTURE_DESK_{clamp_thickness:g}MM", clamp.desk_placeholder(clamp_thickness), "desk"))
    return items


def make_assembly(name, angle_deg=None, clamp_thickness=None, include_desk=True):
    assy = cq.Assembly(name=name)
    for item in components(angle_deg, clamp_thickness, include_desk):
        assy.add(item["shape"], name=item["name"], color=COLORS[item["category"]])
    return assy


def exploded_components(angle_deg=None):
    items = components(angle_deg, clamp_thickness=None)
    result = []
    for i, item in enumerate(items):
        shape = item["shape"]
        if "LEFT_PIVOT" in item["name"] or "RELEASE_STOP" in item["name"] or "FULL_PULL" in item["name"]:
            shape = shape.translate((0, -26, 0))
        elif "RIGHT_PIVOT" in item["name"] or "HALL" in item["name"]:
            shape = shape.translate((0, 26, 0))
        elif "ELECTRONICS" in item["name"] or "PRO_MICRO" in item["name"]:
            shape = shape.translate((20, 28, 20))
        elif "BACKING" in item["name"]:
            shape = shape.translate((0, 0, -12))
        result.append({**item, "shape": shape})
    return result
