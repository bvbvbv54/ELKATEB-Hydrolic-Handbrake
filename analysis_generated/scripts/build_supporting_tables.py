#!/usr/bin/env python3
"""Write curated, evidence-linked measurement and hardware candidate tables."""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "analysis_generated"

MEAS_FIELDS = [
    "model", "category", "measurement", "value", "unit", "confidence",
    "geometry_source", "source_path", "method", "notes",
]


def m(model, category, measurement, value, unit, confidence, source, path, method, notes=""):
    return dict(zip(MEAS_FIELDS, [model, category, measurement, value, unit, confidence, source, path, method, notes]))


measurements = [
    m("Chinese generic", "overall", "overall dimensions", "UNKNOWN", "mm", "UNKNOWN", "SLDASM embedded preview only", "chinese-generic-sim-handbrake-model-1.snapshot.1/Chinese handbrake assembly.SLDASM", "No proprietary SolidWorks B-Rep reader available", "Do not infer dimensions from thumbnail or filenames."),
    m("Chinese generic", "parts", "unique SLDPRT definitions", 32, "count", "VERIFIED", "filesystem", "chinese-generic-sim-handbrake-model-1.snapshot.1", "file inventory", "Includes 15 filename-identified fastener/nut/washer definitions and 17 product-specific definitions."),
    m("Chinese generic", "assemblies", "SLDASM definitions", 4, "count", "VERIFIED", "filesystem", "chinese-generic-sim-handbrake-model-1.snapshot.1", "file inventory", "Main, handle, PCB, and yoke assemblies."),

    m("Fanatec reference", "overall", "down configuration bounding box", "424.000 x 64.687 x 118.000", "mm", "VERIFIED", "STEP B-Rep", "fanatec-handbrake-1.snapshot.1/FANATEC Handbrake down.step", "OpenCascade exact B-Rep bounding box"),
    m("Fanatec reference", "overall", "up configuration bounding box", "213.373 x 64.687 x 328.627", "mm", "VERIFIED", "STEP B-Rep", "fanatec-handbrake-1.snapshot.1/FANATEC Handbrake up.step", "OpenCascade exact B-Rep bounding box"),
    m("Fanatec reference", "base", "base envelope", "154.000 x 61.500 x 76.000", "mm", "VERIFIED", "STEP B-Rep solids 3-4", "fanatec-handbrake-1.snapshot.1/FANATEC Handbrake down.step", "union bounding range of unchanged base solids"),
    m("Fanatec reference", "lever", "lever plate thickness", 4.000, "mm", "VERIFIED", "STEP B-Rep solid 2", "fanatec-handbrake-1.snapshot.1/FANATEC Handbrake down.step", "minimum lever-solid bounding extent aligned with global Y"),
    m("Fanatec reference", "handle", "grip envelope", "106.000 x 42.375 x 42.375", "mm", "VERIFIED", "STEP B-Rep solid 1", "fanatec-handbrake-1.snapshot.1/FANATEC Handbrake down.step", "solid bounding box"),
    m("Fanatec reference", "pivot", "concentric candidate diameters", "7 / 8 / 12", "mm", "VERIFIED", "STEP cylindrical faces", "fanatec-handbrake-1.snapshot.1/FANATEC Handbrake down.step", "B-Rep cylindrical surfaces at x=148, z=20.953", "Candidate pivot/boss sizes; exact hardware standard not documented."),
    m("Fanatec reference", "lever", "pivot to grip centroid", "about 224", "mm", "DERIVED", "STEP B-Rep", "fanatec-handbrake-1.snapshot.1/FANATEC Handbrake down.step", "distance from candidate pivot axis to grip solid center of mass", "Approximate hand position, not physical travel."),
    m("Fanatec reference", "parts", "disjoint solids", 4, "count", "VERIFIED", "STEP B-Rep", "fanatec-handbrake-1.snapshot.1/FANATEC Handbrake down.step", "topology traversal", "Not a verified manufacturing BOM; internals are omitted."),

    m("DIY v1.2", "overall", "assembly bounding box", "165.611 x 84.090 x 302.591", "mm", "VERIFIED", "STEP B-Rep", "handbrake-for-sim-racing-diy-1.snapshot.48/STEP and Parasolid/hand brake v1.2.stp", "OpenCascade exact B-Rep bounding box", "Drawing HB3 independently shows 163.24 x 81.06 x 302.57 mm, excluding some protrusions."),
    m("DIY v1.2", "lever", "printed handle envelope", "26.000 x 20.000 x 122.000", "mm", "VERIFIED", "STEP occurrence handle", "handbrake-for-sim-racing-diy-1.snapshot.48/STEP and Parasolid/hand brake v1.2.stp", "XCAF occurrence bounding box"),
    m("DIY v1.2", "lever", "handle length called out", 116.9, "mm", "VERIFIED", "package drawing image", "handbrake-for-sim-racing-diy-1.snapshot.48/HB3.bmp", "drawing annotation"),
    m("DIY v1.2", "pivot", "primary bearing-axis center", "x=17.000, z=43.429", "mm", "VERIFIED", "STEP XCAF F696ZZ occurrences", "handbrake-for-sim-racing-diy-1.snapshot.48/STEP and Parasolid/hand brake v1.2.stp", "center of paired bearing bounding boxes; assembly Y axis omitted"),
    m("DIY v1.2", "pivot", "secondary bearing-axis center", "x about 97.97, z about 54.8", "mm", "VERIFIED", "STEP XCAF F696ZZ occurrences", "handbrake-for-sim-racing-diy-1.snapshot.48/STEP and Parasolid/hand brake v1.2.stp", "center of paired bearing bounding boxes"),
    m("DIY v1.2", "bearing", "F696ZZ modeled size", "ID 6 / OD 15 / flange OD 17 / width 5", "mm", "VERIFIED", "STEP B-Rep named F696ZZ occurrences", "handbrake-for-sim-racing-diy-1.snapshot.48/STEP and Parasolid/hand brake v1.2.stp", "cylindrical surfaces and occurrence width", "BOM explicitly names F696ZZ; overall rotated bbox reaches about 18.4 mm."),
    m("DIY v1.2", "side plates", "hbplate2 thickness", 3.000, "mm", "VERIFIED", "STEP XCAF occurrence", "handbrake-for-sim-racing-diy-1.snapshot.48/STEP and Parasolid/hand brake v1.2.stp", "bounding extent along Y"),
    m("DIY v1.2", "side plates", "hbplate2 inner spacing", 26.000, "mm", "DERIVED", "STEP XCAF paired occurrences", "handbrake-for-sim-racing-diy-1.snapshot.48/STEP and Parasolid/hand brake v1.2.stp", "39.171 - 13.171"),
    m("DIY v1.2", "side plates", "hbplate2 outer spacing", 32.000, "mm", "DERIVED", "STEP XCAF paired occurrences", "handbrake-for-sim-racing-diy-1.snapshot.48/STEP and Parasolid/hand brake v1.2.stp", "42.171 - 10.171"),
    m("DIY v1.2", "lever", "primary pivot to handle centroid", 182.43, "mm", "DERIVED", "STEP XCAF", "handbrake-for-sim-racing-diy-1.snapshot.48/STEP and Parasolid/hand brake v1.2.stp", "Euclidean distance from primary bearing center to handle center of mass"),
    m("DIY v1.2", "sensor", "sensor-board assembly envelope", "12.616 x 3.116 x 54.016", "mm", "VERIFIED", "STEP named occurrence", "handbrake-for-sim-racing-diy-1.snapshot.48/STEP and Parasolid/hand brake v1.2.stp", "XCAF occurrence bounding box; includes components, not bare PCB outline"),
    m("DIY v1.2", "sensor", "magnet nominal size", "5 x 4 x 2", "mm", "VERIFIED", "package hardware-list image", "handbrake-for-sim-racing-diy-1.snapshot.48/Cutting; flexion; electronics and information/fasteners and accessories.png", "BOM row 19", "STEP magnet solid volume 38.19 mm^3 is consistent with nominal 40 mm^3."),
    m("DIY v1.2", "sensor", "magnet-holder STL envelope", "15.200 x 15.198 x 10.000", "file units, validated as mm", "VERIFIED", "STL cross-checked to STEP", "handbrake-for-sim-racing-diy-1.snapshot.48/Cutting; flexion; electronics and information/printed parts/magnet holder.stl", "trimesh bounds and STEP volume/size comparison"),
    m("DIY v1.2", "sheet metal", "cut sheet thickness", 3.000, "mm", "VERIFIED", "folder/documentation and STEP occurrences", "handbrake-for-sim-racing-diy-1.snapshot.48/Cutting; flexion; electronics and information/сutting 3mm", "folder title plus repeated 3.000 mm B-Rep plate extents"),
    m("DIY v1.2", "parts", "assembly occurrences", 90, "count", "VERIFIED", "STEP XCAF", "handbrake-for-sim-racing-diy-1.snapshot.48/STEP and Parasolid/hand brake v1.2.stp", "top-level component occurrence count"),
    m("DIY v1.2", "printed parts", "unique STL files", 10, "count", "VERIFIED", "filesystem/STL", "handbrake-for-sim-racing-diy-1.snapshot.48/Cutting; flexion; electronics and information/printed parts", "file inventory"),
    m("DIY v1.2", "sheet metal", "nested plate pieces", 10, "count", "VERIFIED", "PDF fabrication sheet", "handbrake-for-sim-racing-diy-1.snapshot.48/Cutting; flexion; electronics and information/сutting 3mm/hand brake v1.1 info.pdf", "drawing table totals"),

    m("Hydraulic", "overall", "assembly bounding box", "92.245 x 263.761 x 409.983", "mm", "VERIFIED", "STEP B-Rep", "hydraulic-handbrake-1.snapshot.2/Handbrake.stp", "OpenCascade exact B-Rep bounding box"),
    m("Hydraulic", "base", "Osnova envelope", "52.000 x 64.000 x 165.000", "mm", "VERIFIED", "STEP named occurrence", "hydraulic-handbrake-1.snapshot.2/Handbrake.stp", "XCAF occurrence bounding box"),
    m("Hydraulic", "base", "sheet thickness", 2.300, "mm", "VERIFIED", "package drawing image and STEP", "hydraulic-handbrake-1.snapshot.2/Handbrake/Web/osnova1.jpg", "drawing callout; matching UhoStoper 2.3 mm B-Rep thickness"),
    m("Hydraulic", "base", "derived inner side-wall spacing", 47.400, "mm", "DERIVED", "drawing", "hydraulic-handbrake-1.snapshot.2/Handbrake/Web/osnova1.jpg", "52.0 outer width - 2 x 2.3 sheet thickness"),
    m("Hydraulic", "lever", "Arm2 local part envelope", "289.980 x 83.498 x 8.000", "mm", "VERIFIED", "IGES neutral part", "hydraulic-handbrake-1.snapshot.2/Handbrake/IGS/Arm2.IGS", "OpenCascade B-Rep/surface bounding box"),
    m("Hydraulic", "lever", "Arm2 plate thickness", 8.000, "mm", "VERIFIED", "STEP/IGES B-Rep", "hydraulic-handbrake-1.snapshot.2/Handbrake.stp", "named occurrence minimum extent"),
    m("Hydraulic", "pivot", "Shtift shaft envelope", "27.000 x 8.000 x 8.000", "mm", "VERIFIED", "STEP named occurrence", "hydraulic-handbrake-1.snapshot.2/Handbrake.stp", "XCAF occurrence bounding box"),
    m("Hydraulic", "pivot", "Durjach flanged-bushing candidates", "8 bore / 16 neck / 32 flange", "mm", "VERIFIED", "STEP cylindrical faces", "hydraulic-handbrake-1.snapshot.2/Handbrake.stp", "named occurrence surfaces", "Custom-looking flanged parts; material/tolerance not documented."),
    m("Hydraulic", "pivot", "pivot axis center", "x=22.266, y=68.682, z=142.951", "mm", "VERIFIED", "STEP Shtift occurrence", "hydraulic-handbrake-1.snapshot.2/Handbrake.stp", "center of shaft occurrence bounding box"),
    m("Hydraulic", "lever", "pivot to grip center of mass", 203.72, "mm", "DERIVED", "STEP named occurrences", "hydraulic-handbrake-1.snapshot.2/Handbrake.stp", "Euclidean distance from Shtift axis center to Rukohvatka center of mass"),
    m("Hydraulic", "parts", "assembly occurrences", 14, "count", "VERIFIED", "STEP XCAF", "hydraulic-handbrake-1.snapshot.2/Handbrake.stp", "top-level component occurrence count"),

    m("MOZA low-poly", "overall", "STEP bounding box", "67.000 x 152.000 x 319.331", "mm", "VERIFIED", "STEP B-Rep", "moza-hbp-handbrake-low-poly-1.snapshot.1/MOZA HBP Handbrake Low Poly.step", "OpenCascade exact B-Rep bounding box"),
    m("MOZA low-poly", "overall", "STL bounding box", "67.000 x 152.000 x 319.331", "file units, validated as mm", "VERIFIED", "STL cross-checked to STEP", "moza-hbp-handbrake-low-poly-1.snapshot.1/MOZA HBP Handbrake Low Poly.stl", "trimesh bounds equal STEP bounds"),
    m("MOZA low-poly", "parts", "STEP solids / STL components", "1 / 1", "count", "VERIFIED", "STEP and STL", "moza-hbp-handbrake-low-poly-1.snapshot.1", "B-Rep topology and welded mesh split", "Single fused low-poly exterior, not a manufacturing assembly."),
]

HW_FIELDS = ["model", "candidate", "quantity", "evidence_status", "evidence", "source_path", "audit_comment"]
hardware = [
    ["Chinese generic", "M8 fastener family", "multiple / occurrence count unknown", "VERIFIED filenames; geometry UNKNOWN", "8 mm bolts, nuts, washers named in files", "chinese-generic-sim-handbrake-model-1.snapshot.1", "Do not order from filename evidence alone; assembly quantities and fit are unavailable."],
    ["Chinese generic", "M5 and M3 fasteners", "multiple / occurrence count unknown", "VERIFIED filenames; geometry UNKNOWN", "M5/M3 hardware part definitions", "chinese-generic-sim-handbrake-model-1.snapshot.1", "Quantities unknown."],
    ["Fanatec reference", "7/8/12 mm concentric pivot/boss features", "candidate only", "VERIFIED geometry", "STEP cylindrical faces", "fanatec-handbrake-1.snapshot.1/FANATEC Handbrake down.step", "No BOM; do not equate these automatically to a specific bearing or bolt."],
    ["DIY v1.2", "F696ZZ flanged bearing (6 x 15 x 5 mm, 17 mm flange OD)", 4, "VERIFIED", "BOM name/quantity and STEP named occurrences", "handbrake-for-sim-racing-diy-1.snapshot.48", "Strong reference for compact paired pivots; less common than 608."],
    ["DIY v1.2", "M6 DIN 912 socket-head screws", "14 across 12/16/35/40/55 mm lengths", "VERIFIED BOM image", "rows 1-5", "handbrake-for-sim-racing-diy-1.snapshot.48/Cutting; flexion; electronics and information/fasteners and accessories.png", "STEP occurrence names corroborate several lengths."],
    ["DIY v1.2", "M8 socket/hex screws", "2 documented plus M8x170 modeled shaft", "CONFLICT", "BOM says M8x45 and M8x55; STEP names M8x40 and M8X170", "handbrake-for-sim-racing-diy-1.snapshot.48", "Physically verify before ordering."],
    ["DIY v1.2", "DIN 985 M6 nyloc nuts", 11, "VERIFIED documentation", "hardware-list image", "handbrake-for-sim-racing-diy-1.snapshot.48/Cutting; flexion; electronics and information/fasteners and accessories.png", ""],
    ["DIY v1.2", "PHS8 rod end", 1, "VERIFIED", "BOM and STEP named occurrence", "handbrake-for-sim-racing-diy-1.snapshot.48", "Adds cost and complexity; not recommended for P1."],
    ["DIY v1.2", "compression spring 20 x 51 light", 1, "VERIFIED documentation", "hardware-list image", "handbrake-for-sim-racing-diy-1.snapshot.48/Cutting; flexion; electronics and information/fasteners and accessories.png", "Spring rate/preload are not documented."],
    ["DIY v1.2", "magnet 5 x 4 x 2 mm", 1, "VERIFIED documentation", "hardware-list image; STEP volume corroboration", "handbrake-for-sim-racing-diy-1.snapshot.48", "Works with AS5600 arrangement; magnet grade/polarization is undocumented."],
    ["DIY v1.2", "AS5600-ASOT sensor PCB", 1, "VERIFIED documentation", "PCB BOM", "handbrake-for-sim-racing-diy-1.snapshot.48/Cutting; flexion; electronics and information/electronics/AS5600_analog_pcb/BOM_PCB_AS5600_pcb.csv", "PCB BOM says C2=10uF while pick-and-place comment says C2=1uF; resolve before fabrication."],
    ["Hydraulic", "8 x 27 mm pivot pin", 1, "VERIFIED geometry", "named Shtift occurrence", "hydraulic-handbrake-1.snapshot.2/Handbrake.stp", "Appears custom; a standard M8 shoulder/part-thread bolt is preferable for P1."],
    ["Hydraulic", "custom flanged bushings", 2, "VERIFIED geometry", "two Durjach occurrences", "hydraulic-handbrake-1.snapshot.2/Handbrake.stp", "8 mm bore, 16 mm neck, 32 mm flange; not a cheap off-the-shelf choice unless a matching bushing is sourced."],
    ["Hydraulic", "hydraulic cylinder/piston/link", "1 set", "VERIFIED geometry", "PompaTqlo, Butalo, ArmButalo occurrences", "hydraulic-handbrake-1.snapshot.2/Handbrake.stp", "Major cost and fabrication driver; reject for P1."],
    ["MOZA low-poly", "hardware", "UNKNOWN", "UNKNOWN", "No recoverable component structure", "moza-hbp-handbrake-low-poly-1.snapshot.1", "Do not infer BOM from exterior low-poly body."],
]


def write_csv(path: Path, fields, rows):
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for row in rows:
            w.writerow(row if isinstance(row, dict) else dict(zip(fields, row)))


write_csv(OUT / "measurements.csv", MEAS_FIELDS, measurements)
write_csv(OUT / "hardware_candidates.csv", HW_FIELDS, hardware)
print(f"Wrote {len(measurements)} measurements and {len(hardware)} hardware rows")
