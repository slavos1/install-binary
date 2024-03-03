from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser, BooleanOptionalAction, Namespace
from pathlib import Path

from loguru import logger

from . import __version__ as VERSION
from .install import LATEST_RELEASE, install
from .log import setup_logging

HELP_FORMATTER = ArgumentDefaultsHelpFormatter


def parse_args() -> Namespace:
    parser = ArgumentParser("install-binary", formatter_class=HELP_FORMATTER)
    parser.add_argument("--version", action="version", version=VERSION)
    parser.add_argument("-q", "--quiet", action="store_true", help="Log less")
    parser.add_argument("-d", "--debug", action="store_true", help="Log more")
    parser.add_argument(
        "-l",
        "--log-root",
        help="Log root path (specify '' to suppress logging to a file)",
        type=lambda s: Path(s) if s else None,
        metavar="PATH",
        default="logs",
    )
    parser.add_argument(
        "-b",
        "--binary",
        help="Destination binary (e.g. starship); must match binary in the downloaded artifact",
        required=True,
    )
    parser.add_argument(
        "-p",
        "--dest-path",
        help="Destination path",
        type=Path,
        default="~/.local/bin",
    )
    parser.add_argument(
        "-g",
        "--source-repo",
        help="Source GitHub repo (e.g. https://github.com/starship/starship)",
        metavar="URL",
        required=True,
    )
    parser.add_argument(
        "-a",
        "--artifact",
        help=r"Released binary artifact, Python format string recognizing {tag} that would be replaced by resolved release version (e.g. starship-x86_64-unknown-linux-musl.tar.gz or 'restic_{tag}_linux_amd64.bz2')",
        metavar="FMT_STRING",
        required=True,
    )
    parser.add_argument(
        "-r",
        "--release",
        help="Release to install",
        metavar="STR",
        default=LATEST_RELEASE,
    )
    parser.add_argument(
        "-c",
        "--compress",
        help="Compress during artifact download",
        action=BooleanOptionalAction,
        default=True,
    )

    return parser.parse_args()


def cli() -> None:
    args = parse_args()
    setup_logging(args)
    logger.debug("args={}", args)
    install(args)
