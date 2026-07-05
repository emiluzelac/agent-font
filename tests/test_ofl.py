import pathlib
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import pytest

import build_agent

pytestmark = pytest.mark.skipif(
    not (build_agent.VENDOR_DIR / "OFL.txt").exists(),
    reason="vendor/ not populated; run scripts/fetch_vendor.py first",
)


@pytest.fixture()
def dist_dir(tmp_path, monkeypatch):
    d = tmp_path / "Agent"
    monkeypatch.setattr(build_agent, "DIST_DIR", d)
    monkeypatch.setattr(build_agent, "REPO_ROOT", tmp_path)
    return d


def test_generate_ofl_retains_original_and_adds_new_copyright(dist_dir):
    ofl_path = build_agent.generate_ofl()
    text = ofl_path.read_text(encoding="utf-8")
    assert "Local Remote" in text
    assert "Emil Uzelac" in text
    assert "SIL OPEN FONT LICENSE Version 1.1" in text
    assert "DISCLAIMER" in text


def test_generate_ofl_does_not_declare_agent_as_reserved(dist_dir):
    ofl_path = build_agent.generate_ofl()
    text = ofl_path.read_text(encoding="utf-8")
    header = text.split("SIL OPEN FONT LICENSE")[0]
    assert "Reserved Font Name" not in header


def test_generate_ofl_writes_root_license(dist_dir):
    build_agent.generate_ofl()
    license_path = build_agent.REPO_ROOT / "LICENSE"
    assert license_path.exists()
    assert license_path.read_text(encoding="utf-8") == (dist_dir / "OFL.txt").read_text(encoding="utf-8")
