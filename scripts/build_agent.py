#!/usr/bin/env python3
"""Build the Agent font family from vendored TASA Orbiter binaries."""
import pathlib

from fontTools.ttLib import TTFont

from rename_map import COPYRIGHT_NOTICE, STATIC_WEIGHTS

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
VENDOR_DIR = REPO_ROOT / "vendor" / "TASA-Orbiter-v1.001"
DIST_DIR = REPO_ROOT / "dist" / "Agent"


def rename_strings(font, skip_name0=True):
    name = font["name"]
    for rec in name.names:
        if skip_name0 and rec.nameID == 0:
            continue
        text = rec.toUnicode()
        new_text = text.replace("TASA Orbiter", "Agent").replace("TASAOrbiter", "Agent")
        if new_text != text:
            rec.string = new_text
    if "CFF " in font:
        cff = font["CFF "].cff
        cff.fontNames = [
            n.replace("TASA Orbiter", "Agent").replace("TASAOrbiter", "Agent")
            for n in cff.fontNames
        ]
        td = cff.topDictIndex[0]
        if hasattr(td, "FullName"):
            td.FullName = (
                td.FullName.replace("TASA Orbiter", "Agent").replace("TASAOrbiter", "Agent")
            )
        if hasattr(td, "FamilyName"):
            td.FamilyName = (
                td.FamilyName.replace("TASA Orbiter", "Agent").replace("TASAOrbiter", "Agent")
            )


def set_name_all_platforms(name_table, name_id, value):
    name_table.setName(value, name_id, 3, 1, 0x409)
    name_table.setName(value, name_id, 1, 0, 0)


def set_copyright(font, notice=COPYRIGHT_NOTICE):
    set_name_all_platforms(font["name"], 0, notice)


def build_static_otfs():
    out_dir = DIST_DIR / "otf"
    out_dir.mkdir(parents=True, exist_ok=True)
    built = []
    for optical, weights in STATIC_WEIGHTS.items():
        for weight in weights:
            src = VENDOR_DIR / "otf" / f"TASAOrbiter{optical}-{weight}.otf"
            font = TTFont(src)
            rename_strings(font)
            set_copyright(font)
            out_path = out_dir / f"Agent{optical}-{weight}.otf"
            font.save(out_path)
            built.append(out_path)
    return built
