# Hand Brake Reference CAD Engineering Audit

**Audit date:** 2026-09-26  
**Scope:** read-only investigation of five extracted reference packages; no source CAD changed and no new product CAD created.  
**Primary machine-readable evidence:** `analysis_generated/model_inventory.csv`, `analysis_generated/measurements.csv`, `analysis_generated/hardware_candidates.csv`, and `analysis_generated/geometry_findings.json`.

## Evidence and confidence rules

- **VERIFIED** - read directly from documentation or measured from neutral CAD/mesh geometry by a real parser.
- **DERIVED** - calculated from VERIFIED values; the calculation is identified.
- **ESTIMATED** - visual/engineering interpretation that is not a defined CAD dimension.
- **UNKNOWN** - unavailable from the supplied evidence or the available tools.

The audit used OpenCascade 7.9.3.1 for STEP/IGES B-Rep import, XCAF for STEP occurrence names, `trimesh` for STL integrity, `ezdxf` for DXF entities/units, `olefile` for SolidWorks container metadata and embedded previews, and Poppler/PyPDF for the fabrication PDF. No proprietary SolidWorks B-Rep reader was available. Therefore, the Chinese generic `.SLDPRT`/`.SLDASM` geometry was **not** dimensionally analyzed. Embedded SolidWorks preview PNGs are treated as visual metadata, never as dimensional CAD evidence.

## 1. Executive summary

Do **not** print any complete reference package immediately.

- The **DIY v1.2** package is the strongest engineering reference and the closest mechanical starting point. It supplies a valid 139-solid STEP assembly with 90 named occurrences, mm DXFs, ten watertight printed parts, a fabrication PDF, hardware list, and an AS5600 sensor PCB. Its best principles are paired side plates, compact real bearings, metal load paths, stationary sensor PCB/moving magnet, and rig slots. It is too expensive and complicated for P1 as a whole: it uses ten 3 mm cut-metal pieces, four F696ZZ bearings, a PHS8 rod end, a damper, a compression spring, and a large fastener count.
- The **Chinese generic** reference has the simplest visible spring/yoke architecture and a protected PCB compartment, but it is SolidWorks-only. Geometry, fits, dimensions, occurrence counts, and material thicknesses are UNKNOWN. It cannot be trusted as a printable dimensional source in this environment.
- The **Fanatec reference** gives the cleanest horizontal/vertical packaging precedent. Its two valid STEP configurations have four solids and a compact 154 x 61.5 x 76 mm base, but they omit useful internal mechanism detail. It is an exterior/configuration reference, not a manufacturing design.
- The **hydraulic reference** has the strongest visibly defined metal load path: an 8 mm lever plate, an 8 x 27 mm steel pivot pin, and paired flanged bushings inside a bent sheet base. Its custom hydraulic cylinder, piston, linkage, bushings, and metal fabrication are wrong for a low-cost P1.
- The **MOZA low-poly reference** is one fused solid. The STEP and STL are geometrically clean and agree in scale, but no functional components can be recovered. It is useful only for a rough vertical ergonomic envelope, not mechanics or manufacturing.

Recommended P1 is an original mixed architecture: a mostly printed modular base/support structure, a single low-cost drilled steel flat-bar lever, a fixed M8 steel pivot through two real 608 bearings housed in a replaceable printed lever-root hub, a simple extension spring with steel anchors, a moving neodymium magnet and stationary adjustable SS49E sensor board, a separate Pro Micro enclosure, independent rig holes, and a removable steel-screw desk clamp. Validate one vertical/diagonal configuration first; retain a bolt-on lever interface that can support a later horizontal variant. Do not add hydraulic parts, a damper, load cell, or a complex adjustable linkage to P1.

An example load only: 100 N applied 0.22 m from the pivot produces **22 N·m**. This is a torque illustration, not a safety factor or FEA result. Geometry and load paths still require physical proof testing.

## 2. Workspace inventory

### Important file tree

```text
chinese-generic-sim-handbrake-model-1.snapshot.1/
  Chinese handbrake assembly.SLDASM                 main assembly candidate
  Chinese handbrake handle assembly.SLDASM          handle subassembly
  Chinese handbrake PCB assembly.SLDASM             electronics subassembly
  Chinese handbrake yoke assembly.SLDASM            spring/yoke subassembly
  Chinese Handbrake side wall.SLDPRT
  Chinese Handbrake Lower Handle.SLDPRT
  Chinese Handbrake UpperHandle.SLDPRT
  Chinese Handbrake reaction plate.SLDPRT
  Chinese Handbrake spring.SLDPRT
  Chinese Handbrake PCB.SLDPRT / PCB cover.SLDPRT
  ...32 SLDPRT and 4 SLDASM total

fanatec-handbrake-1.snapshot.1/
  FANATEC Handbrake down.step                        neutral assembly/configuration
  FANATEC Handbrake up.step                          alternate configuration
  FANATEC Handbrake v2.f3d                           native Fusion archive

handbrake-for-sim-racing-diy-1.snapshot.48/
  STEP and Parasolid/hand brake v1.2.stp             main neutral assembly
  STEP and Parasolid/*.x_t                           Parasolid duplicate; not parsed
  HB1.jpg / HB2.jpg / HB3.bmp                        renders and dimensioned overview
  Cutting; flexion; electronics and information/
    fasteners and accessories.png                    21-line hardware list
    printed parts/*.stl                              10 printable parts
    сutting 3mm/hand brake v1.1 (250x200).dxf        nested sheet
    сutting 3mm/Plates separately/*.dxf              7 plate definitions
    сutting 3mm/hand brake v1.1 info.pdf              3 mm sheet nesting report
    electronics/AS5600_analog_pcb/                   Gerbers, BOM, PnP, images

hydraulic-handbrake-1.snapshot.2/
  Handbrake.stp                                      main neutral assembly
  Handbrake/Handbrake.SLDASM                         native assembly
  Handbrake/*.SLDPRT                                 12 native parts
  Handbrake/IGS/*.IGS                                9 neutral part exports
  Handbrake/DWG/*.DWG                                9 drawings; not parsed
  Handbrake/SolidWorks_Draw/*.SLDDRW                 9 native drawings
  Handbrake/Web/*.jpg                                part renders/drawing previews

moza-hbp-handbrake-low-poly-1.snapshot.1/
  MOZA HBP Handbrake Low Poly.step                   single-solid neutral model
  MOZA HBP Handbrake Low Poly.stl                    matching mesh
```

### File totals

| Project | Files | Engineering formats |
|---|---:|---|
| Chinese generic | 36 | 32 SLDPRT, 4 SLDASM |
| Fanatec reference | 3 | 2 STEP, 1 F3D |
| DIY v1.2 | 31 | 1 STEP, 1 Parasolid, 10 STL, 8 DXF, 1 PDF, 2 CSV, 2 Gerber ZIPs, images |
| Hydraulic | 71 | 1 STEP, 1 SLDASM, 12 SLDPRT, 9 IGES, 9 DWG, 9 SLDDRW, 30 JPG |
| MOZA low-poly | 2 | 1 STEP, 1 STL |

No README, LICENSE, COPYING, or explicit commercial-use grant was found in any package. SHA-256 hashes for every source file are in `analysis_generated/model_inventory.csv`.

## 3. Model 1 audit - Chinese generic sim handbrake

**MODEL:** Chinese generic sim handbrake  
**SOURCE FILE(S):** `Chinese handbrake assembly.SLDASM`, 3 subassemblies, 32 SLDPRT definitions  
**GEOMETRY SOURCE USED:** SolidWorks OLE metadata and embedded preview PNG only; proprietary B-Rep not parsed  
**CONFIGURATION:** horizontal  
**OVERALL DIMENSIONS:** UNKNOWN  
**LEVER:** two-piece metal-looking lower/upper handle; exact length/thickness UNKNOWN  
**PIVOT:** filename evidence includes M8 bolts, bush/bushing, plastic washers, circlip, and cotter pin; exact arrangement UNKNOWN  
**BEARINGS/BUSHINGS:** bushes are modeled; no named rolling bearing  
**SPRING SYSTEM:** visible compression spring captured by a yoke/reaction-plate system  
**BASE:** plate-and-side-wall metal-looking enclosure  
**FASTENERS:** unique definitions include M3, M5, and M8 families; assembly quantities UNKNOWN  
**SENSOR:** separate PCB and PCB-cover subassembly; sensor type UNKNOWN  
**PCB SPACE:** protected rear/side rectangular cover visible in embedded preview  
**PRINTED PARTS:** none supplied as STL; no evidence it was designed for FDM  
**METAL PARTS:** appears predominantly plate/turned hardware, but material metadata was not established  
**CLAMP COMPATIBILITY:** possible external under-base module; base geometry and strength UNKNOWN  
**RIG MOUNTING:** holes/slots are visible in previews, but sizes/spacing UNKNOWN  
**MAJOR WEAK POINTS:** likely bolt/bushing wear, possible plastic washer creep, thin plate around slots, and cantilevered long lever; cannot be dimensionally verified  
**USEFUL DESIGN PRINCIPLES:** simple axial compression spring/yoke, horizontal package, discrete electronics cover, replaceable fasteners  
**UNKNOWNS:** all dimensions, fits, materials, occurrences, sensor method, spring rate, travel, and actual clearances  
**CONFIDENCE:** architecture ESTIMATED from embedded preview and filenames; part-file inventory VERIFIED; geometry UNKNOWN

### Mechanism and DFM assessment

The embedded main-assembly preview shows a long horizontal lever rotating between two side structures. A compression spring sits in a compact yoke below/behind the pivot and reacts into a separate plate. That is a mechanically simple way to create return force without a gas damper or hydraulic system. The filenames `Chinese Handbrake bush.SLDPRT`, `handle bush`, `plastic washer`, and M8 pivot hardware indicate a bushed bolt pivot, not a rolling-bearing pivot. This is less desirable for repeated cycling than a steel shaft supported by bearings.

The main parts look like machined/laser-cut metal plates. Printing the thin lever and side walls directly in PETG would not preserve the original load path. The long handle, abrupt bends near the lever root, slots, and bolt holes are potential stress concentrators. No strength conclusion is possible without B-Rep dimensions, material, and testing.

Hall adaptation is feasible in principle: attach a magnet to the rotating lower handle and a stationary sensor board to one side wall. The existing separate PCB cover is the best packaging principle in this model. Exact gap, travel, and bracket clearance are UNKNOWN.

### Dimensional trust verdict

**Do not manufacture or print from this package without opening it in a real SolidWorks-compatible B-Rep system and measuring it.** Filenames are not dimensions and embedded previews are not metrology.

## 4. Model 2 audit - Fanatec reference

**MODEL:** Fanatec handbrake reference  
**SOURCE FILE(S):** `FANATEC Handbrake down.step`, `FANATEC Handbrake up.step`, `FANATEC Handbrake v2.f3d`  
**GEOMETRY SOURCE USED:** both STEP B-Reps; F3D archive metadata/thumbnail only  
**CONFIGURATION:** horizontal and vertical/up configurations  
**OVERALL DIMENSIONS:** VERIFIED down 424.000 x 64.687 x 118.000 mm; VERIFIED up 213.373 x 64.687 x 328.627 mm  
**LEVER:** VERIFIED 4.000 mm thick solid; approximate pivot-to-grip centroid DERIVED about 224 mm  
**PIVOT:** concentric VERIFIED 7/8/12 mm cylindrical features at the candidate pivot/boss; hardware standard not documented  
**BEARINGS/BUSHINGS:** UNKNOWN; no recoverable named internals  
**SPRING SYSTEM:** UNKNOWN; not modeled  
**BASE:** VERIFIED 154.000 x 61.500 x 76.000 mm envelope across the two unchanged base solids  
**FASTENERS:** holes/bosses modeled, no BOM or named hardware  
**SENSOR:** UNKNOWN; not modeled  
**PCB SPACE:** enclosed base could contain electronics, but usable cavity geometry was not separated  
**PRINTED PARTS:** none identified as print-ready  
**METAL PARTS:** exterior resembles thin formed/cut metal and molded grip; exact materials UNKNOWN  
**CLAMP COMPATIBILITY:** removable under-base adapter is possible, but only 61.5 mm base width limits clamp-bolt spacing  
**RIG MOUNTING:** some base/side holes are modeled; exact intended mounting pattern is not documented  
**MAJOR WEAK POINTS:** a 4 mm lever copied in PETG would be structurally poor; internals and stops are absent; exterior geometry cannot establish reliability  
**USEFUL DESIGN PRINCIPLES:** compact rectangular base; bolt-on/reconfigurable lever orientation; separated grip, lever, and base bodies  
**UNKNOWNS:** internal pivot, spring, sensor, stops, bearing arrangement, wall thickness intent, and production tolerances  
**CONFIDENCE:** envelope/topology VERIFIED; mechanism UNKNOWN; configurability VERIFIED as two CAD states but the reconfiguration procedure is not documented

### CAD quality and geometry

Both STEP files declare millimetres and import as valid B-Reps. Each contains four solids, 105 faces, and four shells. The base solids are unchanged between configurations. The grip and lever solids are repositioned. This supports a configuration reference but does **not** prove a continuous actuation range. No travel angle was claimed.

The grip envelope is VERIFIED at 106.000 x 42.375 x 42.375 mm. The lever solid extends about 317 mm overall in the down file because its root and grip-end geometry are included; the meaningful hand lever arm is approximately 224 mm from candidate pivot to grip centroid. This is DERIVED and should not be treated as a production dimension.

### Printability and structural assessment

The STEP is geometrically convertible, but it is not a printable mechanism. The 4 mm lever is consistent with metal sheet, not a safe PETG cantilever at a roughly 0.22 m lever arm. The base solids overlap as an exterior package rather than a documented print assembly. Supports, internal cavities, spring mounts, and electronics mounts are absent.

### Hall and clamp integration

The enclosed base provides a useful packaging volume, but a sensor bracket would need to be created from scratch. A removable clamp could attach below or behind the 154 x 61.5 mm base. Clamp reaction should not be carried by a thin printed copy of the shell.

### Dimensional trust verdict

**Trust the two STEP envelopes as reference geometry, not as a complete product. Do not print it as a working handbrake.**

## 5. Model 3 audit - Handbrake for sim racing DIY v1.2

**MODEL:** hand brake v1.2  
**SOURCE FILE(S):** main STEP, Parasolid duplicate, 10 STLs, 8 mm-unit DXFs, one PDF, hardware-list image, AS5600 PCB files  
**GEOMETRY SOURCE USED:** STEP B-Rep/XCAF, STL meshes, DXF geometry, fabrication PDF, package images  
**CONFIGURATION:** vertical/rally style  
**OVERALL DIMENSIONS:** VERIFIED STEP 165.611 x 84.090 x 302.591 mm; package overview independently calls out 163.24 x 81.06 x 302.57 mm excluding some protrusions  
**LEVER:** two 3 mm side plates plus printed handle; VERIFIED handle envelope 26 x 20 x 122 mm; drawing calls out 116.9 mm handle length  
**PIVOT:** paired bearing axes; primary at x=17.000, z=43.429 mm and secondary near x=97.97, z=54.8 mm in assembly coordinates  
**BEARINGS/BUSHINGS:** VERIFIED four F696ZZ, modeled ID 6, OD 15, flange OD 17, width 5 mm  
**SPRING SYSTEM:** 20 x 51 light compression spring combined with a compact damper/gas-spring-like component, adjustable holes/slots, and PHS8 rod end  
**BASE:** ten pieces of 3 mm cut sheet, including paired plates and bent/flanged base pieces  
**FASTENERS:** extensive M3/M6/M8 hardware; 90 top-level occurrences in STEP  
**SENSOR:** moving 5 x 4 x 2 mm magnet, printed magnet holder, stationary AS5600 analog angle-sensor PCB  
**PCB SPACE:** dedicated 12.616 x 3.116 x 54.016 mm sensor-board assembly envelope; no clear protected main-controller enclosure  
**PRINTED PARTS:** 10 watertight STLs  
**METAL PARTS:** ten 3 mm laser-cut/bent plates plus rod end, bearings, damper, shafts, springs, and fasteners  
**CLAMP COMPATIBILITY:** no desk clamp; `clamp.stl` clamps the resistance component, not a desk  
**RIG MOUNTING:** strong; base flanges visibly include slotted mounting holes  
**MAJOR WEAK POINTS:** high part count, many joints that can loosen, unsupported/protruding sensor PCB, complex resistance linkage, thin printed handle/spacers, BOM inconsistencies  
**USEFUL DESIGN PRINCIPLES:** bearing-supported load path, paired side plates, mm-documented hardware, co-axial contactless sensor, sensor-board slots, steel rig-mounting flange  
**UNKNOWNS:** spring rate, damper force/part specification, exact actuation travel, fits/tolerances, plate material, sensor calibration, and main USB controller packaging  
**CONFIDENCE:** high for geometry and component names; medium for operating behavior because the STEP is static and no assembly-motion study is supplied

### Architecture and dimensions

This is the only package that resembles a complete build package. The STEP declares millimetres, imports as a valid 139-solid assembly, and exposes 90 named occurrences. The 3 mm plate thickness is repeated in B-Rep dimensions and the `сutting 3mm` documentation. The two main `hbplate2` side plates are 3 mm thick, have a DERIVED 26 mm internal gap and 32 mm outer spacing, and surround the principal mechanism.

The primary hand-lever bearing pair centers at approximately x=17, z=43.429 mm. The printed handle center of mass is 182.43 mm from that axis; the far grip end is farther, so actual user leverage varies with hand position. Four F696ZZ flanged bearings form two paired pivots. This is the best pivot implementation in the set.

### Part count and cost drivers

- VERIFIED ten printed STL files: `cap`, `clamp`, `hand rest`, `handle`, `hbha`, `magnet holder`, `rear hub`, `spacer`, `spacer1`, `spacer2`.
- VERIFIED ten nested 3 mm plate pieces in the PDF: two base-side variants, two each of plates 2/3/4, and one each of plates 5/6.
- VERIFIED hardware list includes 14 M6 socket-head screws across five lengths, two countersunk M6 screws, 11 M6 nyloc nuts, M8 hardware, M3 hardware, washers, PHS8 rod end, silicone tube, four F696ZZ bearings, magnet, and spring.
- The STEP additionally models a compact `SZ 8010_20 x 051 (0B)` resistance component and an M8x170 shaft.

Cost/effort is driven by laser cutting/bending, the PHS8 rod end, four less-common flanged bearings, the resistance component, and assembly time. This is not a low-cost mostly printed P1.

### STL integrity and units

All ten STLs are unitless by format. Millimetre scale is accepted only because named STEP occurrences have matching envelopes/volumes and DXF/STEP documentation is mm. After welding repeated STL facet vertices, every STL is one connected component, watertight, winding-consistent, has positive volume, zero detected duplicate faces, and zero near-zero-area faces. The MOZA STL passed the same checks.

One discrepancy is material: `rear hub.stl` volume is about 1206.3 file-units³ while the named STEP occurrence is about 1176.8 mm³, a roughly 2.5% difference. This indicates revision drift or a configuration difference. Other named printed-part volumes agree closely.

### Printability

- `handle.stl` (26 x 20 x 122 mm) should not be printed as a tall upright column for structural use. A side orientation gives longer continuous layers along the lever direction, but the internal shaft/bore may need support and post-processing. The modeled M8x170 steel member is an important reinforcement principle.
- `hand rest.stl` (about 40 x 40 x 3 mm) prints flat.
- `cap.stl` and `magnet holder.stl` print on their largest flat faces.
- `rear hub.stl` and spacers need bore/shaft calibration coupons. Vertical bore orientation improves circularity but can create a tall slender `spacer1` print.
- `clamp.stl` is a small mechanism clamp with a through feature; it may require support depending on orientation. It is not a table clamp.
- Bearing fits occur primarily in metal plates, avoiding risky PETG press fits in this design.

### Resistance system

The spring/damper linkage is adjustable through several holes and curved slot patterns. It provides useful higher-range product principles: replaceable spring, variable geometry, and multiple leverage settings. It is not the simplest reliable P1 mechanism. Spring rate, damper force, and installed preload are undocumented, so exact hand-force curves cannot be derived.

### Hall/PCB system

The AS5600 architecture is excellent: a moving magnet near the primary pivot and a stationary slotted sensor board avoid wear. The STEP sensor assembly envelope is 12.616 x 3.116 x 54.016 mm including components. The printed magnet holder is about 15.2 x 15.2 x 10 mm. The package BOM explicitly gives a 5 x 4 x 2 mm magnet, and the modeled magnet volume is consistent.

There is a PCB documentation conflict: `BOM_PCB_AS5600_pcb.csv` calls C2 **10 uF**, while `PickAndPlace_PCB_AS5600_pcb.csv` labels C2 **1 uF**. Resolve this before ordering or assembling that board. The provided PCB is a sensor board only; P1 still needs a protected Pro Micro/main board compartment and strain-relieved USB routing.

### Dimensional trust verdict

The neutral CAD and STL quality are the best in the set, but **do not complete-print/fabricate blindly**. First verify F696ZZ fit, every M6/M8 clearance, plate material/thickness, spring/damper specifications, sensor gap, and the BOM conflicts. Small printed parts are reasonable test prints after coupons.

## 6. Model 4 audit - Hydraulic handbrake

**MODEL:** Hydraulic Handbrake  
**SOURCE FILE(S):** `Handbrake.stp`, native SolidWorks assembly/parts, 9 IGES parts, 9 drawings, 30 images  
**GEOMETRY SOURCE USED:** STEP B-Rep/XCAF, IGES surfaces, package drawing images; native SolidWorks geometry not needed for measurements  
**CONFIGURATION:** vertical/rally style  
**OVERALL DIMENSIONS:** VERIFIED 92.245 x 263.761 x 409.983 mm  
**LEVER:** VERIFIED 8 mm Arm2 plate; local part envelope 289.980 x 83.498 x 8.000 mm  
**PIVOT:** VERIFIED 8 x 27 mm Shtift pin at assembly center x=22.266, y=68.682, z=142.951 mm  
**BEARINGS/BUSHINGS:** paired custom-looking flanged `Durjach` parts with 8 mm bore, 16 mm neck, and 32 mm flange cylindrical faces  
**SPRING SYSTEM:** hydraulic cylinder/piston/linkage supplies resistance; no documented simple return spring  
**BASE:** bent U-channel `Osnova`, 52 x 64 x 165 mm; drawing calls out 2.30 mm sheet  
**FASTENERS:** several pins/bolts are geometrically represented but no BOM  
**SENSOR:** none modeled  
**PCB SPACE:** no dedicated enclosure; limited space inside the U-base if hydraulic components are removed  
**PRINTED PARTS:** none  
**METAL PARTS:** nearly all structural and hydraulic components  
**CLAMP COMPATIBILITY:** possible under 52 mm-wide base but requires a wider adapter/reinforcement plate  
**RIG MOUNTING:** base geometry/drawings include holes/slots, but the supplied design is mainly a fabricated metal assembly  
**MAJOR WEAK POINTS:** custom seals/cylinder, side-load risk at hydraulic link, wear in custom bushings, welded/bent thin base, maintenance/leak risk  
**USEFUL DESIGN PRINCIPLES:** thick metal lever, two-sided pivot support, separate steel pin, compact U-channel base, replaceable linkage  
**UNKNOWNS:** materials, fits, bushing material, hydraulic pressure/seals, travel, force curve, and mounting-hole standard  
**CONFIDENCE:** dimensions/part structure high from neutral CAD; operating performance UNKNOWN without hydraulic data/testing

### Mechanism and load path

The hand load enters an 8 mm metal lever (`Arm2`), passes through paired flanged bushings and the 8 mm steel pin into the U-channel base, then drives `Arm1` and `ArmButalo` into `Butalo`/`PompaTqlo`. This is a strong mechanical concept, but the resistance system is expensive and maintenance-heavy.

The pivot-to-grip center-of-mass distance is DERIVED as 203.72 mm. The grip extends farther, so tip leverage is higher. At 100 N on the grip centroid, pivot torque is about 20.4 N·m; this does not establish strength.

### CAD quality

The main STEP declares millimetres, imports as 14 valid solids, and retains names. The nine IGES files also identify `MM`, but import as surfaces/open shells rather than solids. Use the STEP for assembly metrology. The drawings visually agree with key values: 2.30 mm base sheet, 8 mm lever plate, and detailed custom pivot pieces.

### Hall and clamp adaptation

A magnet can be placed concentrically at the pivot and a stationary board on the outside of `Osnova`, but the existing hydraulic link occupies the internal volume. Removing the hydraulic system would make the reference a useful vertical skeleton, not a minor modification. A desk clamp needs a wider removable adapter plate so clamp reaction does not peel the 2.3 mm base flange.

### Dimensional trust verdict

Trust the STEP/drawing measurements as reference dimensions, but **do not build this as P1** unless custom metal fabrication and hydraulic work are intentionally accepted.

## 7. Model 5 audit - MOZA HBP low-poly

**MODEL:** MOZA HBP Handbrake Low Poly  
**SOURCE FILE(S):** matching STEP and STL  
**GEOMETRY SOURCE USED:** STEP B-Rep and STL mesh  
**CONFIGURATION:** vertical/rally style  
**OVERALL DIMENSIONS:** VERIFIED 67.000 x 152.000 x 319.331 mm  
**LEVER:** fused into one low-poly solid; no separable lever geometry  
**PIVOT:** UNKNOWN; only four cylindrical faces exist, including two 12 mm faces, but no assembly meaning is recoverable  
**BEARINGS/BUSHINGS:** UNKNOWN  
**SPRING SYSTEM:** UNKNOWN  
**BASE:** fused exterior envelope  
**FASTENERS:** UNKNOWN  
**SENSOR:** UNKNOWN  
**PCB SPACE:** UNKNOWN; no recoverable cavity/component structure  
**PRINTED PARTS:** one watertight STL, but it is a monolithic exterior/prop rather than a mechanism  
**METAL PARTS:** UNKNOWN  
**CLAMP COMPATIBILITY:** a 67 x 152 mm footprint could accept an adapter in a new design; the supplied solid does not define one  
**RIG MOUNTING:** not mechanically recoverable  
**MAJOR WEAK POINTS:** monolithic fused body, no joints, no hardware, no load path, no replaceable electronics, large solid-print volume  
**USEFUL DESIGN PRINCIPLES:** vertical ergonomic envelope only  
**UNKNOWNS:** every functional detail  
**CONFIDENCE:** envelope and mesh integrity VERIFIED; all mechanism conclusions UNKNOWN

The STEP is one valid B-Rep solid. The STL becomes one watertight, winding-consistent component after normal STL vertex welding. STEP and STL bounds agree essentially exactly, so STL file units are safely interpreted as millimetres. Volumes also agree within about 0.001%. This proves conversion consistency, not functional usefulness.

Printing the monolithic shape would consume about 534,000 mm³ of solid material before slicer infill changes and would not produce a moving handbrake. It is the least useful mechanical source.

## 8. Dimensional comparison

| Model | Overall L x W x H | Base / side structure | Lever / hand radius | Critical pivot evidence | Confidence |
|---|---|---|---|---|---|
| Chinese generic | UNKNOWN | UNKNOWN | UNKNOWN | M8/bush filenames only | geometry UNKNOWN |
| Fanatec | down 424.000 x 64.687 x 118.000; up 213.373 x 64.687 x 328.627 mm | 154.000 x 61.500 x 76.000 mm base | about 224 mm to grip centroid | 7/8/12 mm concentric candidate features | VERIFIED/DERIVED |
| DIY v1.2 | 165.611 x 84.090 x 302.591 mm | paired 3 mm plates; 26 mm inner gap | 182.43 mm pivot-to-handle centroid; 122 mm handle envelope | four F696ZZ, 6 mm bore | VERIFIED/DERIVED |
| Hydraulic | 92.245 x 263.761 x 409.983 mm | 52 x 64 x 165 mm, 2.3 mm sheet | 203.72 mm pivot-to-grip centroid | 8 x 27 mm shaft; 8/16/32 mm flanged bushings | VERIFIED/DERIVED |
| MOZA low-poly | 67.000 x 152.000 x 319.331 mm | fused | UNKNOWN | UNKNOWN | envelope VERIFIED |

Full evidence rows are in `analysis_generated/measurements.csv`.

## 9. Mechanical architecture comparison

The Chinese design is the simplest visible horizontal mechanism. Fanatec is the best compact configurable envelope but lacks internals. DIY is the most complete and best instrumented mechanism, at the cost of complexity. Hydraulic has the strongest traditional fabricated-metal skeleton but the most expensive resistance system. MOZA has no recoverable mechanism.

The most useful cross-model pattern is a **two-sided pivot support with a metal lever/shaft and separate electronics**. Every credible functional reference routes hand force through metal at the lever or pivot. None provides evidence that a long, thin PETG-only lever is durable.

## 10. Pivot system comparison

| Model | Pivot evidence | Wear/DFM assessment |
|---|---|---|
| Chinese generic | M8 bolt, bush/bushing, plastic washers named | Simple/cheap; likely more friction and wear; exact fit UNKNOWN |
| Fanatec | concentric 7/8/12 mm features; internals omitted | Cannot establish whether bearing/bushing exists |
| DIY v1.2 | four F696ZZ flanged bearings on two axes, paired plates | Best supplied pivot; compact and smooth, but higher count and less-common bearing |
| Hydraulic | 8 mm steel pin, paired 8/16/32 flanged bushings, 8 mm lever | Strong load path; custom bushings/pin increase fabrication cost |
| MOZA | none recoverable | unusable as pivot evidence |

Closest to the desired `hand -> lever -> steel pivot -> bearings -> reinforced housing` is **DIY v1.2**. P1 should adapt the principle using common 608-2RS bearings only after PETG fit coupons prove a reliable 22 mm pocket.

## 11. Spring/resistance comparison

- **Chinese generic:** simple axial compression spring and yoke. Best simplicity principle; dimensions/preload UNKNOWN.
- **Fanatec:** no internal spring evidence.
- **DIY v1.2:** adjustable compression spring plus resistance component and PHS8 link. Best adjustment principle; too complex for P1.
- **Hydraulic:** cylinder/piston linkage. Strong simulation feel is possible, but cost, seals, machining, and maintenance reject it for P1.
- **MOZA:** no evidence.

For P1, use one replaceable **extension spring** with steel eye/bolt anchors and a mechanical stop. It is cheaper and easier to inspect than the yoke/damper systems. Place multiple steel-supported anchor holes in later revisions for resistance adjustment; use one fixed validated position in the first core test.

## 12. 3D printability comparison

| Model | FDM readiness | Key concern |
|---|---|---|
| Chinese generic | poor/UNKNOWN | no neutral geometry or STL; appears metal-oriented |
| Fanatec | poor | exterior STEP only; 4 mm lever unsuitable as PETG copy |
| DIY v1.2 | good for ten auxiliary parts, poor for whole product | core still needs ten cut-metal plates and extensive hardware |
| Hydraulic | very poor | fabricated metal and hydraulic parts |
| MOZA low-poly | mesh-valid but functionally unusable | single fused exterior, high material/support demand |

Assumed PETG, 0.20 mm layers, at least 5-6 perimeters around loaded holes, high local infill, and no load-bearing printed threads. Final slicer orientations must be reviewed after P1 geometry exists.

## 13. Durability and weak-point analysis

Critical load zones across the references are lever roots, pivot holes, side-wall transitions, spring anchors, and base/clamp interfaces. Printed versions add layer-separation risk.

An illustrative torque range:

| Hand load | Radius | Pivot torque |
|---:|---:|---:|
| 50 N | 0.22 m | 11 N·m |
| 100 N | 0.22 m | 22 N·m |
| 150 N | 0.22 m | 33 N·m |

These are input loads only. Bearing reactions and spring-anchor forces depend on geometry and can be higher. No safety factor is claimed.

P1 structural risks to manage:

- PETG creep around bearing pockets and clamp loads.
- Lever-root hub splitting between layer lines.
- M8 pivot threads contacting bearing inner races.
- Spring hook tearing a printed anchor.
- Printed supports spreading apart under moment.
- Clamp reaction peeling the base or crushing a printed shell.
- Hard travel stops shocking thin walls.

Mitigations are metal lever, smooth pivot shank, dual bearings, through-bolted supports, large washers/backing strips, steel eye bolts, rubber bump stop, and a clamp load path tied to steel reinforcement.

## 14. Hall sensor integration opportunities

Ranking:

1. **DIY v1.2** - best. Co-axial moving magnet, stationary slotted AS5600 board, and documented magnet holder.
2. **Chinese generic** - good packaging potential. Existing PCB cover and exposed rotating lower handle, but all gaps/dimensions UNKNOWN.
3. **Hydraulic** - feasible outside the pivot if the hydraulic linkage is removed/reworked.
4. **Fanatec** - enclosed base is promising, but pivot cavity and internals are absent.
5. **MOZA** - no recoverable interface.

For SS49E experiments, make the stationary board adjustable over a VERIFIED experimental **3-15 mm gap range** and allow magnet rotation/orientation changes. Do not freeze the magnet pocket until P0 maps ADC output versus angle and gap. Keep the sensor on a small replaceable 3-wire board so it can later be exchanged for AS5600 or another magnetic sensor.

## 15. PCB/USB packaging opportunities

- DIY proves a modular sensor-board concept but leaves the main controller exposed/undefined.
- Chinese provides the best visible separate electronics cover.
- Fanatec provides the best compact enclosure envelope but no internal mounting evidence.
- Hydraulic requires a new enclosure.
- MOZA provides no usable cavity.

P1 should use two modules:

```text
Pro Micro / main PCB enclosure
        |
  3-wire locking connector
        |
adjustable Hall sensor board
```

Provide screw access, a strain-relieved USB cable exit, a future USB-C bulkhead/PCB opening, LED window option, calibration-button access, and enough slack that lever motion cannot pull the sensor cable. Do not glue the controller permanently into the base.

## 16. Horizontal versus vertical suitability

| Model | Horizontal | Vertical/rally | Evidence |
|---|---|---|---|
| Chinese generic | excellent | poor | embedded assembly preview |
| Fanatec | excellent | excellent | two STEP configurations |
| DIY v1.2 | poor | excellent | STEP/renders |
| Hydraulic | limited | excellent | STEP/renders |
| MOZA low-poly | poor | envelope only | fused vertical solid |

P1 should validate one vertical/diagonal configuration because it keeps the footprint compact and exposes the mechanism for testing. The lever-to-hub interface should be bolt-on so a horizontal lever plate can be tested later without rebuilding the pivot/base.

## 17. Table-clamp integration analysis

| Model | Feasibility | Main issue |
|---|---|---|
| Chinese generic | medium | base dimensions/strength UNKNOWN; separate under-base bracket needed |
| Fanatec | medium | narrow 61.5 mm base; shell must not carry clamp peel load |
| DIY v1.2 | good | 81 mm-wide steel flange and rig slots; add a separate clamp plate, not the mechanism `clamp.stl` |
| Hydraulic | medium | 52 mm U-base needs a wider load-spreading adapter |
| MOZA low-poly | low | no separable base or load path |

P1 clamp architecture should be removable and mechanically independent of rig holes: steel M10 threaded rod/bolt, captured steel coupling nut or nut, 40-50 mm swivel pressure pad, large printed hand knob around steel hardware, and rubber pads. Target 10-55 mm desk thickness. Tie clamp reaction into steel base reinforcement; do not depend on a printed main thread.

## 18. Component and hardware requirements found

The detailed evidence table is `analysis_generated/hardware_candidates.csv`.

Most reusable reference hardware:

- M6/M8 through-bolts, washers, and nyloc nuts.
- F696ZZ bearings in DIY if compactness is critical; 608-2RS is preferable for P1 availability and cost if the larger pocket is acceptable.
- Replaceable compression/extension spring with metal anchors.
- 5 x 4 x 2 mm magnet/AS5600 arrangement as a reference, not a mandatory final sensor choice.
- Hydraulic 8 mm steel pin principle, not its custom pin geometry.

Prototype cost drivers to avoid are laser-cut multi-plate stacks, custom bushings, PHS8 rod ends, dampers/gas springs, hydraulic cylinders, machined shafts, and a large mix of fastener lengths.

## 19. License and commercial-use evidence

Package evidence:

- **All five:** no README/LICENSE/COPYING or explicit commercial grant found.
- **Chinese generic:** OLE metadata shows SolidWorks 2012-era files and author field `Les`; no rights statement. A secondary web index shows the exact title as a GrabCAD model and describes dimensionally accurate mounting holes, but it does not establish the license contained with this download.
- **Fanatec:** package is branded `FANATEC`; no rights statement. Treat it only as reference geometry and avoid copying brand/trade dress.
- **DIY v1.2:** no rights statement. PCB/manufacturing files do not imply commercial permission.
- **Hydraulic:** STEP header names `Jose Luis Fernandez`, Autodesk Inventor 2012, and a path containing `GRABCAD DIA DIA`; no rights statement.
- **MOZA low-poly:** package is branded `MOZA`; no rights statement. A current similarly titled CGTrader listing is not enough to authenticate this package or grant rights.

**Commercial-use clarity is low/unclear for every package.** This is an evidence statement, not legal advice. The safe engineering course is to use general mechanical principles and create an original architecture, dimensions, parts, and appearance.

## 20. Comparison matrix

Scale: 5 = best for the stated P1 objective; 1 = worst; `U` = unavailable evidence.

| Category | Chinese | Fanatec | DIY v1.2 | Hydraulic | MOZA low-poly |
|---|---:|---:|---:|---:|---:|
| Mechanical simplicity | 4 | U | 2 | 1 | 1 functional |
| Low prototype cost | 3 | U | 2 | 1 | 1 functional |
| Printability as supplied | 1 | 1 | 3 | 1 | 1 functional |
| Low metal-fabrication need | 2 | U | 1 | 1 | U |
| Few custom components | 3 | U | 1 | 1 | U |
| Durability potential | 3 | U | 5 | 5 | U |
| Pivot quality | 2 estimated | U | 5 | 4 | U |
| Simple P1 resistance | 5 principle | U | 2 | 1 | U |
| Adjustable future resistance | 2 | U | 5 | 3 | U |
| Hall adaptability | 3 | 2 | 5 | 3 | 1 |
| PCB packaging | 5 principle | 3 | 3 | 2 | 1 |
| Horizontal suitability | 5 | 5 | 2 | 2 | 1 |
| Vertical suitability | 1 | 5 | 5 | 5 | 5 envelope |
| Clamp integration | 3 | 2 | 4 | 3 | 1 |
| CAD quality/usefulness | 2 | 3 | 5 | 4 | 2 |
| Ease of safe modification | 2 | 3 | 4 | 3 | 1 |
| Likely reliability evidence | 2 | U | 4 | 3 | U |
| Commercial-license clarity | 1 | 1 | 1 | 1 | 1 |

## 21. Recommended Prototype P1 architecture

### Chosen concept

A compact vertical/diagonal mechanical skeleton, approximately in the DIY/MOZA footprint class, using:

1. Separate PETG base and left/right pivot-support modules through-bolted to steel backing strips.
2. A replaceable PETG lever-root hub containing **two 608-2RS bearings**.
3. A fixed M8 class 8.8 partially threaded bolt or shoulder bolt whose smooth shank passes through both bearing inner races; washers/spacer and M8 nyloc prevent axial binding.
4. A **25 x 5 mm steel flat-bar lever**, about 250-300 mm stock length, bolted to the printed hub. Cutting/drilling is acceptable; no CNC machining is required.
5. A separate printed grip and replaceable end cap.
6. One extension spring with M6 steel eye/bolt anchors. Initial P1 uses one anchor position and a rubber-bumper travel stop; later plates can add adjustment holes.
7. A moving N35/N42 neodymium magnet in a replaceable printed holder on the hub/lower lever.
8. A stationary SS49E sensor board on a slotted bracket covering a 3-15 mm experimental gap.
9. A rear/side Pro Micro enclosure connected by a 3-wire sensor cable, with strain-relieved USB exit.
10. Independent M6 rig holes/slots and a removable clamp adapter using an M10 steel screw/coupling nut/swivel pad.

### Why this is the recommended hybrid

- **DIY v1.2** proves that paired plates/bearings and a co-axial magnet/sensor work cleanly.
- **Hydraulic** proves the value of a thick metal lever and a steel pivot supported on both sides.
- **Chinese generic** contributes the simple single-spring/yoke philosophy and a separate electronics cover.
- **Fanatec** contributes the bolt-on orientation/configuration idea and compact base envelope.
- **MOZA** contributes only a rough vertical ergonomic/footprint reference.

The deliberate challenge to an all-printed P1 is the steel flat-bar lever. Every credible functional reference uses metal in the primary lever/load path. A 250 mm PETG-only lever would make layer orientation and creep the dominant failure risks. One drilled commodity flat bar is a low-cost compromise that materially improves safety and test value.

### P1 success criteria

- Smooth pivot with no printed-on-printed rubbing.
- No bearing creep or support spreading after repeated pulls.
- Stable return to zero and mechanical travel stop.
- Sensor monotonic over full travel with no contact.
- Electronics removable without disassembling the pivot.
- Rig mounting and desk clamp loads bypass thin covers.
- Progressive static/repetition tests completed before cosmetic shell work.

## 22. Features worth borrowing as engineering principles

| Reference | Principle | Why valuable |
|---|---|---|
| DIY v1.2 | paired real bearings and two-sided support | reduces friction/wear and controls shaft alignment |
| DIY v1.2 | moving magnet + stationary slotted sensor board | contactless, adjustable, serviceable |
| DIY v1.2 | rig slots in a wide base flange | flexible mounting and load distribution |
| Hydraulic | thick metal lever and steel pin | puts highest bending/pivot loads into metal |
| Hydraulic | compact U-channel base | simple load path and good lateral stiffness |
| Chinese generic | separate compression-spring/yoke module | simple replaceable resistance concept |
| Chinese generic | dedicated PCB cover | protects electronics while preserving service access |
| Fanatec | discrete lever orientations around one compact base | supports product-family reuse without a fully universal mechanism |
| MOZA | compact vertical proportions | ergonomic envelope reference only |

## 23. Features that should not be copied

- Any branded exterior, logos, trade dress, or unchanged downloaded geometry.
- DIY's complete 90-occurrence spring/damper/PHS8 stack for entry P1.
- Hydraulic cylinder/piston/custom bushings for an inexpensive prototype.
- Chinese likely bolt-through-bushing pivot as the preferred production pivot.
- Fanatec's 4 mm lever dimension if the material is changed to PETG.
- MOZA's monolithic fused solid.
- Printed main clamp threads or spring hooks.
- Exposed sensor PCB or a USB connector carrying cable strain directly on solder joints.
- Any undocumented fastener length from the DIY BOM until conflicts are resolved.

## 24. Critical dimensions/components to physically verify

Before P1 CAD is frozen:

1. Actual 608-2RS bearing OD, ID, width, chamfer, and seal protrusion from the purchased batch.
2. M8 pivot bolt smooth-shank diameter/length and thread start; threads must not run in the bearing bores.
3. Steel flat-bar actual width/thickness/straightness and achievable drilled-hole position.
4. Chosen spring free length, body OD, hook geometry, rate, maximum safe extension, and force at intended travel.
5. SS49E supply/output range and magnet polarity/orientation over 3-15 mm gaps.
6. Actual magnet dimensions/coating tolerance.
7. Pro Micro board, USB plug, and cable bend-radius envelope.
8. Printer XY hole shrinkage, PETG bearing-pocket creep, and heat-set insert pullout.
9. Desk thickness range, underside clearance, edge radius, and maximum clamp reach.
10. Desired hand force, lever travel, grip position, and resting angle.

Reference-specific verification if reusing a part:

- DIY F696ZZ actual 6 x 15 x 5 / flange 17 dimensions and fit.
- DIY M8 conflict: documentation says M8x45/M8x55 while STEP includes M8x40 and M8x170.
- DIY AS5600 C2 conflict: 10 uF BOM versus 1 uF PnP comment.
- DIY `rear hub` STL/STEP revision difference.
- Chinese dimensions only after native B-Rep access.

## 25. Small calibration prints before a full prototype

Use the same printer, PETG, nozzle, layer height, walls, and slicer compensation planned for P1.

1. **608 pocket ladder:** 21.8, 22.0, 22.1, 22.2, 22.3, 22.4 mm; include both 7 and 14 mm pocket depths.
2. **M8 clearance ladder:** 8.0, 8.2, 8.4, 8.6 mm through-holes.
3. **M6 clearance ladder:** 6.0, 6.2, 6.4, 6.6 mm.
4. **M6 nut traps:** 10.0, 10.2, 10.4, 10.6 mm across flats with realistic trap depth.
5. **Heat-set insert coupon:** sizes based on the exact purchased insert datasheet, plus +/-0.1 and +0.2 mm bore variants.
6. **Magnet pocket coupon:** nominal, +0.1, +0.2, +0.3 mm in both press-fit and retained-cover versions.
7. **Sensor-gap jig:** fixed 3, 5, 8, 10, 12, 15 mm stations for logging ADC output versus angle/orientation.
8. **Loaded bearing-wall coupon:** representative bearing pocket with the intended wall thickness and through-bolt, held under load for creep observation.

Do not use glue as the only magnet retention method in the final mechanism; the coupon may evaluate a mechanical cap plus optional adhesive.

## 26. Recommended P0/P1 shopping list

### P0 electronics bench

- 2 x ATmega32U4 Arduino Pro Micro, 5 V / 16 MHz.
- 3 x SS49E linear Hall sensor, TO-92, from a traceable supplier if possible.
- 4 x N35/N42 neodymium block magnet, nominal 10 x 5 x 3 mm, plus 4 x 6 x 3 mm disc magnets for comparison.
- 1 x AS5600 breakout/module as a benchmark against the linear Hall approach.
- 1 x solderable prototype board or small custom sensor breakout.
- 2 x JST-XH 3-pin cable assemblies, 200-300 mm.
- 100 nF ceramic capacitors, 10 uF electrolytic/ceramic capacitors, headers, breadboard jumpers.
- 1 x known-good data-capable USB cable.
- Digital caliper and a simple force gauge/luggage scale if not already owned.

### P1 mechanical core

- 2 x 608-2RS bearings, 8 x 22 x 7 mm; buy 4 so two are spares/test samples.
- 2 x candidate M8 class 8.8 partially threaded bolts, approximately M8x70, with verified smooth shank long enough for both bearing inner races; alternatively one M8 shoulder bolt after dimension check.
- M8 flat washers and M8 nyloc nuts, 4 each.
- 1 x steel flat bar, 25 x 5 x 300 mm minimum.
- M6 class 8.8 socket-head bolts: M6x20, M6x30, M6x40, four each for prototyping.
- M6 large washers and M6 nyloc nuts, at least 12 each.
- 2 x M6 eye bolts or clevis-style steel spring anchors with nuts/washers.
- 1 x extension-spring assortment centered on 15-20 mm OD and 60-100 mm hook-to-hook length; target spring rate cannot be finalized until hand-force/travel requirements are supplied.
- 2 x M6 adjustable rubber bump stops or equivalent rubber-covered stop bolts.
- PETG, 1 kg, known dry filament.
- M4/M5 heat-set insert assortment only for covers/brackets, not the primary pivot/clamp load.
- 2 x steel backing strips, approximately 25 x 3 x 180 mm, drillable by hand.
- For clamp P3, not required for first core test: M10x120 steel threaded rod/bolt, M10 coupling nut, 40-50 mm swivel pressure pad, steel washers, rubber sheet/pads, and a printed knob around a captured steel nut.

Spring selection is intentionally an assortment at P1 because no reference supplies a complete force-rate-travel specification and the user's target force is still unknown.

## 27. Unknowns/measurements still required from the owner

1. Preferred first P1 resting orientation: vertical, diagonal, or horizontal.
2. Desired handle travel in degrees or mm at the grip.
3. Desired light/medium/heavy hand-force range at full pull.
4. Printer model, build volume, nozzle size, and normal PETG dimensional accuracy.
5. Available fabrication tools: drill press/hand drill, hacksaw/bandsaw, files, taps.
6. Whether one drilled steel flat-bar lever and two drilled steel backing strips are acceptable.
7. Target P1 mechanical/electronics/clamp budget.
8. Desk thickness/underside obstruction measurements and desired clamp throat depth.
9. Grip diameter/length preference and right/left-hand mounting needs.
10. Measured pull force, travel, pivot size, and sensor behavior from the already reverse-engineered inexpensive metal handbrake, if available.
11. Whether P0 should compare SS49E and AS5600 before the sensor bracket interface is frozen.

## 28. Proposed next CAD phase - after approval only

1. Freeze P1 requirements: orientation, hand force, travel, desk/rig envelope, and allowed metal work.
2. Measure purchased bearings, pivot bolt, flat bar, spring candidates, magnets, and electronics.
3. Create a parameter sheet/master skeleton with pivot axis, lever radius, spring anchors, stops, sensor arc, base envelope, rig pattern, and clamp interface.
4. CAD only the mechanical core parts first: base, two supports, lever-root hub, steel lever drawing/template, spring anchor, and stop.
5. Produce the 608/M8/M6/insert/magnet coupons and revise fit allowances.
6. Print and assemble P1 core without electronics; run progressive load and repetition tests.
7. Add the adjustable Hall bracket and magnet holder after P0 field mapping.
8. Add the removable clamp after the rig-mounted core passes testing.
9. Add accessible electronics cover and cable management.
10. Only then refine appearance and consider horizontal/vertical variants and a custom PCB.

## Stop-condition conclusion

**A. Inspected:** all 143 source files across five packages, neutral B-Reps, STL integrity, DXF units/entities, PDF fabrication sheet, package renders, hardware/PCB lists, SolidWorks metadata/previews, and local tool availability.  
**B. Learned:** only DIY v1.2 is a complete functional reference; every credible load path uses metal; contactless sensing is best documented in DIY; license clarity is absent.  
**C. Recommended architecture:** printed modular skeleton + drilled steel lever + M8/dual-608 pivot + simple extension spring + adjustable SS49E + removable electronics + independent rig/clamp interfaces.  
**D. Reference contributions:** DIY pivot/sensor/rig base; Hydraulic metal load path; Chinese spring/PCB cover; Fanatec configuration packaging; MOZA envelope only.  
**E. Closest starting point:** DIY v1.2, used as a principle reference rather than copied geometry.  
**F. Purchase list:** specified in Section 26.  
**G. Physical verification:** specified in Sections 24-25.  
**H. Next plan:** specified in Section 28.

No production or prototype CAD has been created. Await approval of the architecture and answers to the Section 27 unknowns before starting CAD development.
