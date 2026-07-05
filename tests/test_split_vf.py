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


@pytest.fixture()
def combined_ttf(dist_dir):
    return build_agent.build_combined_vf()


EXPECTED = {
    "Text": ((400.0, 700.0), 4, "Agent Text VF"),
    "Deck": ((400.0, 700.0), 4, "Agent Deck VF"),
    "Display": ((400.0, 900.0), 5, "Agent Display VF"),
}


@pytest.mark.parametrize("optical", ["Text", "Deck", "Display"])
def test_split_vf_axes_instances_family(dist_dir, combined_ttf, optical):
    wght_range, n_instances, family = EXPECTED[optical]
    ttf_path = build_agent.build_split_vf(combined_ttf, optical)
    font = TTFont(ttf_path)
    axes = font["fvar"].axes
    assert [a.axisTag for a in axes] == ["wght"]
    assert (axes[0].minValue, axes[0].maxValue) == wght_range
    assert len(font["fvar"].instances) == n_instances
    assert font["name"].getDebugName(16) == family
    assert font["name"].getDebugName(6) == f"Agent{optical}VF-Regular"


@pytest.mark.parametrize("optical", ["Text", "Deck", "Display"])
def test_split_vf_stat_pruned_to_wght_only(dist_dir, combined_ttf, optical):
    ttf_path = build_agent.build_split_vf(combined_ttf, optical)
    font = TTFont(ttf_path)
    stat_axes = [ax.AxisTag for ax in font["STAT"].table.DesignAxisRecord.Axis]
    assert stat_axes == ["wght"]


@pytest.mark.parametrize("optical", ["Text", "Deck", "Display"])
def test_split_vf_instance_names_drop_redundant_optical_prefix(dist_dir, combined_ttf, optical):
    ttf_path = build_agent.build_split_vf(combined_ttf, optical)
    font = TTFont(ttf_path)
    name = font["name"]
    for inst in font["fvar"].instances:
        style = name.getDebugName(inst.subfamilyNameID)
        assert optical not in style


def test_split_vf_webfont_is_valid_woff2(dist_dir, combined_ttf):
    build_agent.build_split_vf(combined_ttf, "Text")
    font = TTFont(dist_dir / "webfonts" / "AgentTextVF.woff2")
    assert font.flavor == "woff2"
