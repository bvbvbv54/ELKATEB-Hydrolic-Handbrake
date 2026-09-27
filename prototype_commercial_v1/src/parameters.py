"""P1-C Commercial Alpha master parameters.

All dimensions are millimetres unless stated otherwise.  This file is the
single source of truth for geometry, manufacturing assumptions, and analysis.
"""

from dataclasses import dataclass
from math import cos, radians, sin


@dataclass(frozen=True)
class Parameter:
    value: object
    confidence: str
    note: str


P = {
    # Envelope / folded tray
    "base_length": Parameter(190.0, "ASSUMED_P1C", "Commercial alpha tray length."),
    "base_width": Parameter(88.0, "ASSUMED_P1C", "Commercial alpha tray width."),
    "base_sheet": Parameter(3.0, "MANUFACTURING_ASSUMPTION", "Laser-cut mild steel; RFQ 2.5 and 3.0 mm."),
    "base_flange_height": Parameter(15.0, "ASSUMED_P1C", "Upturned edge flange."),
    "bend_inside_radius": Parameter(3.0, "MANUFACTURING_ASSUMPTION", "Final radius per supplier tooling."),
    "pivot_x": Parameter(58.0, "ASSUMED_P1C", "Retains short front overhang and rear equipment zone."),
    "pivot_y": Parameter(44.0, "DERIVED", "Base centre plane."),
    "pivot_z": Parameter(76.0, "ASSUMED_P1C", "Low side-frame silhouette with adequate mechanism clearance."),
    # Side frames
    "side_sheet": Parameter(3.0, "MANUFACTURING_ASSUMPTION", "S235/ST37/DC01 equivalent mild steel."),
    "side_inner_gap": Parameter(34.0, "ASSUMED_P1C", "30 mm hub plus two 2 mm axial spacers."),
    "side_left_y": Parameter(24.0, "DERIVED", "Left plate outside face."),
    "side_right_y": Parameter(61.0, "DERIVED", "Right plate inside face; 34 mm inner gap."),
    "side_foot_width": Parameter(17.0, "ASSUMED_P1C", "One-bend outward foot per side frame."),
    "accent_sheet": Parameter(2.0, "MANUFACTURING_ASSUMPTION", "Non-structural 5xxx/6xxx aluminium accent."),
    # Pivot / hub
    "pivot_nominal": Parameter(8.0, "P1_BASELINE_VERIFIED", "M8 steel pivot architecture."),
    "pivot_clearance": Parameter(8.5, "CALIBRATION_DEPENDENT", "Laser/printed fit to verify."),
    "pivot_bolt_length": Parameter(80.0, "MEASURE_BEFORE_BUILD", "Partial-thread M8 candidate; smooth shank across races."),
    "bearing_id": Parameter(8.0, "COMMODITY_NOMINAL", "608 bearing."),
    "bearing_od": Parameter(22.0, "COMMODITY_NOMINAL", "608 bearing."),
    "bearing_width": Parameter(7.0, "COMMODITY_NOMINAL", "608 bearing."),
    "bearing_pocket": Parameter(22.2, "CALIBRATION_DEPENDENT", "Inherited P1 coupon starting value."),
    "hub_width": Parameter(30.0, "ASSUMED_P1C", "Hidden reinforced printed carrier."),
    "hub_radius": Parameter(25.0, "ASSUMED_P1C", "Adequate wall around 22.2 mm bearing pocket."),
    "hub_pocket_depth": Parameter(7.2, "CALIBRATION_DEPENDENT", "Bearing face allowance."),
    "hub_inner_spacer": Parameter(15.6, "DERIVED", "30 - 2 x 7.2 mm."),
    "hub_outer_spacer": Parameter(2.0, "DERIVED", "(34 - 30) / 2."),
    # Lever and grip
    "lever_sheet": Parameter(5.0, "MANUFACTURING_ASSUMPTION", "Laser-cut mild steel plate."),
    "lever_length": Parameter(300.0, "ASSUMED_P1C", "Pivot to upper end."),
    "hand_radius": Parameter(245.0, "DERIVED", "Approximate hand centre from pivot."),
    "released_angle": Parameter(75.0, "P1_BASELINE_VERIFIED", "Released state."),
    "mid_angle": Parameter(62.5, "DERIVED", "Midpoint."),
    "full_angle": Parameter(50.0, "P1_BASELINE_VERIFIED", "Full-pull state."),
    "grip_length": Parameter(112.0, "ASSUMED_P1C", "Commodity rubber grip target."),
    "grip_od": Parameter(34.0, "ASSUMED_P1C", "Premium-feeling effective diameter."),
    "grip_core_od": Parameter(22.0, "MEASURE_BEFORE_BUILD", "Steel/aluminium tube under rubber grip."),
    "grip_start_radius": Parameter(188.0, "DERIVED", "112 mm grip ends at 300 mm."),
    # Spring / stops
    "moving_anchor_radius": Parameter(45.0, "ASSUMED_P1C", "Steel M6 moving anchor through hub lug."),
    "fixed_anchor_x": Parameter(123.0, "ASSUMED_P1C", "Rear spring bracket centre."),
    "fixed_anchor_z": Parameter(25.0, "ASSUMED_P1C", "Three-position steel anchor."),
    "spring_od": Parameter(18.0, "MEASURE_BEFORE_BUILD", "Commodity extension spring maximum envelope."),
    "spring_free_length": Parameter(75.0, "MEASURE_BEFORE_BUILD", "Select after force testing."),
    "stop_pin_radius": Parameter(21.0, "ASSUMED_P1C", "M6 hub stop pin radius."),
    "stop_nominal": Parameter(6.0, "COMMODITY_NOMINAL", "Replaceable M6 stop hardware."),
    "travel_deg": Parameter(25.0, "DERIVED", "75 - 50 degrees."),
    # Hall / magnet.  Right steel panel contains a window over the complete path.
    "magnet_size": Parameter((10.0, 5.0, 3.0), "MEASURE_BEFORE_BUILD", "Block magnet starting point."),
    "magnet_radius": Parameter(55.0, "P1_BASELINE_VERIFIED", "P1 proven monotonic approach principle."),
    "magnet_local_angle": Parameter(-105.0, "P1_BASELINE_VERIFIED", "Relative to lever axis."),
    "hall_gap": Parameter(6.0, "ASSUMED_P1C", "Initial face gap."),
    "hall_gap_range": Parameter((3.0, 15.0), "P1_BASELINE_VERIFIED", "Prototype adjustment range."),
    "hall_pcb": Parameter((20.0, 10.0, 1.6), "MEASURE_BEFORE_BUILD", "49E breakout envelope."),
    "magnetic_window_width": Parameter(38.0, "ASSUMED_P1C", "Steel exclusion zone around magnet path."),
    # Electronics rear pod
    "electronics_outer": Parameter((54.0, 64.0, 30.0), "ASSUMED_P1C", "Integrated replaceable rear pod."),
    "electronics_wall": Parameter(2.4, "PRINT_ASSUMPTION", "Six 0.4 mm perimeters."),
    "electronics_origin": Parameter((134.0, 12.0, 4.0), "DERIVED", "Behind spring and pivot."),
    "pro_micro_envelope": Parameter((40.0, 20.0, 12.0), "MEASURE_BEFORE_BUILD", "Temporary controller."),
    # Base / mounting
    "rig_slot_length": Parameter(44.0, "ASSUMED_P1C", "Longitudinal M6 adjustment."),
    "rig_slot_width": Parameter(7.0, "MANUFACTURING_ASSUMPTION", "Laser-cut M6 clearance slot."),
    "m6_clearance": Parameter(6.6, "MANUFACTURING_ASSUMPTION", "General M6 through clearance."),
    "m4_clearance": Parameter(4.5, "MANUFACTURING_ASSUMPTION", "General M4 clearance."),
    "m3_clearance": Parameter(3.4, "MANUFACTURING_ASSUMPTION", "General M3 clearance."),
    # Removable steel C-clamp
    "clamp_sheet": Parameter(3.0, "MANUFACTURING_ASSUMPTION", "Laser-cut/bent mild steel."),
    "clamp_throat": Parameter(65.0, "ASSUMED_P1C", "Desk edge to M10 screw axis."),
    "clamp_desk_range": Parameter((10.0, 55.0), "P1_BASELINE_VERIFIED", "Required desk range."),
    "clamp_screw": Parameter(10.0, "COMMODITY_NOMINAL", "M10 steel screw; no printed primary thread."),
    "clamp_screw_length": Parameter(120.0, "MEASURE_BEFORE_BUILD", "Covers required states with 30 mm coupling nut."),
    "clamp_pad_od": Parameter(46.0, "ASSUMED_P1C", "Swivel pad/rubber contact."),
    "clamp_knob_od": Parameter(50.0, "ASSUMED_P1C", "Printed hand knob around steel hardware."),
    "clamp_screw_x": Parameter(125.0, "DERIVED", "190 - 65 mm throat."),
    "clamp_nut_z": Parameter(-103.0, "DERIVED", "Coupling nut begins above lower arm."),
    # Process/density assumptions
    "steel_density_g_cm3": Parameter(7.85, "ENGINEERING_REFERENCE", "Nominal mild steel density."),
    "al_density_g_cm3": Parameter(2.70, "ENGINEERING_REFERENCE", "Nominal aluminium density."),
    "petg_density_g_cm3": Parameter(1.27, "ENGINEERING_REFERENCE", "Solid volume only, not slicer mass."),
}


def v(name):
    return P[name].value


def lever_point(radius, angle_deg):
    a = radians(angle_deg)
    return (v("pivot_x") + radius * cos(a), v("pivot_y"), v("pivot_z") + radius * sin(a))


def opposite_lever_point(radius, angle_deg):
    return lever_point(-radius, angle_deg)


def magnet_center(angle_deg):
    a = radians(angle_deg + v("magnet_local_angle"))
    return (v("pivot_x") + v("magnet_radius") * cos(a), v("pivot_y"), v("pivot_z") + v("magnet_radius") * sin(a))


def rows():
    for key, item in P.items():
        yield key, item.value, item.confidence, item.note
