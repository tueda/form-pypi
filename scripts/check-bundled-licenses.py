#!/usr/bin/env python3
"""Check bundled license files in distributions under dist/."""

from __future__ import annotations

import tarfile
import zipfile
from pathlib import Path
from typing import NoReturn

DIST_DIR = Path("dist")
MANIFEST_FILE = "LICENSES_bundled.txt"
BUNDLED_LICENSE_FILES = frozenset(
    {
        MANIFEST_FILE,
        "form/COPYING",
        "gmp/COPYINGv3",
        "gmp/COPYING.LESSERv3",
        "mpfr/COPYING",
        "mpfr/COPYING.LESSER",
        "flint/COPYING",
        "flint/COPYING.LESSER",
        "zlib/LICENSE",
        "zstd/LICENSE",
    }
)
SDIST_REQUIRED_FILES = (
    "hepware/Makefile",
    "hepware/LICENSES_bundled.txt",
)


def fail(message: str) -> NoReturn:
    """Exit with a distribution validation error."""
    raise SystemExit(message)


def parse_manifest(contents: str) -> list[str]:
    """Return license paths declared by LICENSES_bundled.txt."""
    paths = []
    for line in contents.splitlines():
        if line.startswith("License file: "):
            paths.append(line.removeprefix("License file: "))
        elif line.startswith("License files: "):
            paths.extend(line.removeprefix("License files: ").split(", "))
    return paths


def check_wheel(wheel: Path) -> None:
    """Check bundled licenses in one wheel."""
    with zipfile.ZipFile(wheel) as archive:
        names = archive.namelist()
        metadata = [name for name in names if name.endswith(".dist-info/METADATA")]
        if len(metadata) != 1:
            fail(f"{wheel}: expected one METADATA file, found {len(metadata)}")

        prefix = metadata[0].removesuffix("METADATA") + "licenses/"
        actual = {
            name.removeprefix(prefix)
            for name in names
            if name.startswith(prefix) and not name.endswith("/")
        }
        if actual != BUNDLED_LICENSE_FILES:
            missing = sorted(BUNDLED_LICENSE_FILES - actual)
            unexpected = sorted(actual - BUNDLED_LICENSE_FILES)
            fail(
                f"{wheel}: bundled licenses differ; "
                f"missing={missing}, unexpected={unexpected}"
            )

        manifest = archive.read(f"{prefix}{MANIFEST_FILE}").decode()
        declared_paths = parse_manifest(manifest)
        if len(declared_paths) != len(set(declared_paths)):
            fail(f"{wheel}: {MANIFEST_FILE} contains duplicate license paths")

        expected_paths = BUNDLED_LICENSE_FILES - {MANIFEST_FILE}
        actual_paths = set(declared_paths)
        if actual_paths != expected_paths:
            missing = sorted(expected_paths - actual_paths)
            unexpected = sorted(actual_paths - expected_paths)
            fail(
                f"{wheel}: {MANIFEST_FILE} differs from bundled licenses; "
                f"missing={missing}, unexpected={unexpected}"
            )


def check_sdist(sdist: Path) -> None:
    """Check license-related files in one source distribution."""
    with tarfile.open(sdist) as archive:
        names = archive.getnames()

    for required in SDIST_REQUIRED_FILES:
        if not any(name.endswith(f"/{required}") for name in names):
            fail(f"{sdist}: {required} not found")

    if any("/hepware/build/licenses/" in name for name in names):
        fail(f"{sdist}: generated license files must not be included")


def main() -> None:
    """Check all wheel and source distributions under dist/."""
    wheels = sorted(DIST_DIR.glob("*.whl"))
    if not wheels:
        fail("no wheels found")
    for wheel in wheels:
        check_wheel(wheel)
        print(f"{wheel}: OK")  # noqa: T201

    sdists = sorted(DIST_DIR.glob("*.tar.gz"))
    if not sdists:
        fail("no source distributions found")
    for sdist in sdists:
        check_sdist(sdist)
        print(f"{sdist}: OK")  # noqa: T201


if __name__ == "__main__":
    main()
