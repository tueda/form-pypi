import os

import enscons
import packaging.tags
import toml
from SCons.Script import Environment, File, FindSourceFiles
from setuptools_scm import get_version


def get_universal_platform_tag() -> str:
    """Return the wheel tag for universal Python 3, but specific platform."""
    tag = next(packaging.tags.sys_tags())
    return f"py3-none-{tag.platform}"


def get_make_job_count() -> int:
    """Return the number of parallel jobs to use when running make."""
    process_cpu_count = getattr(os, "process_cpu_count", None)  # Python 3.13+
    count = None
    if process_cpu_count:
        count = process_cpu_count()
    return count or os.cpu_count() or 1


pyproject = toml.load("pyproject.toml")
metadata = pyproject["project"]
metadata["version"] = get_version(root=".", fallback_root=".")
metadata.pop("dynamic")

env = Environment(
    tools=["default", "packaging", enscons.generate],
    PACKAGE_METADATA=metadata,
    WHEEL_TAG=get_universal_platform_tag(),
    ENV=os.environ,
)

hepware_form = env.Command(
    ["hepware/form.done", "hepware/bin/tform"],
    ["hepware/Makefile"],
    f"make -C hepware -j{get_make_job_count()} form.done",
)

files = [
    File("form-packages/README.md"),
    File("form_bin/__init__.py"),
    File("form_bin/__main__.py"),
    env.Command(
        "form_bin/tform",
        [hepware_form],
        ["cp hepware/bin/tform form_bin/tform", "strip form_bin/tform"],
    ),
]

platformlib = env.Whl("platlib", files, root="")
bdist = env.WhlFile(source=platformlib)

File("PKG-INFO")
# Work around an enscons 0.30.0 issue where the sdist target_prefix
# uses the unnormalised package name.
# FindSourceFiles() will list every source file of every target
# defined so far.
sdist_env = env.Clone()
sdist_env["PACKAGE_NAME"] = sdist_env["PACKAGE_NAME_SAFE"]
sdist = sdist_env.SDist(source=FindSourceFiles())

env.Alias("dist", sdist + bdist)
env.Alias("bdist", bdist)
env.Alias("sdist", sdist)
