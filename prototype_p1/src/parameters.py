"""P1.0 master parameters.

Every design-driving value has an evidence class:
VERIFIED           commodity geometry or a value directly specified by the user.
ASSUMED_P1         an engineering choice for the first printable iteration.
MEASURE_BEFORE_PRINT a nominal purchased-hardware value to check before structural prints.
CALIBRATION_DEPENDENT a printed-fit value selected by the supplied coupons.

Units are millimetres, degrees, newtons, and N.m unless stated otherwise.
"""

from dataclasses import dataclass
from math import cos, radians, sin


@dataclass(frozen=True)
class Parameter:
    value: object
    confidence: str
    note: str


P = {
    # Core envelope and coordinate system: X front->user, Y left->right, Z up.
    "base_length": Parameter(180.0, "ASSUMED_P1", "Within approved 170-190 mm target."),
    "base_width": Parameter(84.0, "ASSUMED_P1", "Within approved 75-90 mm target."),
    "base_thickness": Parameter(10.0, "ASSUMED_P1", "Structural PETG plate over recessed steel strips."),
    "pivot_x": Parameter(50.0, "ASSUMED_P1", "Leaves spring and electronics zones behind pivot."),
    "pivot_y": Parameter(42.0, "DERIVED", "Base centre plane."),
    "pivot_z": Parameter(76.0, "ASSUMED_P1", "66 mm above base top."),
    "support_inner_gap": Parameter(32.0, "ASSUMED_P1", "28 mm hub plus axial washers/clearance."),
    "support_thickness": Parameter(18.0, "ASSUMED_P1", "Printed on outer face for layer-friendly load path."),
    "support_outer_span": Parameter(68.0, "DERIVED", "18 + 32 + 18 mm."),
    # Pivot and bearings.
    "pivot_nominal": Parameter(8.0, "VERIFIED", "Approved M8 steel pivot architecture."),
    "pivot_clearance": Parameter(8.6, "CALIBRATION_DEPENDENT", "Selected from required M8 coupon series."),
    "pivot_bolt_length": Parameter(90.0, "MEASURE_BEFORE_PRINT", "ISO 4014-style partial-thread M8x90 candidate; confirm shank length."),
    "bearing_id": Parameter(8.0, "VERIFIED", "608 commodity nominal ID."),
    "bearing_od": Parameter(22.0, "VERIFIED", "608 commodity nominal OD."),
    "bearing_width": Parameter(7.0, "VERIFIED", "608 commodity nominal width."),
    "bearing_pocket": Parameter(22.2, "CALIBRATION_DEPENDENT", "Nominal P1 hub pocket; coupon decides final."),
    "bearing_pocket_depth": Parameter(7.2, "CALIBRATION_DEPENDENT", "0.2 mm assembly allowance; verify."),
    "hub_width": Parameter(28.0, "ASSUMED_P1", "Two bearings plus 13.6 mm inner-race spacer."),
    "hub_radius": Parameter(24.0, "ASSUMED_P1", "13 mm radial PETG around 22.2 mm pocket."),
    "inner_spacer_length": Parameter(13.6, "DERIVED", "28 - 2 x 7.2 mm pocket depths."),
    "outer_axial_spacer_length": Parameter(2.2, "DERIVED", "(32 mm support gap - 27.6 mm bearing/centre stack) / 2."),
    # Lever and grip.
    "lever_bar_width": Parameter(25.0, "MEASURE_BEFORE_PRINT", "Locally common steel flat-bar target; measure actual stock."),
    "lever_bar_thickness": Parameter(5.0, "MEASURE_BEFORE_PRINT", "Steel carries bending load; measure actual stock."),
    "lever_bar_length": Parameter(280.0, "ASSUMED_P1", "Within approved 250-300 mm raw-bar range."),
    "lever_bar_root_radius": Parameter(20.0, "ASSUMED_P1", "Bar begins 20 mm from pivot inside hub socket."),
    "lever_hand_radius": Parameter(245.0, "DERIVED", "Pivot to centre of 110 mm grip."),
    "lever_released_angle": Parameter(75.0, "ASSUMED_P1", "Approved 70-80 degree rest target."),
    "lever_mid_angle": Parameter(62.5, "DERIVED", "Midpoint of 25 degree travel."),
    "lever_full_angle": Parameter(50.0, "ASSUMED_P1", "25 degree active travel toward user."),
    "grip_length": Parameter(110.0, "ASSUMED_P1", "Within approved 100-120 mm target."),
    "grip_diameter": Parameter(34.0, "ASSUMED_P1", "Within approved 30-35 mm target."),
    "grip_start_radius": Parameter(190.0, "DERIVED", "Ends at 300 mm pivot radius."),
    # Spring.
    "moving_anchor_radius": Parameter(38.0, "ASSUMED_P1", "Opposite lever axis on replaceable hub lug."),
    "fixed_anchor_x": Parameter(108.0, "ASSUMED_P1", "Gives about 70-86 mm hook spacing through travel."),
    "fixed_anchor_z": Parameter(23.0, "ASSUMED_P1", "Steel M6 cross-bolt centre."),
    "spring_envelope_diameter": Parameter(15.0, "MEASURE_BEFORE_PRINT", "Clearance envelope; buy within 15-20 mm OD."),
    "spring_free_length": Parameter(70.0, "MEASURE_BEFORE_PRINT", "Buy an assortment; final rate/free length after test."),
    # Stops.
    "stop_pin_radius": Parameter(20.0, "ASSUMED_P1", "M6 steel pin through hub cam arm."),
    "stop_pin_diameter": Parameter(6.0, "VERIFIED", "M6 nominal pin/bolt."),
    "stop_bumper_diameter": Parameter(10.0, "MEASURE_BEFORE_PRINT", "Rubber-capped M6 stop candidate."),
    # Hall system.
    "magnet_size": Parameter((10.0, 5.0, 3.0), "MEASURE_BEFORE_PRINT", "Nominal neodymium magnet; measure before structural print."),
    "magnet_radius": Parameter(55.0, "ASSUMED_P1", "Clears pivot tower; approaches full-pull sensor monotonically."),
    "hall_nominal_gap": Parameter(5.0, "CALIBRATION_DEPENDENT", "Start point within requested 3-15 mm range."),
    "hall_gap_range": Parameter((3.0, 15.0), "VERIFIED", "User-requested experimental adjustment range."),
    "hall_pcb_size": Parameter((20.0, 10.0, 1.6), "MEASURE_BEFORE_PRINT", "Prototype SS49E breakout envelope."),
    # Electronics.
    "pro_micro_envelope": Parameter((40.0, 20.0, 12.0), "MEASURE_BEFORE_PRINT", "Board plus headers/USB clearance."),
    "electronics_outer": Parameter((50.0, 38.0, 28.0), "ASSUMED_P1", "Rear-right bolt-on enclosure; clears spring module."),
    "electronics_wall": Parameter(2.4, "ASSUMED_P1", "Six 0.4 mm extrusion lines."),
    # Base interfaces.
    "backing_strip_size": Parameter((180.0, 25.0, 3.0), "MEASURE_BEFORE_PRINT", "Two steel strips solve pivot/clamp load path; confirm local stock."),
    "structural_clearance_m6": Parameter(6.6, "CALIBRATION_DEPENDENT", "Through-bolt hole; coupon supplied."),
    "light_clearance_m4": Parameter(4.5, "CALIBRATION_DEPENDENT", "Accessory through-hole."),
    "rig_slot_length": Parameter(44.0, "ASSUMED_P1", "Longitudinal M6 adjustment."),
    "rig_slot_width": Parameter(7.0, "ASSUMED_P1", "M6 washer required."),
    # Clamp.
    "clamp_desk_range": Parameter((10.0, 55.0), "VERIFIED", "Approved desk thickness range."),
    "clamp_throat": Parameter(60.0, "ASSUMED_P1", "Within approved 50-70 mm target."),
    "clamp_screw_nominal": Parameter(10.0, "VERIFIED", "M10 steel clamp screw architecture."),
    "clamp_screw_length": Parameter(100.0, "MEASURE_BEFORE_PRINT", "Provides working engagement for 10-55 mm states."),
    "clamp_coupling_nut_length": Parameter(30.0, "MEASURE_BEFORE_PRINT", "M10 steel coupling nut candidate."),
    "clamp_pad_diameter": Parameter(46.0, "ASSUMED_P1", "Within approved 40-50 mm target."),
    "clamp_knob_diameter": Parameter(50.0, "ASSUMED_P1", "Six-lobe printed knob around steel hardware."),
    "upper_pad_size": Parameter((90.0, 62.0, 3.0), "ASSUMED_P1", "Broad removable rubber contact pad."),
    # Print baseline.
    "nozzle": Parameter(0.4, "VERIFIED", "User-approved prototype assumption."),
    "layer_height": Parameter(0.20, "VERIFIED", "User-approved prototype assumption."),
    "material": Parameter("PETG", "VERIFIED", "User-approved prototype material."),
}


def v(name):
    return P[name].value


def lever_point(radius: float, angle_deg: float) -> tuple[float, float, float]:
    """Point on lever axis in global XYZ."""
    a = radians(angle_deg)
    return (
        v("pivot_x") + radius * cos(a),
        v("pivot_y"),
        v("pivot_z") + radius * sin(a),
    )


def opposite_lever_point(radius: float, angle_deg: float) -> tuple[float, float, float]:
    return lever_point(-radius, angle_deg)


def parameter_rows():
    for name, item in P.items():
        yield name, item.value, item.confidence, item.note
