__all__ = ("form", "form_command")

import os
import tempfile


def _form_cmd() -> list[str]:
    """Determine the path and the needed set of arguments to call
    the form binary. Make sure the include paths are set up so
    that form packages installed into the Python environment are
    found.
    """
    this_dir = os.path.abspath(os.path.dirname(__file__))
    packages = os.path.join(os.path.dirname(this_dir), "form-packages")
    if not packages.endswith(os.path.sep):
        packages += os.path.sep
    form_path = os.path.join(this_dir, "tform")
    tmp_dir = tempfile.gettempdir()
    form_tmp = os.environ.get("FORMTMP", tmp_dir)
    form_tmpsort = os.environ.get("FORMTMPSORT", tmp_dir)
    return [form_path, "-I", packages, "-t", form_tmp, "-ts", form_tmpsort]


def form(*args: str) -> None:
    """Run the form binary with the given arguments."""
    import subprocess

    subprocess.check_call(form_command + list(args))  # noqa: S603


# This is the path and the needed set of arguments to call the
# form binary.
form_command: list[str] = _form_cmd()
