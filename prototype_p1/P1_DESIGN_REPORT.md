# Prototype P1.0 mechanical design report

**Status:** generated first CAD iteration for inspection and calibration printing.  
**CAD source:** CadQuery 2.8/OpenCascade B-Rep in `src/`.  
**Validation:** 30 source parts/coupons valid; 15 design checks with 13 PASS and 2 REVIEW; 90 exported files round-trip checked with zero failures.  
**Boundary:** this is an engineering prototype, not a certified product or final commercial design.

## 1. Design overview

P1.0 is an original vertical/diagonal handbrake core optimized for low-cost FDM prototyping. A steel flat-bar lever rotates with a printed bearing hub around a fixed M8 steel pivot. Two 608 bearings isolate rotation from PETG. A single extension spring supplies return force. Two mechanical M6 stop screws define 25° travel independently of the magnet and Hall sensor. The 180 x 84 mm base accepts either a removable desk clamp or two independent rig slots.

The model is deliberately modular. The towers, hub, lever, spring anchor, stops, sensor carrier, electronics box, clamp frame, and grip are separable. This permits cheap failure/fit iterations and later replacement of only the lever/hub module for a horizontal P1-H derivative.

## 2. Architecture

The mechanical load path is:

`hand -> steel lever -> two M6 hub bolts and broad socket -> printed rotating hub -> two 608 outer races -> bearing balls/inner races -> M8 steel pivot and inner spacer -> paired PETG towers -> four M6 through-bolts -> two steel backing strips -> base -> rig bolts or removable clamp -> desk/rig`.

The sensing path is separate:

`low-load hub arm -> mechanically retained magnet -> air gap -> stationary SS49E board -> three-wire cable -> removable Pro Micro enclosure`.

The Hall parts do not carry lever, spring, or stop load.

## 3. Parameter system

All design-driving values are in `src/parameters.py` with one of four classes:

- **VERIFIED:** commodity nominal or explicit approved requirement.
- **ASSUMED_P1:** chosen for this prototype iteration.
- **MEASURE_BEFORE_PRINT:** purchased hardware/stock must be measured.
- **CALIBRATION_DEPENDENT:** select from printed coupons.

`reports/parameters.csv` is the machine-readable parameter table. Important values are base 180 x 84 x 10 mm; pivot (50,42,76); 32 mm inner tower gap; 18 mm towers; hub 28 mm; M8 pivot; 608 bearings; 280 x 25 x 5 mm lever; 75° release; 50° full pull; 55 mm magnet radius; 60 mm clamp throat; and 10–55 mm desk range.

## 4. Load path and simple statics

The hand centre is 245 mm from the pivot. Hand forces of 50/75/100/150 N create 12.25/18.38/24.5/36.75 N.m. If that moment were reacted as an ideal force couple over the 60 mm clamp throat, the corresponding reactions would be roughly 204/306/408/613 N. These figures motivate broad pads, through-bolts, steel strips, and progressive physical tests; they are not clamp-capacity predictions.

For an ideal unperforated 25 x 5 mm bar loaded in its strong 25 mm plane, elementary elastic bending gives approximately 23.5/35.3/47.0/70.6 MPa at those loads. Steel grade, holes, fatigue, out-of-plane loading, and actual stock size are not included. There is no claimed safety factor. See `calculations/LOAD_CALCULATIONS.md`.

PETG strength, creep, interlayer behavior, and print defects make tower/base/stop/clamp capacity **PHYSICAL TEST REQUIRED**.

## 5. Pivot design

The fixed pivot candidate is an M8x90 class 8.8 partially threaded bolt. Its head and nyloc remain outside the 68 mm support span for access. The desired journal is the smooth shank; threads should not run through the bearing inner races. Before structural printing, measure the actual unthreaded length. If it does not cover the complete bearing/washer/tower stack, use an M8 precision shoulder bolt, a suitable longer partially threaded bolt cut to length, or an 8 mm shaft with retained ends.

The support holes are nominal 8.6 mm but CALIBRATION_DEPENDENT. The bolt is fixed by the head/nyloc; the hub rotates on bearings.

## 6. Bearing design

P1-004 contains two co-axial, side-open 22.2 mm diameter x 7.2 mm deep pockets for 608 bearings. The 28 mm hub width leaves a derived 13.6 mm distance between pocket bottoms. A centre metal tube and two equal 2.2 mm outer steel spacer stacks transmit M8 tightening load through the inner races; they prevent the hub or bearing shields from becoming the axial clamp member. The outer stacks must be measured from real washers/shims or cut tube—ordinary washer thickness is not assumed.

The nominal 22.2 mm pocket is not asserted as correct for the available printer. Both 7 mm and 14 mm depth coupon series cover 21.8–22.4 mm. Bearings remain removable from either face after the pivot/towers are separated.

## 7. Lever design

The load-carrying lever is 25 x 5 x 280 mm steel. Its lower end begins at 20 mm pivot radius and enters a 61 mm-long printed socket. Two Ø6.6 holes in the bar at 16 and 40 mm from its lower end align to M6 hub bolts. The bolts are 24 mm apart and the surrounding hub block is 28 mm wide, distributing load better than a single small printed lug.

The grip-retaining Ø4.5 hole is 190 mm from the lower end. DXF and SVG templates are supplied. The bar can be cut/drilled with a hacksaw, drill, file, square, and caliper.

## 8. Grip design

P1-006 is a 34 mm diameter x 110 mm long sleeve over the steel bar. Its 25.6 x 5.6 mm slot is intentionally fit-dependent. A transverse M4 bolt mechanically retains the grip; glue is unnecessary. It should be printed upright with a brim unless the selected printer produces cleaner internal slots horizontally.

## 9. Spring design

P1.0 uses one extension spring between steel M6 anchors. The hub-side anchor is 38 mm opposite the lever axis. The fixed module centre is X=108, Z=23 mm and provides three positions at X=104/108/112. In the nominal centre hole, hook-centre distances are 69.76 mm released, 77.97 mm mid, and 85.82 mm full pull. This provides approximately 16.1 mm working extension before considering hook geometry/preload.

The CAD checks a 15 mm-diameter clearance envelope. Purchase several 15–20 mm OD, 60–100 mm hook-to-hook springs. Free length, initial tension, rate, and allowable extension are not frozen.

## 10. Travel stops

A steel M6 pin at 20 mm radius rotates with the hub through a clearance arc in the left tower. P1-008 and P1-009 mount outside the left tower and carry tangential M6 adjusters with rubber tips. Their positions correspond to 75° and 50°. Hardware contacts are tangent in CAD; locknuts secure the final adjustment. The stop blocks attach with four M4 through-bolts across the 18 mm tower; heat-set inserts do not carry stop force.

The stops are the only intended travel limits. The spring, Hall carrier, magnet, sensor board, enclosure, and USB cable have clearance in all three checked states.

## 11. Hall sensor integration

The moving magnet holder is bolted to the hub by two M3 screws. Its radial arm sits inside the support gap and steps outward only after clearing the right tower. A 10 x 5 x 3 mm candidate magnet fits an outward-opening pocket and is retained by a transverse M3 keeper; adhesive may be secondary retention.

The magnet radius is 55 mm. The board is at the full-pull endpoint, not the travel midpoint. Therefore 3D centre distance reduces monotonically: 23.99 mm released, 12.63 mm mid, 5.02 mm full at the nominal setting. The fixed bracket plus separate sled supports 3–15 mm face-gap experimentation through two clamped rails. Mechanical stops protect the minimum gap.

Physical testing must establish magnet polarity/orientation and whether the SS49E response remains monotonic and sufficiently linear. Record voltages at release/25/50/75/100%.

## 12. Electronics packaging

P1-012 is a 50 x 38 x 28 mm rear-right enclosure with 2.4 mm walls, a rear USB opening, a pivot-facing Hall cable route, and four base mounting holes. P1-013 is a separate four-screw cover with a locating lip. The nominal usable controller envelope is 40 x 20 x 12 mm. Cover inserts are permitted because they are not structural.

The enclosure does not overlap the pivot, spring module, lever sweep, magnet carrier, or primary clamp load path. It removes without disassembling the pivot.

## 13. Base design

P1-001 is a 180 x 84 x 10 mm structural plate. Its underside has two 176 x 25.4 x 3.3 mm open recesses for the steel strips. The base is printed top-face-down so recesses face upward and do not require 25 mm bridges. Four tower holes, four clamp holes, two spring-module holes, two rig slots, electronics holes, and light accessory holes are through features.

The base is separate from towers and clamp; a failed part does not require reprinting a large cosmetic shell.

## 14. Table clamp design

P1-020 is a 64 x 72 x 8 mm interface plate attached by four M6 bolts through the base and steel strips. P1-021 is a 10 mm structural rear wall with side ribs and two butt-bolted joints. P1-022 is a 76 x 32 mm lower arm with a 38 mm-deep boss and a hexagonal pocket for a real M10 coupling nut. P1-023 is a six-lobe knob, P1-024 a 46 mm carrier for a commodity swivel foot/pad, and P1-025 a 90 x 62 mm upper rubber-pad holder.

The screw axis is X=112, 60 mm inward from the desk edge at X=172. The M10x100 candidate spans the complete 30 mm coupling nut in all four checked states. The knob remains below the lower arm. No printed M10 thread carries clamp force.

## 15. Clamp load path

`lower pad -> M10 steel screw -> M10 steel coupling nut -> thick printed screw-guide boss/lower arm -> two M6 butt-joint bolts -> ribbed vertical bracket -> two M6 upper joint bolts -> clamp interface -> four M6 base bolts -> two steel backing strips/base -> upper pad -> desk`.

Static CAD states at 10/25/40/55 mm have exact pad/desk contact and zero overlap. These checks cannot predict rubber friction, desk stiffness, PETG creep, tightening torque, or slip resistance. Test on sacrificial boards first.

## 16. Rig mounting

Rig mode removes P1-020 through P1-025. Two 44 x 7 mm slots run longitudinally at Y=32 and 52 mm, centre X=136 mm. Use M6 bolts with washers at least 18 mm OD. The clamp-bolt axes at Y=18/66 do not coincide with rig slots.

## 17. 3D-print strategy

Baseline is PETG, 0.4 mm nozzle, 0.20 mm layers, 5–6 perimeters, six top/bottom layers, and 40–60% infill. Geometry/through-bolts/steel carry load; 100% infill is not the strategy. Towers print on outer faces so the M8 and stop/hall transverse holes are vertical. The hub prints on a bearing face for round pockets; its accessible lever socket may need local support over a 25.6 mm bridge. The screw guide prints with the coupling-nut pocket vertical.

All exported STLs are watertight. This does not establish dimensional accuracy or printability on a specific machine.

## 18. Metal fabrication

Only three cut/drilled pieces are designed: one 280 x 25 x 5 mm lever and two 180 x 25 x 3 mm backing strips. Supplied DXFs declare millimetres and re-import correctly. All edges/holes must be deburred. No CNC, welding, bending, or custom-turned shaft is required. The 13.6 mm inner-race spacer can be cut from common 8 mm-ID tube or assembled from a measured precision spacer stack, but a single tube is preferred.

## 19. BOM

The purchase list is in `BOM.md`. Core items are two installed 608-2RS bearings plus two spares, M8 pivot hardware, steel lever/strips, an M6 assortment and nylocs, extension-spring assortment, M10x100 screw, M10 coupling nut, commodity swivel pad/foot, rubber pads, magnet, SS49E board, Pro Micro, three-wire connector/cable, and PETG.

## 20. Assembly sequence

Fit strips; bolt towers; install bearings/spacer; bolt lever into hub; install moving spring/stop pins; install hub/M8 stack; install stops; test dry motion; install grip; install light spring; test progressively; only then add magnet/Hall and electronics; add clamp last. The full practical sequence is in `README.md`.

## 21. Required calibration prints

Eight STEP/STL coupon files are supplied: 608 pockets at 7 and 14 mm depth, M8 clearance, M6 clearance, M6 nut traps, magnet pockets, Hall gap jig, and loaded bearing-wall coupon. All are valid single solids and their STLs are watertight. Print these before any structural component.

## 22. Testing procedure

The staged procedure in `TEST_PLAN.md` covers coupons; bearing/hub fit; free pivot; no-spring core; light spring; stops; 25/50/75/100 N progressive loads; 100/500/1000 pulls; rig mode; all four desk sizes; clamp slip/lift; Hall voltages; and later USB HID Slider mapping. A 150 N case is only a later deliberate proof-case consideration.

## 23. Known uncertainties and weak areas

- PETG creep/fatigue at tower roots, hub socket, stop blocks, spring module, and clamp joints.
- Actual 608 press/slip fit and bearing-pocket roundness.
- Actual M8 bolt shank length and inner-spacer length.
- Steel-bar and magnet stock variation.
- Hub lever-slot bridging quality when printed for best bearing accuracy.
- Spring initial tension/rate/hook fatigue and force feel.
- Stop screw/rubber durability and left-tower local load.
- Hall board size, sensing-element position, magnet polarity, and transfer curve.
- Real coupling-nut AF/length and swivel-foot geometry.
- Clamp friction, desk compliance, and printed clamp creep.
- Pro Micro connector location and cable bend radius.

These are deliberately exposed by replaceable parts/coupons rather than hidden by unjustified certainty.

## 24. Measurements required before P1.1

Provide actual 608 OD/width; selected bearing pocket at both depths; printed M8/M6 hole results; selected nut trap; steel bar width/thickness; M8 overall and smooth-shank length; spacer tube ID/OD; exact magnet; Hall PCB and sensing-element location; Pro Micro with headers/USB; M10 coupling-nut AF/length; clamp screw/head; swivel pad interface; selected spring dimensions/forces; actual released/full angles; and all Hall voltage results.

## 25. Horizontal-module and product-family strategy

The future P1-H changes the lever/hub socket orientation and stop locations while retaining base, towers, M8/608 stack, steel strips, rig slots, clamp, electronics enclosure, and stationary Hall-platform concept. It should be a separate bolt-on hub/lever module, not a complex continuously adjustable joint.

For later products, the current platform separates reusable core interfaces from tier-specific features: an entry horizontal lever can use simpler resistance; a mid-range vertical model can improve bearings/spring adjustment/materials; a premium model can add alternate hubs, travel adjustment, stronger metal structures, or later load-cell sensing. None of those variants is being claimed as designed here.

## Export evidence

- `reports/geometry_validation.json`: source-solid dimensions, state checks, distances, clamp states, and envelopes.
- `reports/part_geometry.csv`: machine-readable part dimensions/volume/validity.
- `reports/design_review_checklist.csv`: PASS/REVIEW/FAIL checklist.
- `reports/export_roundtrip.json`: STEP/STL/DXF/PNG re-import results.
- `step/`: individual B-Reps, main assembly, exploded view, three motion states, rig state, and four desk states.
- `stl/`: nineteen printable components.
- `dxf/` and `drawings/`: steel fabrication templates.
- `renders/`: nineteen visual inspection views.
