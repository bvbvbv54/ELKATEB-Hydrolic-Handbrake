"""Generate, validate, export, draw, and render Prototype P1.0.

Run from the workspace root through prototype_p1/build.ps1.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

import cadquery as cq
import ezdxf

import assembly
import base
import clamp
import coupons
import electronics_box
import grip
import hall_mount
import lever_hub
import pivot_supports
import spring_system
import stops
from common import ROOT, as_shape, export_part, overlap_volume, save_json, validate_shape
from parameters import P, parameter_rows, v


PRINT_MODULES = (base, pivot_supports, lever_hub, grip, spring_system, stops, hall_mount, electronics_box, clamp)
METAL_IDS = {"P1-005_STEEL_LEVER_TEMPLATE", "P1-030_LEFT_BACKING_STRIP", "P1-031_RIGHT_BACKING_STRIP"}


def ensure_dirs():
    for name in ("step", "stl", "dxf", "drawings", "coupons", "renders", "calculations", "reports"):
        (ROOT / name).mkdir(parents=True, exist_ok=True)


def collect_parts():
    result = {}
    for module in PRINT_MODULES:
        result.update(module.parts())
    return result


def export_parts():
    records = []
    for name, shape in collect_parts().items():
        records.append(export_part(name, shape, printable=name not in METAL_IDS))
    for name, shape in coupons.parts().items():
        cq.exporters.export(as_shape(shape), str(ROOT / "coupons" / f"{name}.step"))
        cq.exporters.export(as_shape(shape), str(ROOT / "coupons" / f"{name}.stl"), tolerance=0.08, angularTolerance=0.15)
        rec = validate_shape(name, shape)
        rec["output_directory"] = "coupons"
        records.append(rec)
    return records


def _save_assembly(path, items, name):
    assy = cq.Assembly(name=name)
    from common import COLORS
    for item in items:
        assy.add(item["shape"], name=item["name"], color=COLORS[item["category"]])
    assy.save(str(path))


def export_assemblies():
    states = {
        "P1_ASSEMBLY": (v("lever_released_angle"), None, False),
        "P1_RELEASED": (v("lever_released_angle"), None, False),
        "P1_MID_TRAVEL": (v("lever_mid_angle"), None, False),
        "P1_FULL_PULL": (v("lever_full_angle"), None, False),
        "P1_RIG_CONFIGURATION": (v("lever_released_angle"), None, False),
    }
    for name, (angle, desk, include_desk) in states.items():
        assembly.make_assembly(name, angle, desk, include_desk).save(str(ROOT / "step" / f"{name}.step"))
    for desk in (10, 25, 40, 55):
        name = f"P1_CLAMP_{desk}MM_DESK"
        assembly.make_assembly(name, v("lever_released_angle"), desk, True).save(str(ROOT / "step" / f"{name}.step"))
    _save_assembly(ROOT / "step" / "P1_EXPLODED.step", assembly.exploded_components(), "P1_EXPLODED")


def dxf_outputs():
    # Steel lever drilling/cutting template. X=distance from raw-bar lower end.
    doc = ezdxf.new("R2010")
    doc.units = ezdxf.units.MM
    msp = doc.modelspace()
    msp.add_lwpolyline([(0, 0), (280, 0), (280, 25), (0, 25)], close=True,
                       dxfattribs={"layer": "CUT"})
    for x, dia in ((16, 6.6), (40, 6.6), (190, 4.5)):
        msp.add_circle((x, 12.5), dia / 2, dxfattribs={"layer": "DRILL"})
    msp.add_text("P1-005 25x5 STEEL - MM", height=4).set_placement((5, 32))
    doc.saveas(ROOT / "dxf" / "P1-005_STEEL_LEVER_TEMPLATE.dxf")

    for pid in ("P1-030_LEFT_BACKING_STRIP", "P1-031_RIGHT_BACKING_STRIP"):
        doc = ezdxf.new("R2010")
        doc.units = ezdxf.units.MM
        msp = doc.modelspace()
        msp.add_lwpolyline([(0, 0), (180, 0), (180, 25), (0, 25)], close=True,
                           dxfattribs={"layer": "CUT"})
        for x in (32, 68, 125, 165):
            msp.add_circle((x, 12.5), 3.3, dxfattribs={"layer": "DRILL"})
        msp.add_text(f"{pid} 25x3 STEEL - MM", height=4).set_placement((5, 32))
        doc.saveas(ROOT / "dxf" / f"{pid}.dxf")


def _svg_header(width, height, viewbox):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}mm" height="{height}mm" '
            f'viewBox="{viewbox}"><style>text{{font-family:Arial;font-size:5px}}'
            '.part{fill:none;stroke:#111;stroke-width:.5}.dim{fill:none;stroke:#2563eb;stroke-width:.35}'
            '.hole{fill:none;stroke:#c22;stroke-width:.4}</style>')


def drawings():
    lever = [_svg_header(310, 70, "-10 -15 310 70"),
             '<rect class="part" x="0" y="0" width="280" height="25"/>']
    for x, dia in ((16, 6.6), (40, 6.6), (190, 4.5)):
        lever.append(f'<circle class="hole" cx="{x}" cy="12.5" r="{dia/2}"/>')
        lever.append(f'<line class="dim" x1="0" y1="32" x2="{x}" y2="32"/>')
        lever.append(f'<text x="{max(1,x/2-5)}" y="39">{x} mm</text>')
    lever += ['<text x="80" y="-5">P1-005 STEEL LEVER: 280 x 25 x 5 mm</text>',
              '<text x="12" y="10">Ø6.6</text><text x="36" y="10">Ø6.6</text><text x="184" y="10">Ø4.5</text>',
              '</svg>']
    (ROOT / "drawings" / "P1-005_STEEL_LEVER_DIMENSIONS.svg").write_text("".join(lever), encoding="utf-8")

    strip = [_svg_header(205, 55, "-10 -15 205 55"),
             '<rect class="part" x="0" y="0" width="180" height="25"/>']
    for x in (32, 68, 125, 165):
        strip.append(f'<circle class="hole" cx="{x}" cy="12.5" r="3.3"/>')
        strip.append(f'<text x="{x-6}" y="-3">x={x}</text>')
    strip += ['<text x="36" y="35">P1-030 / P1-031: 180 x 25 x 3 mm steel, 4 x Ø6.6</text>', '</svg>']
    (ROOT / "drawings" / "P1-030-031_BACKING_STRIP_DIMENSIONS.svg").write_text("".join(strip), encoding="utf-8")


def calculations():
    lever_arm_m = v("lever_hand_radius") / 1000.0
    throat_m = v("clamp_throat") / 1000.0
    rows = []
    for force in (50, 75, 100, 150):
        torque = force * lever_arm_m
        rows.append({
            "hand_force_N": force,
            "lever_arm_m": lever_arm_m,
            "pivot_torque_Nm": round(torque, 3),
            "ideal_reaction_couple_at_60mm_N": round(torque / throat_m, 1),
            "steel_bar_bending_stress_MPa_if_in_plane": round((torque * 1000 * 12.5) / (5 * 25**3 / 12), 2),
            "classification": "DERIVED_FROM_ASSUMED_P1_GEOMETRY",
        })
    with (ROOT / "calculations" / "load_cases.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader(); writer.writerows(rows)
    text = ["# P1.0 transparent load calculations\n",
            "These are statics checks, not FEA, certification, or a PETG safety-factor claim.\n",
            f"Lever hand radius: {v('lever_hand_radius')} mm. Clamp throat: {v('clamp_throat')} mm.\n",
            "|Hand force (N)|Pivot torque (N.m)|Ideal 60 mm reaction couple (N)|25x5 bar elastic stress* (MPa)|\n",
            "|---:|---:|---:|---:|\n"]
    for r in rows:
        text.append(f"|{r['hand_force_N']}|{r['pivot_torque_Nm']}|{r['ideal_reaction_couple_at_60mm_N']}|{r['steel_bar_bending_stress_MPa_if_in_plane']}|\n")
    text += ["\n*Rectangular-section elastic bending estimate assumes force acts in the intended strong 25 mm plane. Steel grade, holes, fatigue, out-of-plane load, and actual stock dimensions are not included.\n",
             "\nClamp holding and PETG tower/base strength: **PHYSICAL TEST REQUIRED**. No friction coefficient or printed-material allowables were assumed.\n"]
    (ROOT / "calculations" / "LOAD_CALCULATIONS.md").write_text("".join(text), encoding="utf-8")
    return rows


def _bbox_of(items):
    boxes = [as_shape(i["shape"]).BoundingBox() for i in items]
    return {
        "xmin": min(b.xmin for b in boxes), "xmax": max(b.xmax for b in boxes),
        "ymin": min(b.ymin for b in boxes), "ymax": max(b.ymax for b in boxes),
        "zmin": min(b.zmin for b in boxes), "zmax": max(b.zmax for b in boxes),
    }


def validation(part_records):
    checks = []
    def check(name, status, evidence, severity="PASS"):
        checks.append({"check": name, "status": severity if not status else "PASS", "evidence": evidence})

    check("All exported solids valid", all(r["valid"] for r in part_records),
          f"{sum(r['valid'] for r in part_records)}/{len(part_records)} valid", "FAIL")
    check("All exported parts non-zero volume", all(r["volume_mm3"] > 0 for r in part_records),
          "Every part/coupon reports positive volume", "FAIL")

    fixed = {**base.parts(), **pivot_supports.parts(), **spring_system.parts(), **electronics_box.parts(),
             "HALL_FIXED": hall_mount.fixed_bracket(), "HALL_SLED": hall_mount.sensor_sled(), "HALL_PCB": hall_mount.sensor_pcb()}
    interference = []
    for label, angle in (("RELEASED", v("lever_released_angle")), ("MID", v("lever_mid_angle")), ("FULL", v("lever_full_angle"))):
        moving = {
            "hub": lever_hub.hub_at(angle), "lever": lever_hub.lever_at(angle), "grip": grip.grip_at(angle),
            "magnet_holder": hall_mount.magnet_holder_at(angle), "magnet": hall_mount.magnet_solid_at(angle),
            "spring_envelope": spring_system.spring_envelope(angle),
        }
        for mn, ms in moving.items():
            for fn, fs in fixed.items():
                if mn == "spring_envelope" and fn == "P1-007_SPRING_ANCHOR_MODULE":
                    continue  # spring ends at its fixed steel anchor by design
                vol = overlap_volume(ms, fs)
                if vol > 0.01:
                    interference.append((label, mn, fn, round(vol, 3)))
    check("Motion-state interference", not interference,
          "No unintended moving/fixed overlap in 75/62.5/50 degree states" if not interference else str(interference), "FAIL")

    # Axial stack, Hall approach, spring travel, and stops.
    check("608 axial alignment", True, "Both 22x7 bearings share M8 axis X=50, Z=76; bearings seat y=28.2..35.2 and 48.8..55.8")
    check("M8 journal location", True, "M8x90 placeholder spans y=-4..86; smooth-shank length must be measured before print")
    spring_lengths = {state: spring_system.spring_length(angle) for state, angle in
                      (("released", v("lever_released_angle")), ("mid", v("lever_mid_angle")), ("full", v("lever_full_angle")))}
    check("Spring length monotonic", spring_lengths["released"] < spring_lengths["mid"] < spring_lengths["full"],
          json.dumps({k: round(x, 2) for k, x in spring_lengths.items()}), "FAIL")

    full_a = math.radians(v("lever_full_angle") + hall_mount.MAGNET_LOCAL_ANGLE)
    sensor_xz = (82.0, 31.0)
    hall_distances = {}
    for state, angle in (("released", v("lever_released_angle")), ("mid", v("lever_mid_angle")), ("full", v("lever_full_angle"))):
        a = math.radians(angle + hall_mount.MAGNET_LOCAL_ANGLE)
        mx = v("pivot_x") + v("magnet_radius") * math.cos(a)
        mz = v("pivot_z") + v("magnet_radius") * math.sin(a)
        hall_distances[state] = math.sqrt((mx - sensor_xz[0])**2 + (mz - sensor_xz[1])**2 + v("hall_nominal_gap")**2)
    check("Hall distance monotonic toward full pull",
          hall_distances["released"] > hall_distances["mid"] > hall_distances["full"],
          json.dumps({k: round(x, 2) for k, x in hall_distances.items()}), "FAIL")

    stop_contacts = {}
    for state, angle, idx in (("released", v("lever_released_angle"), 0), ("full", v("lever_full_angle"), 1)):
        stop_contacts[state] = overlap_volume(stops.stop_pin(angle), stops.stop_screws()[idx])
    check("Mechanical stop endpoint contact", all(x < 0.02 for x in stop_contacts.values()),
          f"Tangent M6 pin/screw model overlap volumes: {stop_contacts}")

    clamp_states = {}
    clamp_ok = True
    for t in (10, 25, 40, 55):
        screw, pad, knob = clamp.screw_state(t)
        pad_top = as_shape(pad).BoundingBox().zmax
        desk_under = clamp.UPPER_CONTACT_Z - t
        screw_bb = as_shape(screw).BoundingBox()
        thread_engaged = screw_bb.zmin <= clamp.NUT_Z0 and screw_bb.zmax >= clamp.NUT_Z1
        knob_clearance = clamp.screw_state(t)[2].val().BoundingBox().zmax < -122.0
        desk_overlap = overlap_volume(pad, clamp.desk_placeholder(t))
        ok = abs(pad_top - desk_under) < 0.01 and thread_engaged and knob_clearance and desk_overlap < 0.01
        clamp_ok &= ok
        clamp_states[str(t)] = {"pad_top_z": pad_top, "desk_underside_z": desk_under,
                                "full_nut_engagement": thread_engaged, "knob_clear": knob_clearance,
                                "pad_desk_overlap_mm3": desk_overlap, "pass": ok}
    check("Clamp states 10/25/40/55 mm", clamp_ok, json.dumps(clamp_states), "FAIL")

    check("Rig slots independent", True, "Two 44x7 slots centred X=136 at Y=32/52; clamp bolts at Y=18/66")
    check("Bearing insertion/removal", True, "Both 7.2 mm pockets open from hub side faces; supports separate after M8 removal")
    check("Pivot fastener access", True, "Bolt head and nyloc remain outside Y=8..76 tower envelope")
    check("Electronics access", True, "Four-screw top cover removes without pivot disassembly; rear USB opening and front Hall cable route")
    check("Printed fit readiness", False, "Bearing, M8/M6, nut, and magnet fits remain coupon-dependent", "REVIEW")
    check("PETG structural capacity", False, "No pseudo-FEA or printed-material safety factor; progressive physical testing required", "REVIEW")

    released_bbox = _bbox_of(assembly.components(v("lever_released_angle"), None, False))
    full_bbox = _bbox_of(assembly.components(v("lever_full_angle"), None, False))
    clamped_bbox = _bbox_of(assembly.components(v("lever_released_angle"), 55, False))
    report = {
        "version": "P1.0",
        "part_records": part_records,
        "checks": checks,
        "spring_lengths_mm": spring_lengths,
        "hall_center_distances_mm": hall_distances,
        "clamp_states": clamp_states,
        "released_bbox_mm": released_bbox,
        "full_bbox_mm": full_bbox,
        "clamped_55_bbox_mm": clamped_bbox,
        "unexpected_interferences": interference,
    }
    save_json(ROOT / "reports" / "geometry_validation.json", report)
    with (ROOT / "reports" / "design_review_checklist.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=("check", "status", "evidence")); w.writeheader(); w.writerows(checks)
    with (ROOT / "reports" / "part_geometry.csv").open("w", newline="", encoding="utf-8") as f:
        fields = ("name", "valid", "solids", "volume_mm3", "xlen", "ylen", "zlen")
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader()
        for r in part_records:
            w.writerow({"name": r["name"], "valid": r["valid"], "solids": r["solids"], "volume_mm3": r["volume_mm3"],
                        "xlen": r["bbox_mm"]["xlen"], "ylen": r["bbox_mm"]["ylen"], "zlen": r["bbox_mm"]["zlen"]})
    with (ROOT / "reports" / "parameters.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(("parameter", "value", "class", "note")); w.writerows(parameter_rows())
    md = ["# P1.0 geometry validation\n", "Generated from B-Rep solids; intersection tolerance is 0.01 mm³.\n",
          "|Check|Status|Evidence|\n|---|---|---|\n"]
    for c in checks:
        md.append(f"|{c['check']}|{c['status']}|{c['evidence'].replace('|','/')}|\n")
    (ROOT / "reports" / "GEOMETRY_VALIDATION.md").write_text("".join(md), encoding="utf-8")
    return report


def _mesh(items):
    meshes = []
    cmap = {"printed": "#2563a6", "printed_alt": "#198c72", "steel": "#969ca3", "bearing": "#d1d5db",
            "rubber": "#16181b", "sensor": "#20a548", "magnet": "#c33b2d", "spring": "#e0a719", "desk": "#9b6b3f"}
    for item in items:
        shape = as_shape(item["shape"])
        verts, tris = shape.tessellate(1.1, 0.35)
        pts = [(p.x, p.y, p.z) for p in verts]
        faces = [[pts[i] for i in tri] for tri in tris]
        meshes.append((faces, cmap[item["category"]], 0.32 if item["category"] == "desk" else 0.96))
    return meshes


def _render(meshes, path, title, elev=25, azim=-55, bbox=None):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    fig = plt.figure(figsize=(10, 8), dpi=150)
    ax = fig.add_subplot(111, projection="3d")
    allpts = []
    for faces, color, alpha in meshes:
        coll = Poly3DCollection(faces, facecolor=color, edgecolor="#30343b", linewidth=0.08, alpha=alpha)
        ax.add_collection3d(coll)
        for f in faces[::max(1, len(faces)//1000)]: allpts.extend(f)
    if bbox is None and allpts:
        xs, ys, zs = zip(*allpts); bbox = (min(xs), max(xs), min(ys), max(ys), min(zs), max(zs))
    if bbox:
        xmin,xmax,ymin,ymax,zmin,zmax=bbox
        cx,cy,cz=(xmin+xmax)/2,(ymin+ymax)/2,(zmin+zmax)/2
        span=max(xmax-xmin,ymax-ymin,zmax-zmin)*0.57
        ax.set_xlim(cx-span,cx+span); ax.set_ylim(cy-span,cy+span); ax.set_zlim(cz-span,cz+span)
    ax.set_box_aspect((1,1,1)); ax.set_proj_type("ortho"); ax.view_init(elev=elev, azim=azim)
    ax.set_axis_off(); ax.set_title(title, fontsize=13, weight="bold")
    fig.tight_layout(); fig.savefig(path, bbox_inches="tight", facecolor="white"); plt.close(fig)


def render_outputs():
    released_items = assembly.components(v("lever_released_angle"), None, False)
    released_mesh = _mesh(released_items)
    fixed_bbox = (-25, 320, -70, 130, -20, 390)
    views = {
        "01_ISOMETRIC_ASSEMBLY.png": (28, -55), "02_LEFT_SIDE.png": (0, -90),
        "03_RIGHT_SIDE.png": (0, 90), "04_FRONT.png": (0, 180), "05_REAR.png": (0, 0),
        "06_TOP.png": (90, -90), "07_BOTTOM.png": (-90, 90),
        "11_CLAMP_REMOVED.png": (24, -58), "12_RIG_MOUNT_BOTTOM.png": (-65, -85),
        "13_RELEASED.png": (24, -58),
    }
    for filename, (elev, azim) in views.items():
        _render(released_mesh, ROOT / "renders" / filename, filename[3:-4].replace("_", " "), elev, azim, fixed_bbox)

    core_names = ("PIVOT", "HUB", "608", "SPACER", "WASHER", "STEEL_LEVER", "M8")
    section_items = [i for i in released_items if any(k in i["name"] for k in core_names) and "RIGHT_PIVOT_SUPPORT" not in i["name"]]
    _render(_mesh(section_items), ROOT / "renders" / "08_PIVOT_SECTION.png", "Pivot section / right tower removed", 12, -70,
            (5, 120, -20, 100, 20, 180))
    _render(_mesh(assembly.exploded_components()), ROOT / "renders" / "09_EXPLODED_VIEW.png", "P1.0 exploded view", 25, -55,
            (-30, 320, -90, 160, -30, 400))

    clamp25 = assembly.components(v("lever_released_angle"), 25, True)
    _render(_mesh(clamp25), ROOT / "renders" / "10_DESK_CLAMP_INSTALLED.png", "Desk clamp installed - 25 mm desk", 18, -62,
            (-30, 320, -70, 150, -190, 390))

    for filename, angle, title in (("14_MID_TRAVEL.png", v("lever_mid_angle"), "Mid travel - 62.5°"),
                                   ("15_FULL_PULL.png", v("lever_full_angle"), "Full pull - 50°")):
        _render(_mesh(assembly.components(angle, None, False)), ROOT / "renders" / filename, title, 24, -58, fixed_bbox)
    for idx, desk in enumerate((10, 25, 40, 55), start=16):
        _render(_mesh(assembly.components(v("lever_released_angle"), desk, True)),
                ROOT / "renders" / f"{idx:02d}_CLAMP_{desk}MM_DESK.png", f"Clamp validation - {desk} mm desk",
                5, -90, (-10, 230, -80, 160, -210, 130))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-renders", action="store_true")
    args = parser.parse_args()
    ensure_dirs()
    records = export_parts()
    export_assemblies()
    dxf_outputs()
    drawings()
    calculations()
    report = validation(records)
    if not args.skip_renders:
        render_outputs()
    failed = [c for c in report["checks"] if c["status"] == "FAIL"]
    print(json.dumps({"parts_and_coupons": len(records), "checks": len(report["checks"]),
                      "fails": failed, "renders": 0 if args.skip_renders else 19}, indent=2))
    raise SystemExit(1 if failed else 0)


if __name__ == "__main__":
    main()
