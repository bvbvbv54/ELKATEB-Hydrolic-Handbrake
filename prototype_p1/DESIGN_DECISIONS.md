# P1.0 design decisions

## Architecture selected

P1.0 uses a printed modular skeleton around a commodity steel load path. The 25 x 5 mm steel lever transmits torque into a replaceable printed hub with two 608 bearings. A fixed M8 bolt clamps the bearing inner races through a 13.6 mm spacer; the hub and bearing outer races rotate. Separate PETG towers are through-bolted into two recessed 180 x 25 x 3 mm steel strips. This makes the high-load pieces replaceable and avoids printed shafts, printed primary threads, and a monolithic housing.

## Pivot stack

From left to right: M8 bolt head, left tower, measured 2.2 mm steel axial spacer stack, 608 inner race, 13.6 mm steel/aluminium centre spacer tube, second 608 inner race, measured 2.2 mm steel axial spacer stack, right tower, M8 nyloc. The hub contains two open 22.2 x 7.2 mm bearing seats, recessing each 7 mm bearing by 0.2 mm. The three spacer sections carry tightening load through the inner races and prevent binding. The M8x90 candidate is not frozen: confirm its unthreaded shank covers the complete 68 mm tower span and both inner races.

## Lever-hub connection

The lever is not a printed cantilever. A 25 x 5 x 280 mm steel bar enters a 25.6 x 5.6 mm hub socket and is retained by two M6 bolts 24 mm apart. The surrounding PETG clamp block is broad rather than a small tab. Fit depends on real steel stock and printer calibration.

## Spring

One extension spring acts between two steel M6 pins. The moving pin is 38 mm opposite the lever axis; the fixed anchor centre is X=108, Z=23 mm. Hook distance increases from 69.76 to 85.82 mm through the 25° travel. Spring free length, rate, hook style, and safe extension remain MEASURE_BEFORE_PRINT/physical-test items. Three fixed-anchor holes at X=104/108/112 allow small tuning without redesign.

## Mechanical stops

An M6 steel pin at 20 mm radius moves through a clearance arc in the left tower. Two separately printed blocks hold tangential M6 rubber-tipped screws. The stop pin/screw surfaces—not the spring, magnet, Hall board, or enclosure—define 75° release and 50° full pull. The blocks use through-bolts into the tower; no insert carries stop load.

## Hall system

The 10 x 5 x 3 mm block magnet candidate is mechanically captured in a moving cup and retained by an M3 keeper screw; adhesive is optional secondary retention. A low-load arm places it at 55 mm radius, outside the structural tower. The stationary sensor is centred at the full-pull endpoint, so centre distance reduces monotonically from 23.99 to 12.63 to 5.02 mm. A fixed bracket and clamped sled provide 3–15 mm face-gap adjustment. The mechanical stop protects the board.

## Electronics

The 50 x 38 x 28 mm enclosure is in the rear-right bay, away from the pivot and spring path. It has a screw-on cover, rear USB opening, front Hall-cable route, four base bolts, and room for a nominal 40 x 20 x 12 mm Pro Micro envelope. Actual boards/connectors must be measured.

## Clamp

The clamp is a removable three-piece C-frame. A four-bolt interface reacts into the same steel strips as the towers. A butt-bolted vertical bracket transfers load to a lower screw guide. The guide captures a real 30 mm M10 coupling nut; the printed part contains no primary M10 thread. An M10x100 steel screw drives a 46 mm swivel-pad holder. The upper pad is 90 x 62 mm. Static states for 10, 25, 40, and 55 mm desks show complete nut engagement, knob clearance, correct pad contact, and zero fixture collision.

## Rig interface

Two independent 44 x 7 mm slots are centred at X=136, Y=32/52 mm. Clamp bolts are at Y=18/66 mm, so fastener patterns do not coincide. The clamp is removed for rig use.

## Originality and reference use

No reference solid, mesh, sketch, exterior, or coordinate set was reused. References contributed only engineering principles already established in the audit: two-sided bearing support, steel load paths, simple springing, stationary sensor/moving magnet, modular packaging, and the idea of later horizontal/vertical modules. All P1 proportions, parts, interfaces, sensor path, rig pattern, and clamp geometry were created for this project.

## Deliberate P1 limitations

- No load cell, hydraulic cylinder, damper, continuously adjustable lever angle, or final cosmetic shell.
- No claimed PETG safety factor or life rating.
- No exact spring specification before physical testing.
- No final PCB; Pro Micro and SS49E validate the architecture.
- The hub may need local support in the lever slot when printed on a bearing face.
- The commodity swivel-foot interface must be adapted after the purchased item is measured.
