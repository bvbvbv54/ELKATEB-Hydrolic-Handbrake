# Prototype P1.0 — printable mechanical validation platform

P1.0 is an original, low-cost vertical/diagonal sim-racing handbrake prototype. It is a mechanical test platform, not a production-ready consumer product. The generated B-Rep assembly uses a drilled steel lever, a fixed M8 pivot, two 608 bearings, a simple extension spring, independent mechanical stops, a moving magnet with stationary Hall board, independent rig slots, and a removable M10 desk clamp.

## Start here

1. Inspect `renders/01_ISOMETRIC_ASSEMBLY.png`, `renders/08_PIVOT_SECTION.png`, and `step/P1_ASSEMBLY.step`.
2. Print the eight `coupons/*.stl` files before structural parts.
3. Measure the actual 608 bearings, steel bar, magnet, M8 bolt shank, coupling nut, sensor board, and Pro Micro assembly.
4. Record the coupon selections and update `src/parameters.py`.
5. Regenerate with `powershell -ExecutionPolicy Bypass -File prototype_p1/build.ps1`.
6. Print the mechanical core before the clamp or electronics modules.

The generated geometry passed the checks in `reports/GEOMETRY_VALIDATION.md` and the 90-file round-trip in `reports/EXPORT_ROUNDTRIP.md`. Printed strength and fit remain physical-test items.

## Actual P1.0 geometry

- Base: 180 x 84 x 10 mm.
- Pivot centre: X=50, Y=42, Z=76 mm in the assembly coordinate system.
- Tower inner gap: 32 mm; each tower is 18 mm thick; outer span is 68 mm.
- Rotating hub: 28 mm axial width, 48 mm bearing barrel diameter, two 22.2 x 7.2 mm nominal pockets.
- Bearings: 2 x 608, 8 x 22 x 7 mm; two more are recommended as fit/test spares.
- Pivot: M8x90 candidate. The smooth shank must cover both bearing inner races; verify the purchased bolt.
- Steel lever: 25 x 5 x 280 mm stock; pivot-to-grip-centre lever arm is 245 mm.
- Released/mid/full angles: 75 / 62.5 / 50 degrees, giving 25 degrees active travel.
- Grip: 34 mm diameter x 110 mm long.
- Spring hook-centre distances: 69.76 / 77.97 / 85.82 mm through the three states.
- Hall centre distance: 23.99 / 12.63 / 5.02 mm; the magnet approaches monotonically toward full pull.
- Electronics enclosure: 50 x 38 x 28 mm body plus 5 mm cover envelope.
- Rig slots: two 44 x 7 mm longitudinal slots, centred at X=136 and Y=32/52 mm.
- Clamp: 60 mm throat, M10x100 screw candidate, 10–55 mm desk range, 46 mm lower pad.
- Released unclamped assembly envelope: 180 x 96 x 370.18 mm including protruding hardware.
- Full-pull unclamped envelope: 255.86 x 96 x 316.74 mm.

## Parts to print

|ID|Part|Recommended orientation|Support guidance|
|---|---|---|---|
|P1-001|Base|top face on bed; steel recesses upward|none|
|P1-002|Left pivot support|outer Y face on bed|none; ream holes after print|
|P1-003|Right pivot support|outer Y face on bed|none|
|P1-004|Bearing hub|one bearing face on bed|support only inside accessible lever slot if bridging is poor|
|P1-006|Grip|upright on end with brim|none; drill/ream retaining bore|
|P1-007|Spring anchor module|foot on bed|none|
|P1-008/009|Stop blocks|outer Y face on bed|none|
|P1-010|Magnet holder|inner arm face on bed|small local support may be required at cup|
|P1-011A/B|Hall bracket and sled|largest flat face on bed|inspect rail bridges|
|P1-012|Electronics enclosure|bottom on bed|none|
|P1-013|Electronics cover|outer top face on bed|none|
|P1-020|Clamp interface|large face on bed|none|
|P1-021|Clamp vertical bracket|large X face on bed|none; orient ribs upward|
|P1-022|Clamp screw guide|lower arm face on bed|none; hex pocket vertical|
|P1-023|Clamp knob|flat face on bed|none|
|P1-024|Swivel-pad holder|flat face on bed|none|
|P1-025|Upper-pad holder|large face on bed|none|

Initial slicer baseline: PETG, 0.4 mm nozzle, 0.20 mm layer, 5–6 perimeters, 6 top/bottom layers, 40–60% infill. Use higher local wall count around pivot, stop, spring, and clamp bores. Do not substitute 100% infill for correct orientation and hardware.

## Steel fabrication

### Lever P1-005

Cut 25 x 5 mm steel flat bar to 280 mm. Hole centres are measured from the lower raw-bar end and across the 25 mm width centreline:

- X=16 mm: Ø6.6 mm, first hub clamp bolt.
- X=40 mm: Ø6.6 mm, second hub clamp bolt.
- X=190 mm: Ø4.5 mm, grip retaining bolt.

Use `dxf/P1-005_STEEL_LEVER_TEMPLATE.dxf` or `drawings/P1-005_STEEL_LEVER_DIMENSIONS.svg`. Deburr every edge and hole. Confirm actual bar width/thickness before printing P1-004 and P1-006.

### Backing strips P1-030/P1-031

Cut two strips, each 180 x 25 x 3 mm. Drill Ø6.6 mm holes at X=32, 68, 125, and 165 mm on the 12.5 mm centreline. These strips sit in the base underside recesses and carry the pivot-tower and clamp-interface through-bolts.

## Assembly order

1. Fit the two steel backing strips into the base underside recesses.
2. Through-bolt both pivot supports to the base/backing strips; do not crush PETG.
3. Press or slip-fit one 608 into each open hub face according to the coupon result.
4. Place the 13.6 mm centre spacer between inner races. Build a measured 2.2 mm axial spacer stack between each tower and adjacent inner race; use steel washers plus precision shims or cut spacer tubes, not PETG.
5. Insert the steel lever 56 mm into the hub socket and install two M6 through-bolts with washers and nylocs.
6. Install the M6 moving spring pin and M6 stop pin in the hub.
7. Put the hub between towers. Pass the M8 smooth shank through left tower, washer, first bearing, spacer, second bearing, washer, and right tower. Tighten the nyloc only enough to clamp the inner-race stack without tower distortion.
8. Bolt on both stop blocks and adjust their M6 rubber-tipped screws to touch the stop pin at 75° and 50°.
9. Bolt the spring module to the base. Install a light extension spring between steel anchors only after the no-spring motion test passes.
10. Slide the grip over the bar and retain it with the M4 cross-bolt.
11. Install the magnet carrier and keeper screw. Keep the magnet out during first mechanical load tests.
12. Install the Hall fixed bracket, sliding sled, and board. Start at 5 mm nominal face gap.
13. Install the Pro Micro enclosure and route the Hall cable away from moving parts.
14. For desk mode, attach the clamp interface with four M6 through-bolts, join the vertical bracket and screw guide, insert the real M10 coupling nut/screw, then fit pad and knob.
15. For rig mode, remove the entire clamp and use the two 44 x 7 mm base slots with large washers.

## First mechanical test

Move the core by hand with no spring and no electronics. Confirm free bearing rotation, positive stop contact, and no bar/tower contact. Add the lightest spring. Use a luggage scale at grip centre and step through 25, 50, 75, then 100 N while inspecting the items in `TEST_PLAN.md`. Stop immediately at cracking, whitening, permanent movement, or fastener loosening.

## Regeneration

CadQuery 2.8 and its small Python dependencies are project-local under `.tools/`; OpenCascade and analysis libraries are reused read-only from `analysis_generated/python_packages`.

```powershell
powershell -ExecutionPolicy Bypass -File prototype_p1/build.ps1
```

The source of truth is `src/parameters.py`. Do not edit exported STEP/STL files by hand.
