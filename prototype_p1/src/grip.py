"""P1-006 slide-on PETG grip."""

from common import box_at, cylinder_axis
from lever_hub import place_rotating
from parameters import v


def grip_local():
    start = v("grip_start_radius")
    grip = cylinder_axis((start, 0, 0), v("grip_diameter") / 2, v("grip_length"), (1, 0, 0))
    # Through slot lets the grip slide over the commodity steel flat bar.
    slot = box_at(start - 0.1, -2.8, -12.8, v("grip_length") + 0.2, 5.6, 25.6)
    grip = grip.cut(slot)
    grip = grip.cut(cylinder_axis((210.0, -18, 0), 2.25, 36, (0, 1, 0)))
    return grip


def grip_at(angle_deg):
    return place_rotating(grip_local(), angle_deg)


def parts():
    return {"P1-006_GRIP": grip_local()}
