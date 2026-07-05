#!/usr/bin/env python3
"""Fetch and vendor TASA Orbiter v1.001 from the pinned upstream GitHub release."""
import hashlib
import pathlib
import tempfile
import urllib.request
import zipfile

RELEASE_URL = (
    "https://github.com/localremotetw/TASA-Typeface-Collection"
    "/releases/download/v1.001/TASA-Typeface-Collection-v1.001.zip"
)
EXPECTED_SHA256 = "742ea57402cb56e4030f82550f0690f063cffd291fee6c6d921a17e1fcc5728b"

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
VENDOR_DIR = REPO_ROOT / "vendor" / "TASA-Orbiter-v1.001"


def fetch_vendor():
    with tempfile.TemporaryDirectory() as tmp:
        zip_path = pathlib.Path(tmp) / "tasa.zip"
        urllib.request.urlretrieve(RELEASE_URL, zip_path)

        digest = hashlib.sha256(zip_path.read_bytes()).hexdigest()
        if digest != EXPECTED_SHA256:
            raise SystemExit(
                f"Checksum mismatch: expected {EXPECTED_SHA256}, got {digest}. "
                "Upstream release contents changed since this was pinned — "
                "do not proceed without re-reviewing the license/contents."
            )

        otf_dir = VENDOR_DIR / "otf"
        vf_dir = VENDOR_DIR / "vf"
        otf_dir.mkdir(parents=True, exist_ok=True)
        vf_dir.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(zip_path) as zf:
            for info in zf.infolist():
                name = info.filename
                if "__MACOSX" in name or name.endswith("/"):
                    continue
                if "/TASA Orbiter/" not in name:
                    continue
                base = name.rsplit("/", 1)[-1]
                if base == "OFL.txt":
                    (VENDOR_DIR / "OFL.txt").write_bytes(zf.read(info))
                elif base.endswith(".otf"):
                    (otf_dir / base).write_bytes(zf.read(info))
                elif base.endswith(".woff2"):
                    (vf_dir / base).write_bytes(zf.read(info))


if __name__ == "__main__":
    fetch_vendor()
    print(f"Vendored TASA Orbiter v1.001 into {VENDOR_DIR}")
