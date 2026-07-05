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


def test_build_combined_vf_returns_ttf_path(dist_dir):
    ttf_path = build_agent.build_combined_vf()
    assert ttf_path == dist_dir / "variable" / "AgentVF.ttf"
    assert ttf_path.exists()
    assert (dist_dir / "webfonts" / "AgentVF.woff2").exists()


def test_combined_vf_axes_instances_and_family(dist_dir):
    ttf_path = build_agent.build_combined_vf()
    font = TTFont(ttf_path)
    axes = {a.axisTag: (a.minValue, a.maxValue) for a in font["fvar"].axes}
    assert axes == {"wght": (400.0, 900.0), "opsz": (8.0, 60.0)}
    assert len(font["fvar"].instances) == 13
    assert font["name"].getDebugName(16) == "Agent VF"
    assert "Emil Uzelac" in font["name"].getDebugName(0)


def test_combined_webfont_is_valid_woff2(dist_dir):
    build_agent.build_combined_vf()
    font = TTFont(dist_dir / "webfonts" / "AgentVF.woff2")
    assert font.flavor == "woff2"
    assert font["name"].getDebugName(16) == "Agent VF"
