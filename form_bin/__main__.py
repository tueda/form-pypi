import os
import sys

from . import form_command


def main() -> None:
    os.execv(form_command[0], form_command + sys.argv[1:])  # noqa: S606
    sys.exit(11)


if __name__ == "__main__":
    main()
