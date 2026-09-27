# ELKATEB Sim-Racing Handbrake

Original low-cost sim-racing handbrake development project using a dual-608/M8 pivot, steel lever, extension spring, independent mechanical stops, and contactless Hall-effect position sensing.

## Current designs

- `prototype_p1/` - mostly 3D-printed physical validation prototype. Print and measure the eight calibration coupons before regenerating structural parts.
- `prototype_commercial_v1/` - P1-C Commercial Alpha using laser-cut/bent steel, aluminium accents, hidden magnetic sensing, removable desk clamp, and independent rig mounting.
- `analysis_generated/` - evidence-based engineering audit and reusable measurements. Downloaded reference CAD is deliberately excluded from this repository because its redistribution/commercial rights were not established.

## P1 build order

1. Print all eight files under `prototype_p1/coupons/`.
2. Measure the actual bearings, bolts, nuts, magnet, sensor board, and printed coupon fits.
3. Update calibration-dependent parameters in `prototype_p1/src/parameters.py`.
4. Regenerate P1.1 with `prototype_p1/build.ps1`.
5. Print the 19 functional parts and assemble them with the specified steel lever, reinforcement strips, bearings, and metric hardware.

P1.0 and P1-C are engineering prototypes. CAD checks do not establish production strength, fatigue life, electrical compliance, or commercial safety. Follow the included test plans and perform progressive physical validation.

The current Tunisia purchasing and calibration guide is available at `output/pdf/P1_TUNISIA_PURCHASE_GUIDE.pdf`.
