# Material and printing notes

## Current filament estimate — engineering estimate only

No real printer/slicer profile was available when these figures were calculated. They use STL geometry, PETG density, six perimeter walls, six top/bottom layers, and a 50% planning infill. They exclude slicer-specific line overlap, flow, support, brim, purge, and failed prints.

| Print scope | Pieces | Current 50% estimate |
|---|---:|---:|
| Calibration batch | 8 | approximately 233 g |
| Mechanical core | 8 | approximately 435 g |
| Complete final prototype | 19 | approximately 685 g |
| All final parts plus coupons | 27 | approximately 918 g |
| All 27 plus 30% development/reprint reserve | 27 | approximately 1.19 kg |

The conservative stock recommendation is **2 kg of the same filament**. Please replace these planning figures with the actual slicer result from the real printer/profile.

## Why PETG was selected as the P1 baseline

P1 contains mechanically loaded pivot towers, bearing pockets, a spring anchor, clamp structures, and bolted joints. PETG was chosen as a common starting material because it usually provides a useful compromise between toughness, impact resistance, layer adhesion, availability, cost, and hobby-printer accessibility. It is generally less brittle in mechanical handling than ordinary PLA.

PETG is not automatically “the best,” and the design does not assume that choosing PETG guarantees durability. PETG can be more flexible than PLA, may string, is sensitive to profile and cooling choices, and can creep under sustained load. Dimensional fit and mechanical endurance still require coupon and physical testing.

## If a different material is available

| Material | Calibration coupons | Fit/form testing | Mechanically loaded P1 | Main concern for this prototype |
|---|---|---|---|---|
| PLA | Suitable | Suitable | Usable only as a clearly limited early structural trial | More brittle failure behavior; heat and sustained-load creep can invalidate long tests |
| PETG | Suitable | Suitable | Reasonable P1 baseline, pending testing | Flexibility, stringing, dimensional tuning, and sustained-load creep |
| ABS | Suitable after printer calibration | Suitable | Potentially reasonable | Shrinkage/warping can change bearing and bolt fits; enclosure, ventilation, and layer adhesion matter |
| ASA | Suitable after printer calibration | Suitable | Potentially reasonable | Similar shrink/warp and ventilation concerns to ABS; UV resistance is not important for this indoor P1 |
| Nylon / PA | Suitable only after drying and profile tuning | Suitable after tuning | Potentially very tough | Moisture sensitivity, dimensional variation, flexibility/creep, and harder printing; filled grades may require a hardened nozzle |
| Engineering or fibre-filled filament | Material-dependent | Material-dependent | May improve stiffness or heat behavior | Abrasive grades need suitable hardware; layer strength and manufacturer profile still control the result |

PLA is acceptable for the first calibration and fit work if that is what is available. If PLA is used for structural testing, report it clearly because the results will not directly validate the PETG baseline. A well-understood engineering filament may be better than PETG; please tell us exactly what material and grade is available rather than substituting silently.

## Build-volume check

The manifest lists the oriented envelope for every file. The largest print is the base, `P1-001_BASE.stl`, at approximately **180 x 84 x 10 mm** in the recommended orientation. It needs extra usable bed margin for skirt/brim and exclusion zones, so a nominal 180 mm bed axis may be too small.

Other large envelopes to check are:

- `COUPON_608_POCKETS_DEPTH_7.stl`: approximately 150 x 34 x 11 mm.
- `COUPON_608_POCKETS_DEPTH_14.stl`: approximately 150 x 34 x 18 mm.
- `P1-004_LEVER_ROOT_BEARING_HUB.stl`: approximately 124 x 64 x 28 mm when placed on a bearing face.
- `P1-021_CLAMP_VERTICAL_BRACKET.stl`: approximately 64 x 114 x 34 mm when placed on its large X face.
- `P1-006_GRIP.stl`: approximately 34 x 34 x 110 mm when printed upright.

A typical 220 x 220 x 250 mm printer should have sufficient nominal volume for each individual STL, but usable-area restrictions and slicer margins must be checked. Do not arrange all parts on one plate merely because they fit; the first actual print job is the eight calibration files only.

## Orientation and support review

`PRINT_FILE_MANIFEST.csv` records the existing P1 orientation guidance for every STL. Most parts were designed to minimize support. Please use slicer preview to verify bridges, overhangs, unsupported internal features, and layer direction before printing.

Pay particular attention to:

- `P1-004_LEVER_ROOT_BEARING_HUB.stl`: lever-slot bridge; use local support only if the printer cannot bridge it cleanly.
- `P1-010_MAGNET_HOLDER.stl`: magnet-cup area may need small local support.
- `P1-011A_HALL_FIXED_BRACKET.stl` and `P1-011B_HALL_SENSOR_SLED.stl`: inspect rail/bridge regions.
- `P1-006_GRIP.stl`: print upright as guided; a brim may be appropriate for stability.

Please report any orientation that looks mechanically weak, requires excessive support, or creates excessive print time. Support and brim material were not included in the engineering mass estimate.
