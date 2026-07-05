#!/usr/bin/env python3
"""Build the Agent font family from vendored TASA Orbiter binaries."""
import pathlib

from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

from rename_map import COPYRIGHT_NOTICE, STATIC_WEIGHTS, SPLIT_VF_AXES

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


def build_combined_vf():
    webfonts_dir = DIST_DIR / "webfonts"
    variable_dir = DIST_DIR / "variable"
    webfonts_dir.mkdir(parents=True, exist_ok=True)
    variable_dir.mkdir(parents=True, exist_ok=True)

    font = TTFont(VENDOR_DIR / "vf" / "TASAOrbiterVF.woff2")
    rename_strings(font)
    set_copyright(font)
    font.flavor = None
    ttf_path = variable_dir / "AgentVF.ttf"
    font.save(ttf_path)

    webfont = TTFont(ttf_path)
    webfont.flavor = "woff2"
    webfont.save(webfonts_dir / "AgentVF.woff2")
    return ttf_path


def prune_stat(font):
    stat = font["STAT"].table
    fvar_tags = [a.axisTag for a in font["fvar"].axes]
    old_axes = stat.DesignAxisRecord.Axis
    keep_indices = [i for i, ax in enumerate(old_axes) if ax.AxisTag in fvar_tags]
    index_remap = {old_i: new_i for new_i, old_i in enumerate(keep_indices)}
    stat.DesignAxisRecord.Axis = [old_axes[i] for i in keep_indices]
    if stat.AxisValueArray is not None:
        new_values = []
        for av in stat.AxisValueArray.AxisValue:
            if av.Format in (1, 2, 3):
                if av.AxisIndex not in index_remap:
                    continue
                av.AxisIndex = index_remap[av.AxisIndex]
                new_values.append(av)
            elif av.Format == 4:
                if all(rec.AxisIndex in index_remap for rec in av.AxisValueRecord):
                    for rec in av.AxisValueRecord:
                        rec.AxisIndex = index_remap[rec.AxisIndex]
                    new_values.append(av)
        stat.AxisValueArray.AxisValue = new_values


def build_split_vf(combined_ttf_path, optical):
    axes = SPLIT_VF_AXES[optical]
    webfonts_dir = DIST_DIR / "webfonts"
    variable_dir = DIST_DIR / "variable"
    webfonts_dir.mkdir(parents=True, exist_ok=True)
    variable_dir.mkdir(parents=True, exist_ok=True)

    font = TTFont(combined_ttf_path)
    instantiateVariableFont(
        font,
        {"opsz": axes["opsz_pin"], "wght": axes["wght_range"]},
        inplace=True,
        updateFontNames=False,
    )
    prune_stat(font)

    name = font["name"]
    fvar = font["fvar"]
    for inst in fvar.instances:
        old = name.getDebugName(inst.subfamilyNameID)
        style = old.replace(f"{optical} ", "").replace(optical, "").strip() or "Regular"
        set_name_all_platforms(name, inst.subfamilyNameID, style)
        if inst.postscriptNameID and inst.postscriptNameID != 0xFFFF:
            set_name_all_platforms(name, inst.postscriptNameID, f"Agent{optical}VF-{style}")

    family = f"Agent {optical} VF"
    set_name_all_platforms(name, 1, family)
    set_name_all_platforms(name, 2, "Regular")
    set_name_all_platforms(name, 4, f"{family} Regular")
    set_name_all_platforms(name, 6, f"Agent{optical}VF-Regular")
    set_name_all_platforms(name, 16, family)
    set_name_all_platforms(name, 17, "Regular")
    set_name_all_platforms(name, 3, f"1.001;Local Remote;Agent{optical}VF-Regular")
    set_name_all_platforms(name, 25, f"Agent{optical}VF")

    ttf_path = variable_dir / f"Agent{optical}VF.ttf"
    font.save(ttf_path)

    webfont = TTFont(ttf_path)
    webfont.flavor = "woff2"
    webfont.save(webfonts_dir / f"Agent{optical}VF.woff2")
    return ttf_path
