#!/usr/bin/env python3
"""Build the Agent font family from vendored TASA Orbiter binaries."""
import pathlib

from rename_map import COPYRIGHT_NOTICE

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
