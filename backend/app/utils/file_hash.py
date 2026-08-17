"""File hashing utilities."""

import hashlib
from pathlib import Path


def calculate_file_hashes(file_path: str) -> tuple[str, str]:
    """Calculate SHA-256 and MD5 hashes for a file."""

    sha256 = hashlib.sha256()
    md5 = hashlib.md5()

    path = Path(file_path)

    with path.open("rb") as file:
        while chunk := file.read(1024 * 1024):
            sha256.update(chunk)
            md5.update(chunk)

    return sha256.hexdigest(), md5.hexdigest()
