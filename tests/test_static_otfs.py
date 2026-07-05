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
    return d


def all_name_strings(font):
    # nameID 0 (copyright) is deliberately excluded: set_copyright()'s
    # composed notice legitimately says "based on TASA Orbiter" as
    # attribution — that's required content, not leftover branding.
    strings = [rec.toUnicode() for rec in font["name"].names if rec.nameID != 0]
    cff = font["CFF "].cff
    strings.extend(cff.fontNames)
    if hasattr(cff.topDictIndex[0], "FullName"):
        strings.append(cff.topDictIndex[0].FullName)
    return strings


def test_build_static_otfs_produces_13_files(dist_dir):
    built = build_agent.build_static_otfs()
    assert len(built) == 13
    assert len(list((dist_dir / "otf").glob("*.otf"))) == 13


def test_static_otfs_have_no_upstream_branding(dist_dir):
    build_agent.build_static_otfs()
    for path in sorted((dist_dir / "otf").glob("*.otf")):
        font = TTFont(path)
        for s in all_name_strings(font):
            assert "TASA" not in s and "Orbiter" not in s, f"{path.name}: {s!r}"


def test_static_otf_family_and_copyright(dist_dir):
    build_agent.build_static_otfs()
    font = TTFont(dist_dir / "otf" / "AgentDisplay-Black.otf")
    name = font["name"]
    # Use nameID 16/17 (typographic family/subfamily), not 1/2: upstream's
    # own convention bakes non-RIBBI weights like "Black" into the legacy
    # family name (nameID 1 = "TASA Orbiter Display Black", nameID 2 =
    # "Regular") so old apps don't misgroup it. nameID 16/17 are the ones
    # that stay consistently split across every weight.
    assert name.getDebugName(16) == "Agent Display"
    assert name.getDebugName(17) == "Black"
    assert name.getDebugName(6) == "AgentDisplay-Black"
    assert "Emil Uzelac" in name.getDebugName(0)
    assert "Local Remote" in name.getDebugName(0)
