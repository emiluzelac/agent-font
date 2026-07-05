import pathlib
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import pytest
from fontTools.ttLib import TTFont

import build_agent

pytestmark = pytest.mark.skipif(
    not (build_agent.VENDOR_DIR / "vf").exists(),
    reason="vendor/ not populated; run scripts/fetch_vendor.py first",
)


@pytest.fixture()
def dist_dir(tmp_path, monkeypatch):
    d = tmp_path / "Agent"
    monkeypatch.setattr(build_agent, "DIST_DIR", d)
    return d


def test_combined_vf_instances_have_dedicated_name_ids(dist_dir):
    ttf_path = build_agent.build_combined_vf()
    font = TTFont(ttf_path)
    name = font["name"]
    for inst in font["fvar"].instances:
        assert inst.subfamilyNameID not in (2, 17), (
            f"instance {inst.coordinates} reuses the font's base subfamily "
            "name ID instead of a dedicated one"
        )
        assert inst.postscriptNameID not in (6,), (
            f"instance {inst.coordinates} reuses the font's base PS name ID "
            "instead of a dedicated one"
        )
        assert name.getDebugName(inst.subfamilyNameID)
        assert name.getDebugName(inst.postscriptNameID)


def test_split_vf_default_instance_has_dedicated_name_id(dist_dir):
    combined = build_agent.build_combined_vf()
    ttf_path = build_agent.build_split_vf(combined, "Text")
    font = TTFont(ttf_path)
    name = font["name"]
    default_inst = font["fvar"].instances[0]
    assert default_inst.subfamilyNameID not in (2, 17)
    assert default_inst.postscriptNameID not in (6,)
    assert name.getDebugName(default_inst.subfamilyNameID) == "Regular"


def test_deck_and_display_split_defaults_still_correct(dist_dir):
    combined = build_agent.build_combined_vf()
    for optical, expected_wght_max in (("Deck", 700), ("Display", 900)):
        ttf_path = build_agent.build_split_vf(combined, optical)
        font = TTFont(ttf_path)
        name = font["name"]
        default_inst = font["fvar"].instances[0]
        assert name.getDebugName(default_inst.subfamilyNameID) == "Regular"
