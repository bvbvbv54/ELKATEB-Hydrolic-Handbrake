# P1 changelog

## P1.0-H — 2026-09-26 — exports and verification

- Exported individual STEP/STL parts, assembly/motion/clamp-state STEP files, DXF steel templates, SVG drawings, calculations, machine-readable checks, and 19 renders.
- Round-trip verified 90 files with zero failures; all STLs watertight and all DXFs millimetre-unit.

## P1.0-G — assembly validation

- Verified 75°, 62.5°, and 50° states with no unintended moving/fixed intersections.
- Verified 10/25/40/55 mm desk states, full coupling-nut engagement, knob clearance, and pad contact.
- Confirmed spring length increases 69.76 -> 77.97 -> 85.82 mm.

## P1.0-F — electronics enclosure

- Moved the 50 x 38 x 28 mm removable enclosure into the rear-right bay to eliminate spring-module overlap.
- Added USB opening, Hall cable route, cover, and board envelope.

## P1.0-E — Hall architecture

- Rejected the initial midpoint sensor layout because it could create non-monotonic magnetic distance.
- Moved magnet to 55 mm radius and sensor to the full-pull endpoint.
- Eliminated a detected full-pull magnet-carrier/right-tower interference without notching the structural tower.

## P1.0-D — desk clamp

- Created six clamp parts around a real M10 coupling nut and M10x100 screw candidate.
- Changed overlapping lap joints to non-overlapping butt joints with M6 through-bolts.

## P1.0-C — lever, spring, and stops

- Added drilled 25 x 5 x 280 mm steel lever, printed grip, three-position fixed spring anchor, moving steel anchor, arc-guided M6 stop pin, and two adjustable stop blocks.

## P1.0-B — pivot system

- Added paired towers, 28 mm hub, two open 608 pockets, M8 bore, washers, 13.6 mm inner-race spacer, and removable M8x90 pivot candidate.

## P1.0-A — master skeleton

- Established tagged central parameters, 180 x 84 x 10 mm base, independent rig slots, clamp interface, and two recessed steel backing strips.
