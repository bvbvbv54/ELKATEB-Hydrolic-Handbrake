# P1 sim-racing handbrake — print check for Amine

This is the first mechanical prototype of a sim-racing handbrake.

## Please do not print everything yet

There are **27 STL files** in four folders:

- `01_CALIBRATION_FIRST/`: 8 calibration pieces — this is the only batch to print first.
- `02_MECHANICAL_CORE_AFTER_CALIBRATION/`: 8 structural parts — inspect now, but wait before printing.
- `03_SENSOR_AND_ELECTRONICS/`: 5 parts — inspect now, but wait before printing.
- `04_TABLE_CLAMP/`: 6 parts — inspect now, but wait before printing.

Please load all 27 STLs into your normal slicer to check fit, orientation, support, and total filament. The current mass numbers are engineering estimates only; your slicer result with your real printer and filament profile is the number we need.

## Current design baseline

- Material: PETG
- Nozzle: 0.4 mm
- Layer height: 0.20 mm
- Walls/perimeters: 5–6
- Top layers: 6
- Bottom layers: 6
- Planning infill: 50%

These are starting settings, not mandatory. Please tell us if your printer/profile needs something different.

## Please report back

```text
PRINTER MODEL:
SLICER + VERSION:
NOZZLE:
MATERIAL:
FILAMENT BRAND:
FILAMENT TYPE/GRADE:
AVAILABLE FILAMENT MASS:
BUILD VOLUME (X x Y x Z):

SLICER MASS — 8 CALIBRATION PARTS:
SLICER MASS — 8 MECHANICAL-CORE PARTS:
SLICER MASS — 19 FINAL PARTS:
SLICER MASS — ALL 27 FILES:

PARTS THAT DO NOT FIT:
PARTS NEEDING SUPPORT:
PARTS NEEDING A BRIM:
ORIENTATION CHANGES YOU RECOMMEND:
SETTING CHANGES YOU RECOMMEND:
OTHER SLICER/PREVIEW CONCERNS:
```

Please inspect the bridge/support risk on `P1-004`, `P1-010`, `P1-011A`, and `P1-011B`. The upright grip `P1-006` may need a brim.

After the eight coupons are printed and measured, some fit-dependent dimensions may change and regenerated structural STLs may be sent. That is why the other 19 parts should not be printed yet.
