#!/usr/bin/env python3
"""Extract archive metadata and scan source-package strings for provenance/license clues."""

from __future__ import annotations

import json
import re
import shutil
import zipfile
from pathlib import Path

import olefile

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "analysis_generated"
DEST = OUT / "extracted_metadata"
PROJECTS = sorted(p for p in ROOT.iterdir() if p.is_dir() and ".snapshot." in p.name)

KEYWORDS = re.compile(
    r"license|licence|copyright|creative commons|commercial|non-commercial|author|designer|"
    r"grabcad|thingiverse|printables|cults3d|myminifactory|github|https?://|solidworks|fusion 360|autodesk",
    re.I,
)


def strings(data: bytes):
    for m in re.finditer(rb"[\x20-\x7e]{5,}", data):
        yield m.group().decode("latin-1", errors="replace")
    for m in re.finditer(rb"(?:[\x20-\x7e]\x00){5,}", data):
        yield m.group().decode("utf-16le", errors="replace")


def main():
    DEST.mkdir(parents=True, exist_ok=True)
    hits = []
    for project in PROJECTS:
        for path in sorted(p for p in project.rglob("*") if p.is_file()):
            try:
                data = path.read_bytes()
            except OSError:
                continue
            seen = set()
            for s in strings(data):
                if KEYWORDS.search(s) and s not in seen:
                    seen.add(s)
                    hits.append({"path": path.relative_to(ROOT).as_posix(), "text": s[:1000]})

            if path.suffix.lower() == ".f3d" and zipfile.is_zipfile(path):
                target = DEST / (project.name + "__" + path.stem)
                target.mkdir(exist_ok=True)
                with zipfile.ZipFile(path) as zf:
                    wanted = [
                        n for n in zf.namelist()
                        if n.endswith(("Manifest.dat", "Properties.dat", "Previews/small.png", "MetaStream.dat"))
                    ]
                    for name in wanted:
                        clean = name.replace("/", "__")
                        (target / clean).write_bytes(zf.read(name))
            if path.suffix.lower() in {".sldprt", ".sldasm", ".slddrw"} and olefile.isOleFile(path):
                preview_dir = OUT / "previews" / "solidworks_embedded"
                preview_dir.mkdir(parents=True, exist_ok=True)
                try:
                    with olefile.OleFileIO(path) as ole:
                        if ole.exists("PreviewPNG"):
                            blob = ole.openstream("PreviewPNG").read()
                            pos = blob.find(b"\x89PNG\r\n\x1a\n")
                            if pos >= 0:
                                name = (project.name + "__" + path.stem + ".png").replace(" ", "_")
                                (preview_dir / name).write_bytes(blob[pos:])
                except Exception:
                    pass
    (OUT / "provenance_license_string_scan.json").write_text(
        json.dumps(hits, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"Recorded {len(hits)} keyword-bearing strings")


if __name__ == "__main__":
    main()
