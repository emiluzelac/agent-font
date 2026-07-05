# tests/test_rename_helpers.py
import pathlib
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import pytest
from fontTools.ttLib import TTFont

import build_agent

VENDOR_OTF = REPO_ROOT / "vendor" / "TASA-Orbiter-v1.001" / "otf" / "TASAOrbiterText-Regular.otf"

pytestmark = pytest.mark.skipif(
    not VENDOR_OTF.exists(), reason="vendor/ not populated; run scripts/fetch_vendor.py first"
)


def test_rename_strings_replaces_brand_in_name_table():
    font = TTFont(VENDOR_OTF)
    build_agent.rename_strings(font)
    name = font["name"]
    assert name.getDebugName(1) == "Agent Text"
    assert name.getDebugName(6) == "AgentText-Regular"
    assert "TASA" not in name.getDebugName(0)  # nameID 0 untouched by rename_strings (skip_name0=True)


def test_rename_strings_replaces_cff_names():
    font = TTFont(VENDOR_OTF)
    build_agent.rename_strings(font)
    cff = font["CFF "].cff
    assert cff.fontNames == ["AgentText-Regular"]
    assert cff.topDictIndex[0].FullName == "Agent Text Regular"


def test_set_copyright_overrides_name_id_0():
    font = TTFont(VENDOR_OTF)
    build_agent.set_copyright(font)
    copyright_ = font["name"].getDebugName(0)
    assert "Local Remote" in copyright_
    assert "Emil Uzelac" in copyright_
    assert "Agent" in copyright_
