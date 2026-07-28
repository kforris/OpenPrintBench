"""Streaming fingerprints for regression inputs."""

from __future__ import annotations

import hashlib
from pathlib import Path

from openprintbench.models import FileFingerprint

CHUNK_SIZE = 1024 * 1024


def fingerprint_file(path: Path) -> FileFingerprint:
    """Hash a regular file without loading it all into memory."""

    resolved = path.expanduser().resolve()
    if not resolved.is_file():
        raise ValueError(f"input is not a regular file: {path}")

    digest = hashlib.sha256()
    with resolved.open("rb") as handle:
        for chunk in iter(lambda: handle.read(CHUNK_SIZE), b""):
            digest.update(chunk)

    return FileFingerprint(
        name=resolved.name,
        size_bytes=resolved.stat().st_size,
        sha256=digest.hexdigest(),
    )
