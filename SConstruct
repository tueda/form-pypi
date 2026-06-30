import os

import enscons
import packaging.tags
import toml
from SCons.Script import Environment, File, FindSourceFiles


def get_universal_platform_tag() -> str:
    """Return the wheel tag for universal Python 3, but specific platform."""
    tag = next(packaging.tags.sys_tags())
    return f"py3-none-{tag.platform}"


pyproject = toml.load("pyproject.toml")

env = Environment(
    tools=["default", "packaging", enscons.generate],
    PACKAGE_METADATA=pyproject["project"],
    WHEEL_TAG=get_universal_platform_tag(),
    ENV=os.environ,
)

hepware_form = env.Command(
    ["hepware/form.done", "hepware/bin/tform"],
    ["hepware/Makefile"],
    "make -C hepware -j6 form.done",
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

# FindSourceFiles() will list every source file of every target
# defined so far.
File("PKG-INFO")
sdist = env.SDist(source=FindSourceFiles())

env.Alias("dist", sdist + bdist)
env.Alias("bdist", bdist)
env.Alias("sdist", sdist)
