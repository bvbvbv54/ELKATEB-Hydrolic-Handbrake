# P1.0 Print Material Estimate

## Executive result

The released P1.0 deliverables contain **27 unique STL files at quantity one**: **8 calibration coupons** and **19 final structural/accessory components**. The 19 final components divide into **8 mechanical-core parts**, **5 sensor/electronics parts**, and **6 desk-clamp parts**. No CAD or STL file was modified for this report.

All 27 meshes load as watertight, consistently oriented, single-component solids. Pre-existing P1.0 manifest hash match: **27/27**.

## Method and limitations

- **Exact solid CAD/STL volume:** calculated directly from each released binary STL triangle mesh with trimesh after normal mesh processing. This is the closed tessellated-solid volume, not deposited filament volume.
- **Practical FDM estimate:** no PrusaSlicer, OrcaSlicer, CuraEngine, or Bambu Studio command-line executable was found in PATH or common installation locations, and no printer/profile was supplied. The values below are therefore an **engineering estimate, not slicer output**.
- Baseline: PETG density 1.27 g/cm3, 0.40 mm nozzle, 0.20 mm layers, 6 perimeters, 6 top layers, 6 bottom layers, and an explicit 0.45 mm assumed extrusion width.
- Shell model: directional STL surface area x 2.70 mm perimeter envelope plus projected top/bottom area x 1.20 mm skin envelope. It does not subtract edge overlap and is capped at exact solid volume, so it is intentionally conservative for purchasing. The remaining internal volume receives 40%, 50%, or 60% infill.
- Estimated mass excludes support, brim, skirt, purge/prime lines, extrusion multiplier differences, gap fill, slicer line overlap, failed prints, and moisture-conditioning losses. Support statements are orientation guidance only and were not calculated by a slicer.
- **Print time: UNKNOWN** because neither a slicer result nor a printer/machine profile is available.

Bounding dimensions are native STL X x Y x Z extents in millimetres; the recommended build orientation may rotate them on the printer.

## Piece-count verification

| Category | Unique STLs | Physical pieces |
|---|---:|---:|
| A. Calibration coupons | 8 | 8 |
| B. Mechanical core | 8 | 8 |
| C. Sensor/electronics printed parts | 5 | 5 |
| D. Desk-clamp printed parts | 6 | 6 |
| **Final components (B+C+D)** | **19** | **19** |
| **Complete set (A+B+C+D)** | **27** | **27** |

## A. Calibration coupons

| Part ID | STL filename | Qty | Bounding X x Y x Z (mm) | Exact volume (cm3) | 100% solid mass (g) | Est. 40% (g) | Est. 50% (g) | Est. 60% (g) | Recommended orientation | Likely support requirement |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| CAL-608-07 | `COUPON_608_POCKETS_DEPTH_7.stl` | 1 | 150.0 x 34.0 x 11.0 | 39.95 | 50.7 | 44.0 | 45.1 | 46.2 | Flat base on bed; 7 mm pockets upward | No support expected; not slicer-verified |
| CAL-608-14 | `COUPON_608_POCKETS_DEPTH_14.stl` | 1 | 150.0 x 34.0 x 18.0 | 59.51 | 75.6 | 65.2 | 66.9 | 68.7 | Flat base on bed; 14 mm pockets upward | No support expected; not slicer-verified |
| CAL-M8 | `COUPON_M8_CLEARANCE.stl` | 1 | 72.0 x 24.0 x 8.0 | 12.09 | 15.4 | 13.8 | 14.0 | 14.3 | Flat base on bed; test bores vertical | No support expected; not slicer-verified |
| CAL-M6 | `COUPON_M6_CLEARANCE.stl` | 1 | 72.0 x 24.0 x 8.0 | 12.83 | 16.3 | 13.9 | 14.3 | 14.7 | Flat base on bed; test bores vertical | No support expected; not slicer-verified |
| CAL-M6-NUT | `COUPON_M6_NUT_TRAPS.stl` | 1 | 80.0 x 26.0 x 8.0 | 14.80 | 18.8 | 16.3 | 16.7 | 17.1 | Largest flat face on bed; nut traps upward | No support expected; not slicer-verified |
| CAL-MAG | `COUPON_MAGNET_POCKETS.stl` | 1 | 70.0 x 22.0 x 7.0 | 10.15 | 12.9 | 11.4 | 11.6 | 11.9 | Largest flat face on bed; pockets upward | No support expected; not slicer-verified |
| CAL-HALL | `COUPON_HALL_GAP_JIG.stl` | 1 | 104.0 x 35.0 x 18.0 | 19.40 | 24.6 | 24.6 | 24.6 | 24.6 | Largest flat face on bed | No support expected; not slicer-verified |
| CAL-BEAR-WALL | `COUPON_LOADED_BEARING_WALL.stl` | 1 | 79.0 x 20.0 x 48.0 | 42.05 | 53.4 | 36.9 | 39.6 | 42.4 | Broad side face on bed; bearing axis horizontal | No support expected; not slicer-verified |

## B. Mechanical core

| Part ID | STL filename | Qty | Bounding X x Y x Z (mm) | Exact volume (cm3) | 100% solid mass (g) | Est. 40% (g) | Est. 50% (g) | Est. 60% (g) | Recommended orientation | Likely support requirement |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| P1-001 | `P1-001_BASE.stl` | 1 | 180.0 x 84.0 x 10.0 | 114.03 | 144.8 | 107.0 | 113.3 | 119.6 | Primary flat face on bed; steel recesses upward | No support expected; not slicer-verified |
| P1-002 | `P1-002_LEFT_PIVOT_SUPPORT.stl` | 1 | 56.0 x 18.0 x 93.0 | 65.56 | 83.3 | 56.3 | 60.8 | 65.3 | Outer Y face on bed | No support expected; ream holes after printing |
| P1-003 | `P1-003_RIGHT_PIVOT_SUPPORT.stl` | 1 | 56.0 x 18.0 x 93.0 | 68.85 | 87.4 | 55.6 | 60.9 | 66.2 | Outer Y face on bed | No support expected; not slicer-verified |
| P1-004 | `P1-004_LEVER_ROOT_BEARING_HUB.stl` | 1 | 124.0 x 28.0 x 64.0 | 103.15 | 131.0 | 89.6 | 96.5 | 103.4 | One bearing face on bed | Conditional local support in accessible lever slot if bridging is poor |
| P1-006 | `P1-006_GRIP.stl` | 1 | 110.0 x 34.0 x 34.0 | 83.56 | 106.1 | 82.8 | 86.7 | 90.5 | Upright on end with brim | No support expected; brim material is excluded |
| P1-007 | `P1-007_SPRING_ANCHOR_MODULE.stl` | 1 | 40.0 x 24.0 x 22.0 | 10.48 | 13.3 | 13.3 | 13.3 | 13.3 | Foot on bed | No support expected; not slicer-verified |
| P1-008 | `P1-008_RELEASE_STOP.stl` | 1 | 18.7 x 8.0 x 22.9 | 1.50 | 1.9 | 1.9 | 1.9 | 1.9 | Outer Y face on bed | No support expected; not slicer-verified |
| P1-009 | `P1-009_FULL_PULL_STOP.stl` | 1 | 23.6 x 8.0 x 24.3 | 1.50 | 1.9 | 1.9 | 1.9 | 1.9 | Outer Y face on bed | No support expected; not slicer-verified |

## C. Sensor/electronics printed parts

| Part ID | STL filename | Qty | Bounding X x Y x Z (mm) | Exact volume (cm3) | 100% solid mass (g) | Est. 40% (g) | Est. 50% (g) | Est. 60% (g) | Recommended orientation | Likely support requirement |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| P1-010 | `P1-010_MAGNET_HOLDER.stl` | 1 | 22.4 x 12.0 x 43.0 | 2.88 | 3.7 | 3.7 | 3.7 | 3.7 | Inner arm face on bed | Conditional small local support at magnet cup |
| P1-011A | `P1-011A_HALL_FIXED_BRACKET.stl` | 1 | 31.0 x 15.0 x 35.0 | 3.54 | 4.5 | 4.5 | 4.5 | 4.5 | Largest flat face on bed | Conditional; inspect rail bridges in slicer |
| P1-011B | `P1-011B_HALL_SENSOR_SLED.stl` | 1 | 14.0 x 8.6 x 22.0 | 1.18 | 1.5 | 1.5 | 1.5 | 1.5 | Largest flat face on bed | Conditional; inspect rail bridges in slicer |
| P1-012 | `P1-012_ELECTRONICS_ENCLOSURE.stl` | 1 | 50.0 x 38.0 x 28.0 | 14.21 | 18.0 | 18.0 | 18.0 | 18.0 | Enclosure bottom on bed | No support expected; not slicer-verified |
| P1-013 | `P1-013_ELECTRONICS_COVER.stl` | 1 | 50.0 x 38.0 x 5.0 | 8.36 | 10.6 | 9.7 | 9.8 | 10.0 | Outer top face on bed | No support expected; not slicer-verified |

## D. Desk-clamp printed parts

| Part ID | STL filename | Qty | Bounding X x Y x Z (mm) | Exact volume (cm3) | 100% solid mass (g) | Est. 40% (g) | Est. 50% (g) | Est. 60% (g) | Recommended orientation | Likely support requirement |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| P1-020 | `P1-020_CLAMP_BASE_INTERFACE.stl` | 1 | 64.0 x 72.0 x 8.0 | 35.23 | 44.7 | 32.3 | 34.4 | 36.4 | Large face on bed | No support expected; not slicer-verified |
| P1-021 | `P1-021_CLAMP_VERTICAL_BRACKET.stl` | 1 | 34.0 x 64.0 x 114.0 | 78.80 | 100.1 | 66.4 | 72.0 | 77.6 | Large X face on bed; ribs upward | No support expected; not slicer-verified |
| P1-022 | `P1-022_CLAMP_SCREW_GUIDE.stl` | 1 | 76.0 x 32.0 x 38.0 | 44.68 | 56.7 | 43.0 | 45.3 | 47.6 | Lower arm face on bed; hex pocket vertical | No support expected; not slicer-verified |
| P1-023 | `P1-023_CLAMP_KNOB.stl` | 1 | 52.0 x 47.2 x 18.0 | 27.18 | 34.5 | 25.6 | 27.1 | 28.6 | Flat face on bed | No support expected; not slicer-verified |
| P1-024 | `P1-024_SWIVEL_PAD_HOLDER.stl` | 1 | 46.0 x 46.0 x 8.0 | 11.59 | 14.7 | 12.0 | 12.4 | 12.9 | Flat face on bed | No support expected; not slicer-verified |
| P1-025 | `P1-025_UPPER_RUBBER_PAD_HOLDER.stl` | 1 | 90.0 x 62.0 x 3.0 | 16.50 | 21.0 | 20.9 | 20.9 | 20.9 | Large face on bed | No support expected; not slicer-verified |

## Category and build-stage totals

| Scope | Pieces | Exact solid volume (cm3) | 100% solid mass (g) | Est. 40% (g) | Est. 50% (g) | Est. 60% (g) |
|---|---:|---:|---:|---:|---:|---:|
| Calibration coupons | 8 | 210.78 | 267.7 | 226.0 | 233.0 | 239.9 |
| Mechanical core | 8 | 448.63 | 569.8 | 408.4 | 435.3 | 462.2 |
| Sensor/electronics printed parts | 5 | 30.17 | 38.3 | 37.4 | 37.5 | 37.7 |
| Desk-clamp printed parts | 6 | 213.98 | 271.8 | 200.1 | 212.0 | 224.0 |
| All final P1 printed components (B+C+D) | 19 | 692.78 | 879.8 | 645.8 | 684.8 | 723.8 |
| Complete print set including coupons (A+B+C+D) | 27 | 903.56 | 1147.5 | 871.8 | 917.8 | 963.7 |

## Filament reserve

Reserve calculations use the same estimated deposited mass. A `+15%` allowance is reasonable for normal handling, short test extrusions, and small slicer differences; `+30%` is the development/reprint allowance requested for P1.

### All 19 final components

| Infill | Theoretical printed mass (g) | +15% reserve (g) | +30% development reserve (g) | Safe 1 kg spools |
|---:|---:|---:|---:|---:|
| 40% | 645.8 | 742.7 | 839.6 | 1 |
| 50% | 684.8 | 787.6 | 890.3 | 1 |
| 60% | 723.8 | 832.4 | 941.0 | 1 |

### Complete set: final components plus 8 coupons

| Infill | Theoretical printed mass (g) | +15% reserve (g) | +30% development reserve (g) | Safe 1 kg spools |
|---:|---:|---:|---:|---:|
| 40% | 871.8 | 1002.6 | 1133.4 | 2 |
| 50% | 917.8 | 1055.5 | 1193.1 | 2 |
| 60% | 963.7 | 1108.3 | 1252.9 | 2 |

For sending the job to a friend, **50% infill is the central planning case**. At that case, the complete 27-piece set plus 30% development reserve requires 1193.1 g, so have **2 x 1 kg spool(s)** of the same PETG lot available. This is a stock recommendation, not a claim that all of it will be consumed.

## Practical print sequence

1. **Initially:** print the 8 calibration coupons, approximately **233 g** at the 50% planning case.
2. **After calibration:** print the 8 mechanical-core parts, approximately **435 g** at 50%.
3. Print the 5 sensor/electronics parts and 6 clamp parts after fit and motion checks. The complete final 19-part prototype is approximately **685 g** at 50%.
4. Before each batch, rotate parts to the stated orientation and inspect unsupported bridges, hole orientation, brim need, and generated support in the actual slicer. Use the slicer's own mass result as the final purchasing/production number.

## Simple summary to send to the printer owner

> Initially: 8 calibration pieces / approximately 233 g PETG at 50% infill.  
> After calibration: 8 mechanical-core pieces / approximately 435 g PETG at 50% infill.  
> Complete prototype: 19 final printed pieces / approximately 685 g PETG at 50% infill.  
> Recommended filament to have available: 2 kg PETG (covers all 27 prints and a 30% development/reprint reserve).

## Machine-readable data

`print_material_estimate.csv` contains one row per STL followed by category/final/complete summary rows. It includes SHA-256 evidence, mesh integrity, exact volume, 100%-solid equivalent mass, directional shell estimate, 40/50/60% estimates, orientation, and support guidance.
