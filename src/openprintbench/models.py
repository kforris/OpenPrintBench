"""Evidence models shared by probes and plans."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Literal


@dataclass(frozen=True, slots=True)
class SlicerProbe:
    """Result of discovering and identifying a local slicer."""

    slicer: str
    display_name: str
    available: bool
    executable: str | None
    version: str | None
    source: str | None
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable mapping."""

        return asdict(self)


@dataclass(frozen=True, slots=True)
class FileFingerprint:
    """Stable identity for a local input without embedding its contents."""

    name: str
    size_bytes: int
    sha256: str

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable mapping."""

        return asdict(self)


@dataclass(frozen=True, slots=True)
class SlicePlan:
    """A planned slicer invocation that has not been executed."""

    schema_version: str
    state: Literal["planned"]
    created_at: str
    slicer: SlicerProbe
    input: FileFingerprint
    plate: int
    output_name: str
    command: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable mapping."""

        result = asdict(self)
        result["command"] = list(self.command)
        return result


@dataclass(frozen=True, slots=True)
class FixtureProvenance:
    """Pinned redistribution information for a slice input."""

    source_url: str
    source_commit: str
    license: str

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable mapping."""

        return asdict(self)


@dataclass(frozen=True, slots=True)
class ProfileProvenance:
    """Pinned source and license for locally materialized slicer profiles."""

    source_url: str
    source_commit: str
    license: str

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable mapping."""

        return asdict(self)


@dataclass(frozen=True, slots=True)
class OutputFingerprint:
    """Stable identity for one file produced inside the isolated output tree."""

    relative_path: str
    size_bytes: int
    sha256: str

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable mapping."""

        return asdict(self)


@dataclass(frozen=True, slots=True)
class RunEvidence:
    """Truthful evidence from one explicitly approved slicer process."""

    manifest_path: str
    log_path: str
    exit_status: int | None
    timed_out: bool
    output_count: int

    @property
    def succeeded(self) -> bool:
        """Return whether the slicer exited successfully before the timeout."""

        return not self.timed_out and self.exit_status == 0
