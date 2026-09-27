# P1.0 physical validation plan

Do not jump directly to a maximum-load or endurance test. Photograph and record every stage, including slicer settings and measured hardware.

## Test 0 — calibration coupons

Print all eight coupon STLs in the same PETG, orientation, nozzle, layer height, cooling, and dimensional compensation intended for P1. Record:

- 608 pocket selection at both 7 and 14 mm depths: 21.8/22.0/22.1/22.2/22.3/22.4 mm.
- M8 clearance: 8.0/8.2/8.4/8.6 mm.
- M6 clearance: 6.0/6.2/6.4/6.6 mm.
- M6 nut trap: 10.0/10.2/10.4/10.6 mm AF.
- Magnet pocket: nominal/+0.1/+0.2/+0.3 mm.
- Hall gap jig: verify 3/5/8/10/12/15 mm with calipers.
- Loaded bearing-wall coupon: confirm bearing insertion/removal, then load its M6 lug progressively.

Return the selected sizes, actual printed dimensions, insertion force/feel, and any cracking or whitening.

## Test 1 — bearing/hub fit

Print P1-004 only after updating coupon-dependent values. Install/remove both bearings twice. They must seat squarely without splitting, rock, or free-fall. Confirm the inner spacer length lets both bearings seat fully.

## Test 2 — pivot free rotation

Print both supports and base. Assemble hub, bearings, spacer, washers, and M8 bolt without lever or spring. Tighten the nyloc gradually. The hub must rotate freely with no tower bowing, axial rattle, or bearing bind.

## Test 3 — core mechanism without spring

Add steel lever, grip, M6 hub bolts, stop pin, and stop blocks. Sweep 75° to 50° at least 50 times. Confirm the only endpoint contacts are the rubber-tipped mechanical stops.

## Test 4 — light spring

Install the lightest viable extension spring. Measure hook distance at release/full and spring force if possible. Confirm reliable return without coil bind, hook opening, anchor bending, or spring contact with printed parts.

## Test 5 — travel stops

Mark both M6 adjusters. Pull firmly into each stop 25 times. Check adjuster rotation, block movement, left-tower whitening, stop-pin bending, and final angle drift. Use locknuts after adjustment.

## Test 6 — progressive static hand load

Use a luggage scale at grip centre. Apply 25, 50, 75, then 100 N, holding each for five seconds. After each step inspect: cracks, whitening, permanent tower spread, bearing-seat movement, lever slip, bolt loosening, base lift, backing-strip movement, spring-anchor damage, and stop damage. The derived torques are 6.13, 12.25, 18.38, and 24.5 N.m for 25/50/75/100 N at 245 mm. Do not attempt 150 N until 100 N passes and the user deliberately accepts a proof test.

## Test 7 — repetition

Cycle 100 pulls, inspect; then 500 total, inspect; then 1000 total, inspect. Record angle, looseness, noise, return consistency, bearing movement, and any PETG creep. This is prototype learning, not a life certification.

## Test 8 — rig mounting

Remove the clamp. Use two M6 bolts and >=18 mm OD washers in the 44 x 7 mm slots. Repeat 50/75/100 N tests. Check slot elongation, base bending, and movement on the rig.

## Test 9 — table clamp range

Assemble with the real steel coupling nut and screw. Test sacrificial boards at 10, 25, 40, and 55 mm. Confirm pad articulation, full thread engagement, knob clearance, accessible tightening, and no desk marking.

## Test 10 — clamp slip/lift

At each desk thickness, apply 25/50/75/100 N progressively. Mark base position to detect slip and use a straightedge/feeler to observe edge lift. Stop for clamp-bracket whitening, coupling-nut movement, screw-guide separation, base lift, rubber extrusion, or desk damage. Do not infer friction capacity from CAD.

## Test 11 — magnet/Hall integration

With mechanical stops proven, install the magnet and SS49E board. Start at 5 mm face gap. Record released, 25%, 50%, 75%, and 100% voltages for both magnet polarities/orientations and gaps 3/5/8/10/12/15 mm. Select a monotonic range that stays clear of supply rails and is repeatable after 100 cycles.

## Test 12 — USB HID later

Connect Hall VCC/GND/signal to a Pro Micro ADC. Implement filtering, calibration, dead zones, and 0–1023 USB HID Slider mapping. Optionally assert a virtual firmware button at about 60% travel. Firmware is intentionally outside this mechanical pass.

## Data to return for P1.1

Coupon selections and measured offsets; actual bearing dimensions; M8 shank length; steel-bar width/thickness; spring dimensions/rate/forces; released/full hand force; stop-angle measurements; clamp nut AF/length; swivel-foot geometry; board/connector envelopes; Hall voltages at all five travel points and each tested gap; photographs of every stressed area after 100/500/1000 pulls.
