import bz2
import re
import tarfile
from argparse import Namespace
from hashlib import md5
from io import BytesIO
from pathlib import Path
from shutil import copyfileobj
from tempfile import NamedTemporaryFile
from typing import Any, BinaryIO, Callable, Optional, cast
from urllib.parse import urlsplit

import requests
from loguru import logger

LATEST_RELEASE = "latest"


def file_digest(stream: BinaryIO, digest_class: Callable[[bytes], Any] = md5) -> str:
    return cast(str, digest_class(stream.read()).hexdigest())


def extract_binary_from_tar(stream: BytesIO, desired_name: str) -> Optional[BytesIO]:
    with tarfile.open(fileobj=stream, mode="r:gz") as tar:
        for m in tar.getmembers():
            logger.debug("found member: {}", m)
            if m.name != desired_name:
                continue
            logger.debug("Extracting {}", m)
            # XXX tar.extractfile's type is BinaryIO but tmp_binary is of _TemporaryFileWrapper; mypy requires
            # _TemporaryFileWrapper to be _TemporaryFileWrapper[bytes] but the code fails during execution if I
            # cast(_TemporaryFileWrapper[bytes], tar.extractfile(m));
            # hence just ignoring mypy on the line
            return BytesIO(tar.extractfile(m).read())  # type: ignore

    return None


def extract_as_bz2(stream: BytesIO) -> Optional[BytesIO]:
    stream.seek(0)
    return BytesIO(bz2.BZ2File(stream).read())


def install(args: Namespace) -> None:
    logger.debug("args={}", args)
    parts = urlsplit(args.source_repo)
    if args.release == LATEST_RELEASE:
        # XXX yes, latest has a quirk in the path :|
        download_stub = f"{LATEST_RELEASE}/download"
        resolve_version_url = parts._replace(path="/".join((parts.path, "releases", download_stub))).geturl()
        response = requests.get(resolve_version_url)
        resolved_release = urlsplit(response.url).path.split("/")[-1]
        logger.debug("resolved_release={}", resolved_release)
    else:
        download_stub = f"download/{args.release}"
        resolved_release = args.release
    artifact = args.artifact.format(tag=re.sub("^v", "", resolved_release))
    download_link = parts._replace(path="/".join((parts.path, "releases", download_stub, artifact))).geturl()
    headers = {}
    if args.compress:
        headers.update({"Accept-Encoding": "gzip"})
    with NamedTemporaryFile("w+b") as tmp:
        logger.info("Downloading {}", download_link)
        logger.debug("Downloading {} (headers={})", download_link, headers)
        response = requests.get(download_link, headers=headers)
        response.raise_for_status()
        logger.debug("response={}, bytes={}", response, len(response.content))
        tmp.write(response.content)
        logger.debug("tmp.name: {}", tmp.name)
        tmp.seek(0)  # rewind to start
        # by default, I assume the file is the binary already
        tmp_binary: Optional[BytesIO] = BytesIO(tmp.read())
        try:
            tmp_binary = extract_binary_from_tar(cast(BytesIO, tmp_binary), args.binary)
        except tarfile.ReadError:
            tmp_binary = extract_as_bz2(cast(BytesIO, tmp_binary))
        except Exception as exc:
            logger.warning("Error unpacking {}, file is likely not a tarball ({})", tmp, repr(exc))

        if tmp_binary is None:
            raise RuntimeError(f"Error occurred during unpacking of {tmp}")

        tmp_binary.seek(0)
        new_digest = file_digest(cast(BinaryIO, tmp_binary))
        logger.debug("new new_digest={}", new_digest)
        dest_binary: Path = args.dest_path.expanduser().joinpath(args.binary)
        try:
            existing_digest = file_digest(dest_binary.open("rb"))
        except Exception as exc:
            logger.warning("Error reading {}: {}", dest_binary, exc)
            existing_digest = None
        logger.debug("old digest={}", existing_digest)
        if existing_digest and new_digest == existing_digest:
            logger.success("Existing {} is the latest version", dest_binary)
        else:
            logger.info("Copying newer binary to {}", dest_binary)
            tmp_binary.seek(0)
            copyfileobj(tmp_binary, dest_binary.open("wb"))
            dest_binary.chmod(0o750)
            logger.success("Installed {}", dest_binary)
