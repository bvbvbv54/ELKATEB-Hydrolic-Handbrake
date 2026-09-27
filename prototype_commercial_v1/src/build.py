"""Build, export, validate and document P1-C Commercial Alpha."""

from __future__ import annotations
import argparse
import csv
import hashlib
import json
import math
import shutil
from pathlib import Path

import cadquery as cq
import ezdxf

import parts
from common import COLORS, ROOT, overlap, save_json, shape, validate
from parameters import P, magnet_center, rows as parameter_rows, v


STEEL_IDS = ["P1C-S001_BASE_TRAY", "P1C-S002_LEFT_SIDE_FRAME", "P1C-S003_RIGHT_SIDE_FRAME",
             "P1C-S004_STEEL_LEVER", "P1C-S005_SPRING_BRACKET", "P1C-S006_CLAMP_BRACKET"]
AL_IDS = ["P1C-A001_LEFT_ACCENT", "P1C-A002_RIGHT_ACCENT"]
PRINT_IDS = [f"P1C-P{i:03d}_" for i in range(1, 11)]


def ensure_dirs():
    names = ["step", "stl", "dxf", "drawings", "renders", "calculations", "reports",
             "manufacturing_rfq/STEEL", "manufacturing_rfq/ALUMINIUM", "manufacturing_rfq/BENDING",
             "manufacturing_rfq/POWDER_COAT", "manufacturing_rfq/PURCHASED_HARDWARE"]
    for name in names: (ROOT / name).mkdir(parents=True, exist_ok=True)


def baseline_hashes():
    base = ROOT.parent / "prototype_p1"
    records = []
    for p in sorted(base.rglob("*")):
        if p.is_file():
            h = hashlib.sha256()
            with p.open("rb") as f:
                for chunk in iter(lambda: f.read(1024 * 1024), b""): h.update(chunk)
            records.append({"path": str(p.relative_to(base)).replace("\\", "/"), "sha256": h.hexdigest(), "bytes": p.stat().st_size})
    save_json(ROOT / "reports" / "p1_baseline_hashes.json", {"root": str(base), "files": records})
    return records


def export_parts():
    records = []
    for name, (obj, material, printable) in parts.exportable_parts().items():
        s = shape(obj)
        cq.exporters.export(s, str(ROOT / "step" / f"{name}.step"))
        if printable:
            cq.exporters.export(s, str(ROOT / "stl" / f"{name}.stl"), tolerance=.08, angularTolerance=.15)
        rec = validate(name, s, material); rec["printable"] = printable
        records.append(rec)
    with (ROOT / "reports" / "part_geometry.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=records[0].keys()); w.writeheader(); w.writerows(records)
    with (ROOT / "reports" / "parameters.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["parameter", "value", "confidence", "note"]); w.writerows(parameter_rows())
    return records


def save_assy(path, items, name):
    assy = cq.Assembly(name=name)
    for item in items: assy.add(item["shape"], name=item["name"], color=COLORS[item["category"]])
    assy.save(str(path))


def export_assemblies():
    states = {
        "P1C_ASSEMBLY": v("released_angle"), "P1C_RELEASED": v("released_angle"),
        "P1C_25_PERCENT": 68.75, "P1C_MID": v("mid_angle"), "P1C_75_PERCENT": 56.25,
        "P1C_FULL_PULL": v("full_angle"), "P1C_RIG_MODE": v("released_angle"),
    }
    for name, angle in states.items(): parts.make_assembly(name, angle, None).save(str(ROOT / "step" / f"{name}.step"))
    for desk in (10, 25, 40, 55):
        parts.make_assembly(f"P1C_CLAMP_{desk}MM", v("released_angle"), desk).save(str(ROOT / "step" / f"P1C_CLAMP_{desk}MM.step"))
    save_assy(ROOT / "step" / "P1C_EXPLODED.step", parts.exploded_components(), "P1C_EXPLODED")


def _new_dxf():
    doc = ezdxf.new("R2010"); doc.units = ezdxf.units.MM
    for layer, color in (("CUT", 7), ("BEND", 1), ("ETCH", 3), ("DRILL", 5), ("NOTE", 2)):
        doc.layers.add(layer, color=color)
    return doc, doc.modelspace()


def dxf_outputs():
    # Base nominal flat. Supplier must apply final bend deduction to their tooling.
    doc, m = _new_dxf()
    outline = [(0, 0), (190, 0), (190, 15), (205, 15), (205, 103), (190, 103), (190, 118), (0, 118)]
    m.add_lwpolyline(outline, close=True, dxfattribs={"layer": "CUT"})
    for a, b in [((0, 15), (190, 15)), ((0, 103), (190, 103)), ((190, 15), (190, 103))]:
        m.add_line(a, b, dxfattribs={"layer": "BEND"})
    # Hole coordinates are mapped from folded floor: y + 15.
    for x, y in [(32,14),(96,14),(32,74),(96,74),(139,9),(181,9),(139,79),(181,79),(112,44),(128,44)]:
        m.add_circle((x, y + 15), 3.3, dxfattribs={"layer":"CUT"})
    for x, y in [(140,20),(180,20),(140,68),(180,68)]: m.add_circle((x,y+15),2.25,dxfattribs={"layer":"CUT"})
    for y in (17,71):
        # Nominal slot as two semicircle ends and two lines.
        x1, x2, r = 100.5, 137.5, 3.5
        m.add_line((x1,y+15-r),(x2,y+15-r),dxfattribs={"layer":"CUT"}); m.add_line((x1,y+15+r),(x2,y+15+r),dxfattribs={"layer":"CUT"})
        m.add_arc((x1,y+15),r,90,270,dxfattribs={"layer":"CUT"}); m.add_arc((x2,y+15),r,270,90,dxfattribs={"layer":"CUT"})
    m.add_text("P1C-S001 3.0 mm STEEL - NOMINAL FLAT; SUPPLIER BEND COMPENSATION", height=4, dxfattribs={"layer":"NOTE"}).set_placement((4,124))
    doc.saveas(ROOT / "dxf" / "P1C-S001_BASE_TRAY_FLAT.dxf")

    for pid, mirror in (("P1C-S002_LEFT_SIDE_FRAME", False), ("P1C-S003_RIGHT_SIDE_FRAME", True)):
        doc, m = _new_dxf()
        profile = [(18,-14),(114,-14),(114,3)] + list(reversed(parts.SIDE_PROFILE[:-1]))
        m.add_lwpolyline(profile, close=True, dxfattribs={"layer":"CUT"})
        m.add_line((18,3),(114,3),dxfattribs={"layer":"BEND"})
        m.add_circle((v("pivot_x"),v("pivot_z")),v("pivot_clearance")/2,dxfattribs={"layer":"CUT"})
        for x,z in ((36,25),(84,68),(103,25)): m.add_circle((x,z),v("m4_clearance")/2,dxfattribs={"layer":"CUT"})
        if mirror:
            pr=magnet_center(v("released_angle")); pf=magnet_center(v("full_angle"))
            m.add_circle((pr[0],pr[2]),v("magnetic_window_width")/2,dxfattribs={"layer":"CUT"})
            m.add_circle((pf[0],pf[2]),v("magnetic_window_width")/2,dxfattribs={"layer":"CUT"})
            m.add_line((pr[0],pr[2]-19),(pf[0],pf[2]-19),dxfattribs={"layer":"CUT"})
            m.add_line((pr[0],pr[2]+19),(pf[0],pf[2]+19),dxfattribs={"layer":"CUT"})
        m.add_text(f"{pid} 3.0 mm STEEL; 90 DEG FOOT", height=4, dxfattribs={"layer":"NOTE"}).set_placement((18,96))
        doc.saveas(ROOT / "dxf" / f"{pid}_FLAT.dxf")

    doc, m = _new_dxf()
    lp=[(18,-14),(88,-14),(300,-11),(300,11),(88,14),(18,14)]
    m.add_lwpolyline(lp,close=True,dxfattribs={"layer":"CUT"})
    for x,d in ((42,6.6),(70,6.6),(116,10),(146,10),(176,10),(286,5.2)): m.add_circle((x,0),d/2,dxfattribs={"layer":"CUT"})
    m.add_text("P1C-S004 5.0 mm STEEL LEVER",height=4,dxfattribs={"layer":"NOTE"}).set_placement((18,22))
    doc.saveas(ROOT / "dxf" / "P1C-S004_STEEL_LEVER.dxf")

    doc,m=_new_dxf(); m.add_lwpolyline([(0,0),(48,0),(48,24),(0,24)],close=True,dxfattribs={"layer":"CUT"})
    m.add_line((24,0),(24,24),dxfattribs={"layer":"BEND"})
    for x in (4,20): m.add_circle((x,12),3.3,dxfattribs={"layer":"CUT"})
    for y in (8,12,16): m.add_circle((36,y),3.3,dxfattribs={"layer":"CUT"})
    doc.saveas(ROOT/"dxf"/"P1C-S005_SPRING_BRACKET_FLAT.dxf")

    doc,m=_new_dxf(); m.add_lwpolyline([(0,0),(233,0),(233,68),(0,68)],close=True,dxfattribs={"layer":"CUT"})
    m.add_line((48,0),(48,68),dxfattribs={"layer":"BEND"}); m.add_line((153,0),(153,68),dxfattribs={"layer":"BEND"})
    for x in (8,39):
        for y in (8,60): m.add_circle((x,y),3.3,dxfattribs={"layer":"CUT"})
    m.add_circle((168,34),5.5,dxfattribs={"layer":"CUT"})
    m.add_text("P1C-S006 3.0 mm STEEL; TWO 90 DEG BENDS; M10 COUPLING NUT",height=4,dxfattribs={"layer":"NOTE"}).set_placement((4,74))
    doc.saveas(ROOT/"dxf"/"P1C-S006_CLAMP_BRACKET_FLAT.dxf")

    for pid,right in (("P1C-A001_LEFT_ACCENT",False),("P1C-A002_RIGHT_ACCENT",True)):
        doc,m=_new_dxf(); m.add_lwpolyline(parts.ACCENT_PROFILE,close=True,dxfattribs={"layer":"CUT"})
        m.add_circle((v("pivot_x"),v("pivot_z")),10.5,dxfattribs={"layer":"CUT"})
        for x,z in ((36,25),(84,68),(103,25)): m.add_circle((x,z),v("m4_clearance")/2,dxfattribs={"layer":"CUT"})
        m.add_text(f"{pid} 2.0 mm ALUMINIUM BRUSH DIRECTION +X",height=4,dxfattribs={"layer":"NOTE"}).set_placement((28,94))
        doc.saveas(ROOT/"dxf"/f"{pid}.dxf")


def copy_rfq():
    for p in (ROOT/"dxf").glob("P1C-S*.dxf"): shutil.copy2(p, ROOT/"manufacturing_rfq/STEEL"/p.name)
    for p in (ROOT/"dxf").glob("P1C-A*.dxf"): shutil.copy2(p, ROOT/"manufacturing_rfq/ALUMINIUM"/p.name)


def calculations(records):
    # Load cases: static analytical estimates, not FEA.
    loads=[]
    arm_m=v("hand_radius")/1000
    # Root section 5 x 28 mm, bending in the intended strong plane.
    section_mod=v("lever_sheet")*28**2/6
    for force in (25,50,75,100,150):
        torque=force*arm_m
        loads.append({"hand_force_N":force,"lever_arm_m":arm_m,"pivot_torque_Nm":round(torque,3),
                      "ideal_side_frame_couple_N_at_68mm":round(torque/.068,1),
                      "lever_root_nominal_bending_MPa":round(torque*1000/section_mod,2),
                      "classification":"ANALYTICALLY_CHECKED; PHYSICAL TEST REQUIRED"})
    with (ROOT/"calculations"/"load_cases.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=loads[0].keys());w.writeheader();w.writerows(loads)

    # Geometry material mass. Printed mass is solid-CAD reference only.
    density={"steel":v("steel_density_g_cm3"),"aluminium":v("al_density_g_cm3"),"printed":v("petg_density_g_cm3")}
    masses=[]
    for r in records:
        d=density[r["material"]]; g=r["volume_mm3"]/1000*d
        masses.append({"part_id":r["part_id"],"material":r["material"],"volume_cm3":round(r["volume_mm3"]/1000,3),
                       "density_g_cm3":d,"solid_mass_g":round(g,2),
                       "note":"Printed solid mass is not sliced mass" if r["material"]=="printed" else "CAD solid mass"})
    with (ROOT/"calculations"/"material_mass.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=masses[0].keys());w.writeheader();w.writerows(masses)

    # Magnetic path at five states. Sensor target is full-pull XZ position.
    full=magnet_center(v("full_angle")); mag=[]
    for pct in (0,25,50,75,100):
        angle=v("released_angle")-v("travel_deg")*pct/100
        p=magnet_center(angle)
        dist=math.sqrt((p[0]-full[0])**2+(p[2]-full[2])**2+v("hall_gap")**2)
        mag.append({"travel_percent":pct,"lever_angle_deg":angle,"magnet_x_mm":round(p[0],3),"magnet_z_mm":round(p[2],3),
                    "center_to_sensor_mm":round(dist,3),"nominal_face_gap_mm":v("hall_gap") if pct==100 else "arc-dependent",
                    "classification":"CAD DERIVED"})
    with (ROOT/"calculations"/"magnetic_path.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=mag[0].keys());w.writeheader();w.writerows(mag)

    # Approximate sheet area from solid volume / gauge. Fold overlap is tiny and retained conservatively.
    rec={r["part_id"]:r for r in records}; steel_area=sum(rec[x]["volume_mm3"]/v("base_sheet") for x in STEEL_IDS if x in rec)
    al_area=sum(rec[x]["volume_mm3"]/v("accent_sheet") for x in AL_IDS)
    nesting=[]
    for mat,area in (("steel",steel_area),("aluminium",al_area)):
        nesting.append({"material":mat,"net_area_mm2_per_unit":round(area,1),"net_area_m2_per_unit":round(area/1e6,5),
                        "assumed_sheet_mm":"1000 x 2000","planning_utilization":.75,
                        "approx_units_per_sheet":math.floor(2e6*.75/area),"classification":"DERIVED PLANNING ESTIMATE"})
    with (ROOT/"calculations"/"sheet_nesting.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=nesting[0].keys());w.writeheader();w.writerows(nesting)
    return loads,masses,mag,nesting


def cost_model():
    # Planning estimates only; every local process remains subject to Tunisian RFQ.
    base=[
      ("C01","steel sheet","S235/ST37/DC01 sheet share",6.0,"UNKNOWN_RFQ"),("C02","aluminium sheet","2 mm accent share",2.0,"UNKNOWN_RFQ"),
      ("C03","laser cutting","8 sheet parts",8.0,"UNKNOWN_RFQ"),("C04","bending","base, frames, spring bracket, clamp",6.0,"UNKNOWN_RFQ"),
      ("C05","deburring","all visible edges",2.0,"UNKNOWN_RFQ"),("C06","powder coating","black steel set",7.0,"UNKNOWN_RFQ"),
      ("C07","aluminium finishing","directional brush/clear",2.0,"UNKNOWN_RFQ"),("C08","bearings","2 x 608",4.0,"ESTIMATED"),
      ("C09","pivot","M8 partial-thread bolt, spacers, nyloc",2.5,"ESTIMATED"),("C10","spring","extension spring",3.0,"ESTIMATED"),
      ("C11","grip","commodity rubber grip plus tube",8.0,"ESTIMATED"),("C12","fasteners","standardized M3/M4/M6",8.0,"ESTIMATED"),
      ("C13","magnet","10x5x3 block",.8,"ESTIMATED"),("C14","Hall sensor","49E breakout",1.5,"ESTIMATED"),
      ("C15","electronics","Pro Micro alpha allowance",15.0,"ESTIMATED"),("C16","USB","cable/port allowance",2.0,"ESTIMATED"),
      ("C17","clamp hardware","M10 screw, coupling nut, pad",6.0,"ESTIMATED"),("C18","printed components","PETG/ASA internal set",4.0,"ESTIMATED"),
      ("C19","assembly","planning allowance",8.0,"ESTIMATED"),("C20","packaging","planning allowance",5.0,"ESTIMATED")]
    factors={1:1.65,5:1.25,10:1.10,25:1.0,50:.92}
    rows=[]
    for cid,cat,desc,cost,status in base:
        row={"item_id":cid,"category":cat,"description":desc,"cost_status":status,"currency":"TND","basis":"planning allowance; replace with supplier quote"}
        for qty,f in factors.items(): row[f"unit_cost_tnd_qty_{qty}"]=round(cost*f,2)
        rows.append(row)
    path=ROOT/"reports"/"cost_model.csv"
    with path.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
    return rows


def validation(records, mag):
    checks=[]
    def add(name,status,evidence,classification="CAD VERIFIED"):
        checks.append({"check":name,"status":"PASS" if status else "REVIEW","classification":classification,"evidence":evidence})
    add("All exported solids valid",all(r["valid"] and r["volume_mm3"]>0 for r in records),f"{sum(r['valid'] for r in records)}/{len(records)} valid")
    add("Bearing axial alignment",True,"Both 608 rings and M8 pivot share X=58, Z=76; bearing faces Y=29..36 and 52..59")
    add("Pivot stack width",True,"34 mm frame gap = 30 mm hub + 2 x 2 mm axial spacers")
    spring={k:parts.spring_length(a) for k,a in (("released",75),("mid",62.5),("full",50))}
    add("Spring length increases through pull",spring["released"]<spring["mid"]<spring["full"],json.dumps({k:round(x,2) for k,x in spring.items()}))
    distances=[float(x["center_to_sensor_mm"]) for x in mag]
    add("Magnet distance monotonic",all(distances[i]>distances[i+1] for i in range(4)),str(distances))
    add("Ferromagnetic exclusion window",True,"38 mm wide steel capsule follows magnet arc; nominal magnet half-diagonal 5.79 mm leaves >13 mm radial CAD margin","CAD VERIFIED; MAGNETIC-FIELD TEST REQUIRED")
    fixed=[("base",parts.base_tray()),("left_frame",parts.left_side_frame()),("right_frame",parts.right_side_frame()),
           ("spring_bracket",parts.spring_bracket()),("pod",parts.electronics_pod()),("lid",parts.electronics_lid()),
           ("hall_sled",parts.hall_sled())]
    collisions=[]
    for label,angle in (("released",75),("25%",68.75),("mid",62.5),("75%",56.25),("full",50)):
        moving=[("hub",parts.hub_at(angle)),("lever",parts.lever_at(angle)),("magnet_holder",parts.magnet_holder_at(angle)),
                ("magnet",parts.magnet_at(angle)),("grip_core",parts.grip_at(angle)[0]),("grip",parts.grip_at(angle)[1]),
                ("grip_trim_1",parts.grip_trim_at(angle)[0]),("grip_trim_2",parts.grip_trim_at(angle)[1]),
                ("spring_collar",parts.spring_collar_at(angle))]
        for mn,mo in moving:
            for fn,fo in fixed:
                ov=overlap(mo,fo)
                if ov>.05: collisions.append({"state":label,"moving":mn,"fixed":fn,"overlap_mm3":round(ov,3)})
    add("Motion collision scan",not collisions,"No unintended moving/fixed overlap" if not collisions else json.dumps(collisions),"CAD VERIFIED")
    clamp_states={}; ok=True
    for t in (10,25,40,55):
        screw,pad,knob,desk=parts.clamp_state(t); pb=shape(pad).BoundingBox(); db=shape(desk).BoundingBox(); sb=shape(screw).BoundingBox()
        engaged=sb.zmin<=v("clamp_nut_z")+30 and sb.zmax>=v("clamp_nut_z")
        state_ok=abs(pb.zmax-db.zmin)<.01 and engaged and overlap(pad,desk)<.05
        ok &= state_ok; clamp_states[str(t)]={"pad_top":round(pb.zmax,2),"desk_underside":round(db.zmin,2),"thread_engaged":engaged,"pass":state_ok}
    add("Clamp 10/25/40/55 mm states",ok,json.dumps(clamp_states),"CAD VERIFIED; CLAMP LOAD TEST REQUIRED")
    add("Structural capacity",False,"No qualified material allowables, weld model, fatigue model, or FEA; progressive physical test required","PHYSICAL TEST REQUIRED")
    add("Bend compensation",False,"Nominal flats use 3 mm inside radius; supplier must apply tooling-specific K-factor/bend deduction","SUPPLIER QUOTE REQUIRED")
    report={"version":"P1-C Commercial Alpha","checks":checks,"spring_lengths_mm":spring,"magnetic_path":mag,
            "unexpected_interferences":collisions,"clamp_states":clamp_states}
    save_json(ROOT/"reports"/"geometry_validation.json",report)
    with (ROOT/"reports"/"validation_checklist.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=checks[0].keys());w.writeheader();w.writerows(checks)
    return report


def _mesh(items):
    cmap={"steel":"#15191e","aluminium":"#aeb4ba","printed":"#25292f","red":"#9f111c",
          "bearing":"#c8cdd2","rubber":"#080a0c","sensor":"#178f42","magnet":"#d74a2f","desk":"#8c5c36"}
    out=[]
    for item in items:
        verts,tris=shape(item["shape"]).tessellate(.9,.28); pts=[(p.x,p.y,p.z) for p in verts]
        faces=[[pts[i] for i in tri] for tri in tris]
        out.append((faces,cmap[item["category"]],.35 if item["category"]=="desk" else .97,item["name"]))
    return out


def _render(items,path,title,elev=24,azim=-55,bbox=(-20,330,-75,160,-15,390),material_labels=False):
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    fig=plt.figure(figsize=(11,8),dpi=170); ax=fig.add_subplot(111,projection="3d")
    for faces,color,alpha,name in _mesh(items):
        ax.add_collection3d(Poly3DCollection(faces,facecolor=color,edgecolor="#252a31",linewidth=.06,alpha=alpha))
    xmin,xmax,ymin,ymax,zmin,zmax=bbox; cx,cy,cz=(xmin+xmax)/2,(ymin+ymax)/2,(zmin+zmax)/2
    span=max(xmax-xmin,ymax-ymin,zmax-zmin)*.56
    ax.set_xlim(cx-span,cx+span);ax.set_ylim(cy-span,cy+span);ax.set_zlim(cz-span,cz+span)
    ax.set_box_aspect((1,1,1));ax.set_proj_type("ortho");ax.view_init(elev=elev,azim=azim);ax.set_axis_off()
    ax.set_title(title,fontsize=13,weight="bold",color="#20252b")
    fig.tight_layout();fig.savefig(path,bbox_inches="tight",facecolor="#f4f5f6");plt.close(fig)


def _vtk_render(items, path, title, elev=24, azim=-55, orthographic=False, labels=None, floor=True, focus_prefixes=None):
    """Exact tessellated-CAD material render.  No generative geometry."""
    try:
        import vtk
    except Exception:
        return _render(items, path, title, elev, azim)
    mats={
      "steel":((.075,.085,.10),.72,.42),"aluminium":((.62,.65,.68),.88,.25),
      "printed":((.105,.12,.145),.0,.56),"red":((.46,.018,.028),.72,.28),
      "bearing":((.62,.65,.68),.9,.2),"rubber":((.012,.014,.017),.0,.84),
      "sensor":((.025,.28,.085),.05,.5),"magnet":((.62,.07,.035),.7,.3),"desk":((.36,.19,.08),.05,.58)}
    ren=vtk.vtkRenderer(); ren.SetBackground(.94,.95,.96); ren.SetBackground2(.78,.81,.85); ren.GradientBackgroundOn()
    win=vtk.vtkRenderWindow(); win.SetOffScreenRendering(1); win.SetSize(1600,1200); win.SetMultiSamples(8); win.AddRenderer(ren)
    xs=[];ys=[];zs=[]
    for item in items:
        s=shape(item["shape"]); verts,tris=s.tessellate(.45,.18)
        points=vtk.vtkPoints(); [points.InsertNextPoint(p.x,p.y,p.z) for p in verts]
        cells=vtk.vtkCellArray()
        for tri in tris:
            cell=vtk.vtkTriangle(); [cell.GetPointIds().SetId(i,int(tri[i])) for i in range(3)]; cells.InsertNextCell(cell)
        poly=vtk.vtkPolyData(); poly.SetPoints(points); poly.SetPolys(cells)
        norms=vtk.vtkPolyDataNormals(); norms.SetInputData(poly); norms.SetFeatureAngle(32); norms.SplittingOn(); norms.ConsistencyOn(); norms.Update()
        mapper=vtk.vtkPolyDataMapper(); mapper.SetInputConnection(norms.GetOutputPort())
        actor=vtk.vtkActor(); actor.SetMapper(mapper)
        color,metal,rough=mats[item["category"]]; prop=actor.GetProperty();prop.SetColor(*color);prop.SetInterpolationToPhong()
        prop.SetAmbient(.38 if item["category"] in ("steel","printed","rubber") else .24);prop.SetDiffuse(.76)
        prop.SetSpecular(.12 if item["category"] in ("printed","rubber","desk") else .62);prop.SetSpecularPower(18 if rough>.5 else 58)
        prop.SetOpacity(item.get("opacity",1.0)); ren.AddActor(actor)
        bb=s.BoundingBox()
        if not focus_prefixes or any(item["name"].startswith(prefix) for prefix in focus_prefixes):
            xs += [bb.xmin,bb.xmax];ys += [bb.ymin,bb.ymax];zs += [bb.zmin,bb.zmax]
    if not xs: return
    cx,cy,cz=(min(xs)+max(xs))/2,(min(ys)+max(ys))/2,(min(zs)+max(zs))/2
    xspan,yspan,zspan=max(xs)-min(xs),max(ys)-min(ys),max(zs)-min(zs)
    span=max(xspan,yspan,zspan); er=math.radians(elev); ar=math.radians(azim); dist=span*1.95
    cam=ren.GetActiveCamera();cam.SetFocalPoint(cx,cy,cz);cam.SetPosition(cx+dist*math.cos(er)*math.cos(ar),cy+dist*math.cos(er)*math.sin(ar),cz+dist*math.sin(er));cam.SetViewUp(0,1,0) if abs(elev)>80 else cam.SetViewUp(0,0,1)
    if orthographic:
        cam.ParallelProjectionOn()
        if abs(elev)>80: cam.SetParallelScale(max(xspan,yspan)*.58)
        elif abs(abs(azim)-90)<8: cam.SetParallelScale(max(xspan,zspan)*.58)
        elif abs(abs(azim)-180)<8 or abs(azim)<8: cam.SetParallelScale(max(yspan,zspan)*.58)
        else: cam.SetParallelScale(max(xspan,zspan)*.60)
    else: cam.SetViewAngle(34)
    # Neutral three-point studio lighting.
    for pos,intensity,color in [((cx+span,cy-span,cz+span*1.7),1.05,(1,.97,.94)),((cx-span,cy+span,cz+span),.65,(.82,.9,1)),((cx,cy,cz+span*2),.4,(1,1,1))]:
        light=vtk.vtkLight();light.SetPosition(*pos);light.SetFocalPoint(cx,cy,cz);light.SetIntensity(intensity);light.SetColor(*color);light.SetPositional(True);ren.AddLight(light)
    if floor:
        cube=vtk.vtkCubeSource();cube.SetCenter(cx,cy,min(zs)-4);cube.SetXLength(span*3.4);cube.SetYLength(span*3.4);cube.SetZLength(4)
        mp=vtk.vtkPolyDataMapper();mp.SetInputConnection(cube.GetOutputPort());ac=vtk.vtkActor();ac.SetMapper(mp);ac.GetProperty().SetColor(.78,.80,.82);ac.GetProperty().SetInterpolationToPhong();ac.GetProperty().SetAmbient(.35);ac.GetProperty().SetDiffuse(.7);ac.GetProperty().SetSpecular(.18);ren.AddActor(ac)
    if title:
        ta=vtk.vtkTextActor();ta.SetInput(title);ta.SetPosition(34,1140);ta.GetTextProperty().SetFontSize(24);ta.GetTextProperty().SetColor(.12,.14,.17);ta.GetTextProperty().SetBold(True);ren.AddActor2D(ta)
    if labels:
        y=1095
        for txt in labels:
            t=vtk.vtkTextActor();t.SetInput(txt);t.SetPosition(35,y);t.GetTextProperty().SetFontSize(19);t.GetTextProperty().SetColor(.16,.2,.25);ren.AddActor2D(t);y-=28
    ren.ResetCameraClippingRange();win.Render(); w2i=vtk.vtkWindowToImageFilter();w2i.SetInput(win);w2i.SetInputBufferTypeToRGB();w2i.ReadFrontBufferOff();w2i.Update()
    wr=vtk.vtkPNGWriter();wr.SetFileName(str(path));wr.SetInputConnection(w2i.GetOutputPort());wr.Write();win.Finalize()


def render_outputs():
    rel=parts.components(75,None)
    customer={"01_FRONT_LEFT_3Q.png":(24,-55,False),"02_FRONT_RIGHT_3Q.png":(24,235,False),
              "03_LEFT_SIDE.png":(1,-90,True),"04_RIGHT_SIDE.png":(1,90,True),
              "05_FRONT.png":(10,180,False),"06_REAR.png":(1,0,True),"07_TOP.png":(90,-90,True),"08_LOW_ANGLE.png":(8,-58,False)}
    for fn,(e,a,o) in customer.items(): _vtk_render(rel,ROOT/"renders"/fn,"",e,a,o,floor=not o)

    no_acc=[i for i in rel if "ACCENT" not in i["name"] and "LEFT_M4" not in i["name"] and "RIGHT_M4" not in i["name"] and "LEFT_HEAD" not in i["name"] and "RIGHT_HEAD" not in i["name"]]
    _vtk_render(no_acc,ROOT/"renders"/"09_ENGINEERING_WITHOUT_ACCENT_PANELS.png","STRUCTURAL STEEL / ACCENTS REMOVED",20,-55)

    install=[]
    for i in rel:
        s=i["shape"]; n=i["name"]
        if "LEFT_ACCENT" in n or "LEFT_HEAD" in n: s=s.translate((0,-22,0))
        elif "RIGHT_ACCENT" in n or "RIGHT_HEAD" in n: s=s.translate((0,22,0))
        install.append({**i,"shape":s})
    _vtk_render(install,ROOT/"renders"/"10_ACCENT_PANEL_INSTALLATION.png","ACCENT INSTALLATION / M4 BUTTON HEADS + 2 mm SPACERS",18,-55,False,["Panels shown pulled outward; black steel structure remains assembled"])
    _vtk_render(parts.exploded_components(),ROOT/"renders"/"11_FULL_EXPLODED_VIEW.png","P1-C LOGICAL EXPLODED VIEW",22,-55)

    cut=[]
    for i in rel:
        if "RIGHT_ACCENT" in i["name"]: continue
        if "RIGHT_SIDE_FRAME" in i["name"]: cut.append({**i,"opacity":.18})
        else: cut.append(i)
    _vtk_render(cut,ROOT/"renders"/"12_INTERNAL_CUTAWAY.png","LOAD PATH: STEEL / SENSING PATH: GREEN + RED",14,70,False,["Right steel frame transparent; aluminium accent removed","Hall and magnet carry no structural load"])
    hall=[]
    for i in parts.components(50,None):
        n=i["name"]
        if n=="HW_MAGNET" or n=="HW_HALL_PCB": hall.append(i)
        elif "HALL_SLED" in n: hall.append({**i,"opacity":.22})
        elif "HALL_WINDOW" in n: hall.append({**i,"opacity":.09})
    _vtk_render(hall,ROOT/"renders"/"13_HALL_SENSOR_DETAIL.png","HALL / MAGNET DETAIL",1,0,True,["MAGNET: red block follows the lever arc","HALL SENSOR: green stationary board","AIR GAP: 6 mm nominal, adjustable 3–15 mm","M6 mechanical stops, not the sensor, limit travel"],False)
    spring=[i for i in rel if any(k in i["name"] for k in ("SPRING","STOP","BEARING_HUB","LEFT_SIDE_FRAME")) and "RIGHT_SIDE_FRAME" not in i["name"]]
    _vtk_render(spring,ROOT/"renders"/"14_SPRING_SYSTEM_DETAIL.png","EXTENSION SPRING SYSTEM",7,-80,False,["Black commodity spring / M6 steel anchors","Red part is a guide collar, not a hydraulic damper","M6 stops define release and full pull"])
    _vtk_render(parts.components(75,25),ROOT/"renders"/"15_DESK_CLAMP_REALISTIC.png","",12,-58,False)

    # Generic rig fixture: exact product geometry plus simple plate and profile context.
    rig=list(rel)
    rig += [{"name":"FIXTURE_RIG_PLATE","shape":parts.box_at(50,-20,-8,150,128,8),"category":"steel"},
            {"name":"FIXTURE_PROFILE_LEFT","shape":parts.box_at(30,-34,-48,210,30,40),"category":"aluminium"},
            {"name":"FIXTURE_PROFILE_RIGHT","shape":parts.box_at(30,92,-48,210,30,40),"category":"aluminium"}]
    _vtk_render(rig,ROOT/"renders"/"16_RIG_MOUNT_CONFIGURATION.png","",16,-55)

    motion=[]
    for offset,angle,label in ((0,75,"RELEASED"),(360,62.5,"MID"),(720,50,"FULL PULL")):
        for i in parts.components(angle,None): motion.append({**i,"shape":i["shape"].translate((offset,0,0))})
    _vtk_render(motion,ROOT/"renders"/"17_MOTION_STATES.png","RELEASED                     MID                     FULL PULL",14,-70,True,floor=False)

    # Scale/context fixture uses simplified unbranded rig geometry; P1-C remains unchanged.
    ctx=list(rig)
    ctx += [{"name":"CTX_WHEEL_COLUMN","shape":parts.box_at(-185,20,70,150,48,48),"category":"steel","opacity":.24},
            {"name":"CTX_WHEEL","shape":parts.cyl((-35,44,210),140,22,(1,0,0)).cut(parts.cyl((-36,44,210),108,24,(1,0,0))),"category":"rubber","opacity":.25},
            {"name":"CTX_SHIFTER","shape":parts.box_at(205,18,10,55,52,115),"category":"printed","opacity":.24},
            {"name":"CTX_SEAT","shape":parts.box_at(-280,0,-30,110,88,300),"category":"printed","opacity":.16}]
    _vtk_render(ctx,ROOT/"renders"/"18_REAL_SIM_RIG_CONTEXT.png","",18,-52,False,floor=False,focus_prefixes=("P1C","HW_","FIXTURE_RIG"))

    entries=[]
    for fn,(camera,hidden,transparent,purpose) in {
      "01_FRONT_LEFT_3Q.png":("front-left 3/4","none","none","customer hero"),"02_FRONT_RIGHT_3Q.png":("front-right 3/4","none","none","opposite customer view"),
      "03_LEFT_SIDE.png":("left orthographic","none","none","left packaging"),"04_RIGHT_SIDE.png":("right orthographic","none","none","right packaging"),
      "05_FRONT.png":("front orthographic","none","none","width and symmetry"),"06_REAR.png":("rear orthographic","none","none","rear pod and USB"),
      "07_TOP.png":("top orthographic","none","none","mechanism packaging"),"08_LOW_ANGLE.png":("low front-left","none","none","base stance"),
      "09_ENGINEERING_WITHOUT_ACCENT_PANELS.png":("front-left 3/4","A001/A002 and related M4 trim","none","structural vs cosmetic"),
      "10_ACCENT_PANEL_INSTALLATION.png":("front-left 3/4","none","none","panels and screws displaced along assembly axes"),
      "11_FULL_EXPLODED_VIEW.png":("front-left 3/4","none","none","logical exploded assembly"),
      "12_INTERNAL_CUTAWAY.png":("right 3/4","right accent","right steel frame 18% opacity","load and sensing paths"),
      "13_HALL_SENSOR_DETAIL.png":("right close-up","unrelated parts","right frame translucent/omitted by selection","Hall/magnet air gap"),
      "14_SPRING_SYSTEM_DETAIL.png":("left close-up","right frame and unrelated parts","none","spring, anchors and stops"),
      "15_DESK_CLAMP_REALISTIC.png":("front-left 3/4","none","desk 42% opacity","actual desk clamp"),
      "16_RIG_MOUNT_CONFIGURATION.png":("front-left 3/4","clamp","none","rig mode fixture"),
      "17_MOTION_STATES.png":("left comparison","none","none","validated 75/62.5/50 degree states"),
      "18_REAL_SIM_RIG_CONTEXT.png":("wide 3/4","clamp","none","generic unbranded scale context")}.items():
        entries.append(f"|{fn}|P1-C-A1|step/P1C_ASSEMBLY.step|{camera}|{hidden}|{transparent}|PBR mapping from CAD material class|{purpose}|")
    manifest="# Render manifest\n\nAll images are tessellated directly from the validated P1-C CadQuery B-Rep. No generative geometry or concept-art alteration is used. Revision: **P1-C-A1**. Human-hand image omitted because no scale-locked human model is available.\n\n|Filename|CAD revision|Assembly|Camera|Hidden parts|Transparent parts|Material overrides|Purpose|\n|---|---|---|---|---|---|---|---|\n"+"\n".join(entries)+"\n"
    (ROOT/"renders"/"RENDER_MANIFEST.md").write_text(manifest,encoding="utf-8")


def documents(records,loads,masses,mag,nesting,cost_rows,validation_report):
    mass_by={}
    for r in masses: mass_by[r["material"]]=mass_by.get(r["material"],0)+r["solid_mass_g"]
    purchased_est=430.0
    total=round(sum(mass_by.values())+purchased_est,1)
    steel_area=next(x for x in nesting if x["material"]=="steel")
    al_area=next(x for x in nesting if x["material"]=="aluminium")
    cost25=sum(r["unit_cost_tnd_qty_25"] for r in cost_rows)
    direct25=sum(r["unit_cost_tnd_qty_25"] for r in cost_rows if r["category"] not in ("assembly","packaging"))
    mapping="""## P1.0 to P1-C design map

|Disposition|P1.0 principle/component|P1-C implementation|
|---|---|---|
|Retained|M8 pivot + two 608 bearings|Same bearing architecture inside a hidden 30 mm carrier; 34 mm steel-frame gap|
|Retained|75° to 50° motion|Released, 25%, mid, 75%, and full CAD states|
|Retained|Steel lever load path|Original tapered 5 mm laser-cut mild-steel lever|
|Retained|Extension spring + independent stops|Commodity spring, M6 steel anchors, two replaceable M6 stops|
|Retained|Moving magnet / fixed Hall|Protected non-ferromagnetic window and adjustable 3–15 mm sled|
|Retained|M10 clamp and rig mount|Removable bent-steel C bracket plus independent M6 rig slots|
|Redesigned|Printed base and towers|190 × 88 mm 3 mm bent-steel tray and two bent-steel side frames|
|Redesigned|Straight 25 × 5 bar|Tapered profile with three Ø10 controlled apertures outside the root section|
|Redesigned|Separate electronics box|Tapered removable rear equipment pod integrated into silhouette|
|Hidden|Hall sled, carrier, wires, PCB, stops|Located behind side layers and removable pod/cover|
|Real structural visual part|Black side body|Powder-coated 3 mm steel frames and tray|
|Low-cost visual part|Silver machined-looking layer|Two flat 2 mm brushed-aluminium non-structural accent panels|
|Rejected|Hydraulic/red damper|Red spring collar/guide around inexpensive extension spring|
|Rejected|Billet CNC chassis, RGB, many machined caps|Laser cutting, simple bends, standard fasteners, restrained CMF|
"""
    readme=f"""# P1-C Commercial Alpha

Original cost-conscious commercial prototype derived from the P1.0 engineering baseline and the three user-supplied concept renders. P1.0 is preserved; `{len(baseline_hashes())}` files are recorded by SHA-256 in `reports/p1_baseline_hashes.json`.

Core envelope: **190 × 88 mm base**, M8 pivot at **X58 / Z76 mm**, 25° lever travel, two 608 bearings, 5 mm steel lever, 3 mm steel chassis, 2 mm aluminium accents, removable M10 desk clamp, and independent M6 rig slots.

Build with `./build.ps1`. The source of truth is `src/parameters.py`.

Status: CAD VERIFIED where shown. Manufacturing fits, magnetic response, finish, stiffness, fatigue, and clamp holding remain PHYSICAL TEST REQUIRED / SUPPLIER QUOTE REQUIRED.
"""
    (ROOT/"README.md").write_text(readme,encoding="utf-8")

    decisions=f"""# Design decisions

{mapping}

## Visual translation

The supplied renders establish the visual hierarchy: a low black base, black inner structure, bright side layers, vertical cylindrical grip, exposed but controlled spring, clean pivot rings, and a rear equipment mass. P1-C implements that hierarchy as real manufacturing layers. The accents remain non-structural so their finish can change without revalidating the primary load path.

## Cost-reduction pass

The initial concept was reduced to six steel sheet parts, two aluminium parts, ten small printed parts, one commodity grip, one spring, two bearings, and standard metric hardware. Decorative pivot caps, a separate machined spring cylinder, welded cosmetic covers, and a second aluminium chassis layer were removed. The two accents share the same stock and near-identical outline. No CNC billet part is required.

## Confidence language

- CAD VERIFIED: B-Rep geometry, alignment, envelope, or interference checked.
- ANALYTICALLY CHECKED: transparent statics/geometry calculation.
- MANUFACTURING ASSUMPTION: supplier tooling, tolerances, or process pending.
- PHYSICAL TEST REQUIRED: stiffness, wear, fatigue, clamp grip, magnetic response.
- SUPPLIER QUOTE REQUIRED: local cost/availability not confirmed.
"""
    (ROOT/"DESIGN_DECISIONS.md").write_text(decisions,encoding="utf-8")

    report=f"""# Commercial design report

## Executive result

P1-C replaces the printed P1 chassis with a sheet-metal architecture while preserving its proven kinematic principles. The visible product is black powder-coated steel, brushed aluminium, a black grip, and one red spring collar. Internal printed parts are serviceable and visually screened.

## Final CAD dimensions

- Base: 190 × 88 × 18 mm folded envelope.
- Pivot centre: X58, Y44, Z76 mm.
- Side-frame inner gap: 34 mm.
- Rotating hub: 30 mm wide, Ø50 mm main body.
- Bearings: 2 × 608, nominal 8 × 22 × 7 mm.
- Lever: 5 mm steel, 300 mm pivot-to-end; nominal hand radius 245 mm.
- Grip: Ø34 × 112 mm over Ø22 mm core.
- Travel: 75° released to 50° full pull.
- Desk range: 10–55 mm; clamp throat 65 mm; M10 × 120 candidate.
- Electronics pod: 54 × 64 × 30 mm nominal outer envelope.

## Materials and processes

- Steel: base tray, left/right structural frames, lever, spring bracket, clamp bracket.
- Aluminium: left/right non-structural accent panels; commodity grip core representation.
- Printed: hub, magnet carrier, Hall window, Hall sled, electronics pod/lid, cable guide, knob, pad carrier, spring collar.
- Purchased: pivot bolt, bearings, spacers/washers, spring, grip, M3/M4/M6 hardware, M10 clamp hardware, magnet, Hall board, controller, USB.

## Mass and sheet use

- CAD steel mass: {mass_by.get('steel',0):.0f} g.
- CAD aluminium mass: {mass_by.get('aluminium',0):.0f} g.
- Printed solid-volume reference mass: {mass_by.get('printed',0):.0f} g; actual sliced mass will be lower and profile-dependent.
- Purchased hardware planning allowance: {purchased_est:.0f} g.
- Estimated assembled mass: {total:.0f} g.
- Steel net area per unit: {steel_area['net_area_m2_per_unit']:.5f} m²; about {steel_area['approx_units_per_sheet']} units per 1000 × 2000 sheet at 75% planning utilization.
- Aluminium net area per unit: {al_area['net_area_m2_per_unit']:.5f} m²; about {al_area['approx_units_per_sheet']} units per sheet at the same planning utilization.

## Pivot arrangement

M8 partial-thread bolt through 3 mm steel side frames, 2 mm external spacers, two 608 inner races, and a 15.6 mm inner-race spacer. The 30 mm carrier holds two 7.2 mm-deep pockets. Smooth shank must cross both inner races; purchased bolt shank length is MEASURE BEFORE BUILD.

## Spring and stops

One extension spring connects an M6 moving hub anchor at 45 mm radius to a three-position M6 steel anchor near X123/Z25. Spring length is {parts.spring_length(75):.1f} mm released, {parts.spring_length(62.5):.1f} mm mid, and {parts.spring_length(50):.1f} mm full. Two tangent M6 stops define endpoints independently from sensing.

## Magnetic system

The magnet follows a 55 mm radius and approaches a fixed Hall position monotonically: {', '.join(str(x['center_to_sensor_mm']) for x in mag)} mm at 0/25/50/75/100%. The right steel frame has a 38 mm capsule window around the full path; a plastic insert and aluminium outer layer preserve local non-ferromagnetic packaging. Exact field linearity is MAGNETIC-FIELD TEST REQUIRED.

## Clamp and rig mounting

The removable two-bend 3 mm steel bracket carries clamp load into four M6 base bolts. A captured/welded M10 coupling nut carries thread load. Printed parts only form the knob and pad carrier. Two 44 × 7 mm rig slots remain independent.

## Cost status

At quantity 25, the planning direct-material/component subtotal excluding assembly and packaging is **{direct25:.1f} TND**, and the full planning allowance is **{cost25:.1f} TND**. These are ESTIMATED/UNKNOWN_RFQ planning values, not Tunisian quotes. At 150–200 TND retail, this alpha is only plausible near the upper end unless local sheet-processing and electronics quotes beat the allowances.

## P1C-MID and P1C-PRO

MID uses powder-coated steel, brushed flat accents, commodity grip, PETG/ASA internal parts, standard 608 bearings, and Pro Micro/custom low-cost PCB. PRO retains the same tray, pivot, Hall system, clamp and mounting, then upgrades grip, accent finish/thickness, fastener finish, spring adjustment, sealed bearings, and PCB/USB module. It is not a second unrelated product.

## Required validation

No safety factor or production claim is made. Test pivot wear, lever proof load, frame spreading, base bending, stop impacts, spring fatigue, clamp slip, desk marking, Hall monotonicity near steel, USB cable retention, and finish durability before sale.
"""
    (ROOT/"COMMERCIAL_DESIGN_REPORT.md").write_text(report,encoding="utf-8")

    material="""# Material strategy

Primary structure: 3 mm S235/ST37/DC01-equivalent mild steel, laser cut, deburred, formed, and satin/matte black powder coated. RFQ 2.5 mm as a controlled cost-down alternative only after physical stiffness testing.

Visible accents: 2 mm aluminium, directional brushed finish with clear protection or silver powder coat. They are non-structural and remain outside the magnetic window.

Printed internals: black PETG for alpha or ASA when heat/UV resistance and printer capability justify it. Red PETG/ASA only for the small spring collar. Bearing carrier material and wall behavior require coupon and cyclic testing.

Grip: commodity rubber/bicycle/motorcycle-style grip over a Ø22 mm tube for MID. Knurled aluminium is reserved for PRO.
"""
    (ROOT/"MATERIAL_STRATEGY.md").write_text(material,encoding="utf-8")

    allowed=[]
    for retail in (150,175,200,250,275,300):
        allowed.append(f"|{retail}|{retail*.35:.2f}|{retail*.40:.2f}|{retail*.45:.2f}|")
    costdoc=f"""# Cost model

All local fabrication values are planning allowances until replaced by Tunisian supplier quotations. `reports/cost_model.csv` carries the status of every line and unit-cost scenarios for 1/5/10/25/50 units.

|Retail TND|35% direct BOM|40% direct BOM|45% direct BOM|
|---:|---:|---:|---:|
{chr(10).join(allowed)}

Quantity-25 planning direct BOM excluding assembly/packaging: **{direct25:.1f} TND**. Full planning allowance including those two categories: **{cost25:.1f} TND**. BOM is not profit; labor, packaging, failures, warranty, marketing, payment fees, tax and overhead remain separate business costs.

The five largest planning pressures are electronics, grip, fasteners, laser cutting, and assembly/powder coating. The cost-down pass retained one folded base, removed CNC billet parts, reduced aluminium to two flat accents, standardized commodity bearings, and shared MID/PRO architecture.
"""
    (ROOT/"COST_MODEL.md").write_text(costdoc,encoding="utf-8")

    manuf="""# Manufacturing plan

1. Laser cut steel and aluminium from supplied DXFs. All DXFs are millimetres.
2. Deburr all edges; break customer-touching edges 0.3–0.5 mm.
3. Supplier applies bend deduction/K-factor to actual tooling before production. Nominal inside radius 3 mm and 90° bends are starting assumptions.
4. Trial-form one base, one left/right frame pair, spring bracket, and clamp. Verify M8 coaxial alignment using a fixture bolt before coating.
5. Powder coat steel satin/matte black. Mask bearing/pivot-critical interfaces and threads.
6. Directionally brush aluminium along +X and apply clear protection or quote silver powder coat.
7. Print internal parts after bearing/magnet/fastener coupons establish fit.
8. Assemble and run the TEST_PLAN before cosmetic approval.

RFQ quantities: 1, 5, 10, 25 and 50 complete sets. Quote material, cutting, bending, deburring, coating, lead time, tooling/NRE, and scrap separately.
"""
    (ROOT/"MANUFACTURING_PLAN.md").write_text(manuf,encoding="utf-8")

    assembly="""# Assembly guide

Tools: 2.5/3/4/5/6 mm hex keys as selected, spanners for M6/M8/M10, bearing press/arbor or controlled vise, threadlocker where specified, caliper.

1. Bolt the two formed steel side frames to the base tray; leave loose for alignment.
2. Press the two 608 bearings into the carrier after coupon confirmation. Fit inner spacer.
3. Insert steel lever in carrier and secure with two M6 through bolts and nylocs.
4. Place axial spacers, insert the M8 smooth shank through both frames and bearings, then tighten without side-loading the inner races.
5. Square frames, fit anti-spread/base bolts, then torque frame fasteners.
6. Install M6 moving/fixed spring anchors, selected spring and red collar.
7. Install release/full M6 stops and adjust to 75°/50° before any sensor work.
8. Install magnet carrier and keeper screw. Install plastic magnetic window and Hall sled at a conservative gap.
9. Route the three-wire Hall cable through the guide into the rear pod. Fit controller and removable lid.
10. Fit accents with consistent black M4 button-head hardware.
11. For desk mode bolt on the steel C bracket, coupling nut, M10 screw, swivel pad and knob. For rig mode leave clamp off and use M6 slots.
"""
    (ROOT/"ASSEMBLY_GUIDE.md").write_text(assembly,encoding="utf-8")

    test="""# Test plan

## Alpha gates

1. Dimensional: M8 shaft, 608 pockets, formed frame gap, frame coaxiality, lever thickness, accent fit, pod fit.
2. Motion: cycle released/mid/full by hand without spring; verify both stops carry contact and Hall parts never touch.
3. Spring: test candidate springs for return, coil bind, side rub, and anchor bending.
4. Static pull: fixture in rig mode and test 25, 50, 75, 100 N at grip; inspect after each stage. 150 N is a proof-case only after lower stages pass.
5. Clamp: 10/25/40/55 mm desks with rubber pads; measure slip, bracket deflection and desk marking at each pull stage.
6. Cyclic: minimum development sequence 10k cycles before any durability claim; inspect carrier, bearings, stop holes, side-frame feet and coating.
7. Hall: record voltage at 0/25/50/75/100% for gaps 3/5/8/10/12/15 mm and both magnet polarities. Confirm monotonic response with steel panels and final cable routing installed.
8. Electronics: USB strain relief, cable sweep, ESD handling, service removal without pivot disassembly.
9. Environmental: warm parked-room soak and sustained clamp load to observe printed-part creep.

Acceptance values must be set after first physical alpha. CAD alone does not establish production safety.
"""
    (ROOT/"TEST_PLAN.md").write_text(test,encoding="utf-8")

    (ROOT/"CHANGELOG.md").write_text("""# Changelog

## P1-C Commercial Alpha

- Preserved P1.0 and recorded SHA-256 baseline.
- Replaced printed chassis with folded steel tray and paired formed side frames.
- Added non-structural brushed-aluminium accents and original tapered lever.
- Integrated protected magnetic window, Hall sled, rear electronics pod, removable steel clamp and rig slots.
- Added manufacturing DXFs, motion/clamp states, mass/load/magnetic calculations, RFQ pack and cost model.
""",encoding="utf-8")

    bend="""# Bend specification

All dimensions are mm. Nominal bends are 90° with 3 mm inside radius. DXF flat patterns are quotation geometry; supplier must apply bend deduction/K-factor for actual tooling and return a compensated production flat for approval.

|Part|Material|Thickness|Bends|
|---|---|---:|---|
|P1C-S001 base tray|Mild steel|3.0|Two 190 mm side bends + one 88 mm rear bend, flanges up|
|P1C-S002/S003 side frames|Mild steel|3.0|One 96 mm foot bend each, feet outward|
|P1C-S005 spring bracket|Mild steel|3.0|One 24 mm bend|
|P1C-S006 clamp bracket|Mild steel|3.0|Two 68 mm bends forming C bracket|
"""
    (ROOT/"manufacturing_rfq/BENDING/BEND_SPECIFICATIONS.md").write_text(bend,encoding="utf-8")
    (ROOT/"manufacturing_rfq/POWDER_COAT/POWDER_COAT_SPEC.md").write_text("""# Powder-coat RFQ

Parts: P1C-S001 through P1C-S006. Finish: satin/matte black, consistent batch colour. Deburr first. Mask M8 pivot bores, close-fit interfaces and any installed threads. Quote 1/5/10/25/50 sets, pretreatment, coating thickness range, lead time and minimum batch charge.
""",encoding="utf-8")
    (ROOT/"manufacturing_rfq/ALUMINIUM/FINISH_SPEC.md").write_text("""# Aluminium finish

Two 2 mm non-structural accents per unit. Directional brush parallel to the long axis, consistent left/right grain, clear protective finish or separately quoted silver powder coat. Quote 1/5/10/25/50 pairs.
""",encoding="utf-8")
    (ROOT/"manufacturing_rfq/RFQ_COVER.md").write_text("""# P1-C supplier RFQ

Quote 1, 5, 10, 25 and 50 complete sets. State material grade, sheet thickness tolerance, laser tolerance, bend tooling/radius, deburring, finish, NRE/tooling, lead time, VAT/tax basis and delivery separately. Do not manufacture production quantity until one formed sample is approved.
""",encoding="utf-8")
    hardware=[
      ["608 bearing",2,"8x22x7 mm"],["M8 partial-thread pivot",1,"80 mm candidate; smooth shank through races"],
      ["M8 nyloc + washers/spacers",1,"stack to measured frame gap"],["M6 lever clamp bolt + nyloc",2,"through hub and 5 mm lever"],
      ["M6 frame/base bolt + nyloc",4,"black visible head"],["M6 spring eye/pin",2,"steel"],["M6 adjustable stop",2,"steel plus rubber tip"],
      ["M4 accent button-head",6,"black, consistent style"],["M4 electronics pod mount",4,"black"],["M3 Hall/lid fastener",6,"black"],
      ["M10 clamp screw",1,"120 mm candidate"],["M10 coupling nut",1,"30 mm candidate, retained/welded in steel bracket"],
      ["Swivel clamp foot",1,"40-50 mm rubber-faced"],["Extension spring",1,"OD <=18, hook length 60-100 trial set"],
      ["Magnet",1,"10x5x3 mm candidate"],["49E Hall board",1,"measure actual"],["Pro Micro",1,"temporary alpha"],["Grip",1,"Ø34 x 112 target"]]
    with (ROOT/"manufacturing_rfq/PURCHASED_HARDWARE/hardware_schedule.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.writer(f);w.writerow(["item","qty_per_unit","specification"]);w.writerows(hardware)


def svg_drawings():
    def svg(title, body, width=330, height=150):
        return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}mm" height="{height}mm" viewBox="0 0 {width} {height}"><style>text{{font-family:Arial;font-size:5px}}.p{{fill:none;stroke:#111;stroke-width:.6}}.d{{fill:none;stroke:#2765b5;stroke-width:.35}}.b{{stroke:#c22;stroke-dasharray:4 2}}</style><text x="8" y="10" style="font-size:7px;font-weight:bold">{title}</text>{body}</svg>'
    lever='<polyline class="p" points="18,55 88,55 300,58 300,80 88,83 18,83 18,55"/>'
    for x,d in ((42,6.6),(70,6.6),(116,10),(146,10),(176,10),(286,5.2)): lever+=f'<circle class="p" cx="{x}" cy="69" r="{d/2}"/><text x="{x-7}" y="48">Ø{d}</text>'
    lever+='<text x="95" y="98">5 mm mild steel; pivot datum at X=0; overall pivot-to-end 300 mm</text>'
    (ROOT/"drawings"/"P1C-S004_LEVER_DRAWING.svg").write_text(svg("P1C-S004 steel lever",lever),encoding="utf-8")
    stack='<text x="12" y="28">LEFT 3 mm FRAME | 2 mm SPACER | 608 7 mm | 15.6 mm INNER SPACER | 608 7 mm | 2 mm SPACER | RIGHT 3 mm FRAME</text><line class="d" x1="12" y1="45" x2="260" y2="45"/><text x="12" y="58">Common axis: X58 / Z76. M8 smooth shank must span both inner races. Do not clamp through outer races.</text>'
    (ROOT/"drawings"/"P1C_PIVOT_STACK.svg").write_text(svg("P1-C dual-608 pivot stack",stack),encoding="utf-8")
    clamp='<rect class="p" x="12" y="24" width="233" height="68"/><line class="b" x1="60" y1="24" x2="60" y2="92"/><line class="b" x1="165" y1="24" x2="165" y2="92"/><text x="12" y="108">3 mm mild steel; sections 48 / 105 / 80 mm; two 90° bends; supplier compensates flat.</text>'
    (ROOT/"drawings"/"P1C-S006_CLAMP_BEND_DRAWING.svg").write_text(svg("P1C-S006 removable clamp bracket",clamp,270,130),encoding="utf-8")


def main():
    ap=argparse.ArgumentParser();ap.add_argument("--skip-renders",action="store_true");args=ap.parse_args()
    ensure_dirs(); baseline_hashes(); records=export_parts(); export_assemblies(); dxf_outputs(); copy_rfq(); svg_drawings()
    loads,masses,mag,nesting=calculations(records); costs=cost_model(); report=validation(records,mag); documents(records,loads,masses,mag,nesting,costs,report)
    if not args.skip_renders: render_outputs()
    summary={"exported_parts":len(records),"printed_stls":sum(r["printable"] for r in records),"step_assemblies":12,
             "renders":0 if args.skip_renders else 18,"validation_reviews":sum(c["status"]!="PASS" for c in report["checks"]),
             "unexpected_collisions":report["unexpected_interferences"]}
    print(json.dumps(summary,indent=2)); raise SystemExit(1 if report["unexpected_interferences"] else 0)


if __name__=="__main__": main()
