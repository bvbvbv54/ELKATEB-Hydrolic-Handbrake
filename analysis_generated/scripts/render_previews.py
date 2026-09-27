#!/usr/bin/env python3
"""Create non-destructive CAD and source-image previews under analysis_generated."""

from __future__ import annotations

import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "analysis_generated"
PKGS = OUT / "python_packages"
sys.path.insert(0, str(PKGS))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from PIL import Image, ImageDraw, ImageFont


def load_shape(path: Path):
    ext = path.suffix.lower()
    if ext in {".step", ".stp"}:
        from OCP.STEPControl import STEPControl_Reader
        reader = STEPControl_Reader()
    elif ext in {".igs", ".iges"}:
        from OCP.IGESControl import IGESControl_Reader
        reader = IGESControl_Reader()
    else:
        raise ValueError(ext)
    reader.ReadFile(str(path))
    reader.TransferRoots()
    return reader.OneShape()


def bbox(shape):
    from OCP.Bnd import Bnd_Box
    from OCP.BRepBndLib import BRepBndLib
    box = Bnd_Box()
    BRepBndLib.Add_s(shape, box, True)
    return np.array(box.Get(), dtype=float)


def tessellate(shape, deflection: float):
    from OCP.BRep import BRep_Tool
    from OCP.BRepMesh import BRepMesh_IncrementalMesh
    from OCP.TopAbs import TopAbs_FACE, TopAbs_REVERSED
    from OCP.TopExp import TopExp_Explorer
    from OCP.TopLoc import TopLoc_Location
    from OCP.TopoDS import TopoDS

    mesher = BRepMesh_IncrementalMesh(shape, deflection, False, 0.45, True)
    mesher.Perform()
    vertices = []
    faces = []
    exp = TopExp_Explorer(shape, TopAbs_FACE)
    while exp.More():
        face = TopoDS.Face_s(exp.Current())
        loc = TopLoc_Location()
        tri = BRep_Tool.Triangulation_s(face, loc)
        if tri is not None and tri.NbNodes() > 0:
            offset = len(vertices)
            tr = loc.Transformation()
            for i in range(1, tri.NbNodes() + 1):
                p = tri.Node(i).Transformed(tr)
                vertices.append((p.X(), p.Y(), p.Z()))
            reverse = face.Orientation() == TopAbs_REVERSED
            for i in range(1, tri.NbTriangles() + 1):
                a, b, c = tri.Triangle(i).Get()
                idx = [offset + a - 1, offset + b - 1, offset + c - 1]
                if reverse:
                    idx[1], idx[2] = idx[2], idx[1]
                faces.append(idx)
        exp.Next()
    return np.asarray(vertices, dtype=float), np.asarray(faces, dtype=np.int64)


def equal_axes(ax, v):
    lo, hi = v.min(axis=0), v.max(axis=0)
    center = (lo + hi) / 2
    radius = max(hi - lo) / 2
    if radius <= 0:
        radius = 1
    ax.set_xlim(center[0] - radius, center[0] + radius)
    ax.set_ylim(center[1] - radius, center[1] + radius)
    ax.set_zlim(center[2] - radius, center[2] + radius)


def render_neutral(path: Path, out: Path):
    shape = load_shape(path)
    bb = bbox(shape)
    span = max(bb[3:] - bb[:3])
    verts, faces = tessellate(shape, max(span / 300.0, 0.15))
    if len(faces) > 180000:
        step = math.ceil(len(faces) / 180000)
        faces = faces[::step]
    views = [(25, -55, "isometric"), (0, -90, "side"), (90, -90, "top")]
    fig = plt.figure(figsize=(15, 5), dpi=180)
    tris = verts[faces]
    for i, (elev, azim, title) in enumerate(views, 1):
        ax = fig.add_subplot(1, 3, i, projection="3d")
        poly = Poly3DCollection(tris, linewidths=0.06, edgecolors=(0.1, 0.12, 0.14, 0.25))
        poly.set_facecolor((0.38, 0.63, 0.78, 0.95))
        ax.add_collection3d(poly)
        equal_axes(ax, verts)
        ax.view_init(elev=elev, azim=azim)
        ax.set_title(title)
        ax.set_axis_off()
    ext = bb[3:] - bb[:3]
    fig.suptitle(f"{path.name}\nOpenCascade preview; bounding extents {ext[0]:.2f} x {ext[1]:.2f} x {ext[2]:.2f} mm")
    fig.tight_layout()
    fig.savefig(out, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def contact_sheet(project: Path, out: Path):
    paths = sorted(p for p in project.rglob("*") if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".bmp", ".webp"})
    if not paths:
        return
    thumb_w, thumb_h, label_h = 420, 280, 55
    cols = 3
    rows = math.ceil(len(paths) / cols)
    canvas = Image.new("RGB", (cols * thumb_w, rows * (thumb_h + label_h)), "white")
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.load_default(size=18)
    for idx, path in enumerate(paths):
        try:
            im = Image.open(path).convert("RGB")
            im.thumbnail((thumb_w - 16, thumb_h - 16), Image.Resampling.LANCZOS)
            x = (idx % cols) * thumb_w
            y = (idx // cols) * (thumb_h + label_h)
            canvas.paste(im, (x + (thumb_w - im.width) // 2, y + (thumb_h - im.height) // 2))
            label = path.relative_to(project).as_posix()
            draw.text((x + 8, y + thumb_h + 4), label[:58], fill="black", font=font)
        except Exception as exc:
            draw.text((x + 8, y + 8), f"{path.name}: {exc}", fill="red", font=font)
    canvas.save(out, quality=92)


def main():
    preview_dir = OUT / "previews"
    preview_dir.mkdir(parents=True, exist_ok=True)
    for project in sorted(p for p in ROOT.iterdir() if p.is_dir() and ".snapshot." in p.name):
        contact_sheet(project, preview_dir / f"{project.name}_source_images.jpg")
        for path in sorted(project.rglob("*")):
            if path.suffix.lower() in {".step", ".stp"}:
                safe = f"{project.name}__{path.stem}".replace(" ", "_") + ".png"
                render_neutral(path, preview_dir / safe)


if __name__ == "__main__":
    main()
