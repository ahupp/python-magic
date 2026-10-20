"""Identify files with ``python -m magic``."""

from __future__ import print_function  # noqa: UP010 - Keep the advertised Python 2.7 syntax.

import argparse
import sys

from magic import MagicException, from_file


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="python -m magic", description="Identify file types using libmagic"
    )
    parser.add_argument(
        "--mime", action="store_true", help="print MIME types instead of descriptions"
    )
    parser.add_argument("files", nargs="+", help="files to identify")
    args = parser.parse_args(argv)

    status = 0
    for filename in args.files:
        try:
            result = from_file(filename, mime=args.mime)
        except (OSError, MagicException) as error:
            print("{}: {}".format(filename, error), file=sys.stderr)  # noqa: UP032
            status = 1
        else:
            print("{}: {}".format(filename, result))  # noqa: UP032
    return status


if __name__ == "__main__":
    sys.exit(main())
