"""Independent rig-mount definitions; slots are cut directly in P1-001."""

from base import RIG_SLOT_Y
from parameters import v


def pattern():
    return {
        "slot_centres": [(136.0, y) for y in RIG_SLOT_Y],
        "slot_length": v("rig_slot_length"),
        "slot_width": v("rig_slot_width"),
        "fastener": "M6 through-bolt with >=18 mm OD washer",
        "centre_spacing_y": abs(RIG_SLOT_Y[1] - RIG_SLOT_Y[0]),
    }
