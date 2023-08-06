#!/usr/bin/env python3
"""UNC to URL Converter."""

from __future__ import print_function
import sys
import argparse
import unicodedata

# from urllib.parse import unquote

sys.path.insert(0, "./lib")  # for Alfred Workflow
import argcomplete  # type: ignore # noqa: E402 # pylint: disable=C0413

# from . import __version__
__version__ = "0.1.0"  # for Alfred Workflow


def main(args=None):
    """Start point."""
    if args is None:
        main(get_parser().parse_args())
    else:
        if args.reverse:
            print(url_to_unc(args.unc))
        else:
            print(unc_to_url(args.unc, args.file))


def unc_to_url(unc: str, as_file: bool = False):
    """Convert UNC to file or smb URL."""
    # normalize for the Alfred Workflow
    unc = unicodedata.normalize("NFC", unc).strip()  # pylint: disable=I1101
    url = unc.replace("\\\\", "smb://").replace("\\", "/")
    if as_file:  # for Windows 10
        url = url.replace("smb://", "file://")
    url = url.replace(" ", "%20")  # don't encode Umlauts
    return url


def url_to_unc(url: str):
    """Convert URL und UNC."""
    url = url.strip()
    url = url.replace("smb://", "\\\\")
    url = url.replace("file://", "\\\\")
    url = url.replace("/", "\\")
    url = url.replace("%20", " ")
    return url


def get_parser():
    """Create urn line argument parser."""
    parser = argparse.ArgumentParser(description="Simple UNC to URL tool.")

    parser.add_argument("unc", help="An Uniform Naming Convention (UNC) link")

    parser.add_argument(
        "-r",
        "--reverse",
        dest="reverse",
        help="Reverse the conversation (url2unc)",
        action="store_true",
        default=False,
    )

    parser.add_argument(
        "-f",
        "--file",
        dest="file",
        help="File URL (file://)",
        action="store_true",
        default=False,
    )

    parser.add_argument(
        "--version",
        "-v",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__),
    )

    argcomplete.autocomplete(parser)

    return parser


if __name__ == "__main__":
    main()
