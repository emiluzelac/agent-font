import pathlib
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import pytest
from fontTools.ttLib import TTFont

import build_agent

pytestmark = pytest.mark.skipif(
    not (build_agent.VENDOR_DIR / "otf").exists(),
    reason="vendor/ not populated; run scripts/fetch_vendor.py first",
)


@pytest.fixture()
def dist_dir(tmp_path, monkeypatch):
    d = tmp_path / "Agent"
    monkeypatch.setattr(build_agent, "DIST_DIR", d)
    monkeypatch.setattr(build_agent, "REPO_ROOT", tmp_path)
    return d


def test_main_produces_complete_dist_tree(dist_dir):
    build_agent.main()

    otf_files = sorted(p.name for p in (dist_dir / "otf").glob("*.otf"))
    assert len(otf_files) == 13

    variable_files = sorted(p.name for p in (dist_dir / "variable").glob("*.ttf"))
    assert variable_files == [
        "AgentDeckVF.ttf", "AgentDisplayVF.ttf", "AgentTextVF.ttf", "AgentVF.ttf",
    ]

    webfont_files = sorted(p.name for p in (dist_dir / "webfonts").glob("*.woff2"))
    assert webfont_files == [
        "AgentDeckVF.woff2", "AgentDisplayVF.woff2", "AgentTextVF.woff2", "AgentVF.woff2",
    ]

    assert (dist_dir / "OFL.txt").exists()
    assert (build_agent.REPO_ROOT / "LICENSE").exists()

    # Spot-check one static and one split VF actually load and are correctly named.
    static = TTFont(dist_dir / "otf" / "AgentText-Regular.otf")
    assert static["name"].getDebugName(1) == "Agent Text"
    split = TTFont(dist_dir / "variable" / "AgentDisplayVF.ttf")
    assert split["name"].getDebugName(16) == "Agent Display VF"
