"""Discover and identify user-installed slicer executables."""

from __future__ import annotations

import os
import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import ClassVar

from openprintbench.models import SlicerProbe

VERSION_PATTERNS = (
    re.compile(r"BambuStudio[- ](?P<version>\d+(?:\.\d+){2,3})", re.IGNORECASE),
    re.compile(r"OrcaSlicer[- ](?P<version>\d+(?:\.\d+){1,3})", re.IGNORECASE),
    re.compile(r"\bversion[ :]+(?P<version>\d+(?:\.\d+){1,3})", re.IGNORECASE),
)


@dataclass(frozen=True, slots=True)
class SlicerDefinition:
    """Static discovery information for a slicer."""

    key: str
    display_name: str
    env_var: str
    command_names: tuple[str, ...]
    known_paths: tuple[Path, ...]


BAMBU = SlicerDefinition(
    key="bambu",
    display_name="Bambu Studio",
    env_var="OPENPRINTBENCH_BAMBU",
    command_names=("bambu-studio", "BambuStudio"),
    known_paths=(
        Path("/Applications/BambuStudio.app/Contents/MacOS/BambuStudio"),
        Path("/usr/bin/bambu-studio"),
        Path("/usr/local/bin/bambu-studio"),
    ),
)

ORCA = SlicerDefinition(
    key="orca",
    display_name="OrcaSlicer",
    env_var="OPENPRINTBENCH_ORCA",
    command_names=("orca-slicer", "OrcaSlicer"),
    known_paths=(
        Path("/Applications/OrcaSlicer.app/Contents/MacOS/OrcaSlicer"),
        Path("/usr/bin/orca-slicer"),
        Path("/usr/local/bin/orca-slicer"),
    ),
)

DEFINITIONS: dict[str, SlicerDefinition] = {item.key: item for item in (BAMBU, ORCA)}


class SlicerDiscovery:
    """Discover slicers with explicit, environment, known-path, then PATH priority."""

    probe_timeout_seconds: ClassVar[float] = 12.0

    def __init__(self, definition: SlicerDefinition) -> None:
        self.definition = definition

    def locate(self, explicit: Path | None = None) -> tuple[Path | None, str | None]:
        """Return an executable and the non-secret source used to find it."""

        if explicit is not None:
            candidate = explicit.expanduser().resolve()
            return (candidate, "explicit") if self._is_executable(candidate) else (None, None)

        env_value = os.environ.get(self.definition.env_var)
        if env_value:
            candidate = Path(env_value).expanduser().resolve()
            if self._is_executable(candidate):
                return candidate, f"environment:{self.definition.env_var}"

        for candidate in self.definition.known_paths:
            if self._is_executable(candidate):
                return candidate, "known-path"

        for command in self.definition.command_names:
            located = shutil.which(command)
            if located:
                return Path(located).resolve(), "PATH"

        return None, None

    def probe(self, explicit: Path | None = None) -> SlicerProbe:
        """Run a bounded local help probe and parse a version."""

        executable, source = self.locate(explicit)
        if executable is None:
            return SlicerProbe(
                slicer=self.definition.key,
                display_name=self.definition.display_name,
                available=False,
                executable=None,
                version=None,
                source=None,
                error="executable not found",
            )

        try:
            with TemporaryDirectory(prefix="openprintbench-probe-") as probe_directory:
                completed = subprocess.run(
                    [str(executable), "--help"],
                    check=False,
                    capture_output=True,
                    text=True,
                    timeout=self.probe_timeout_seconds,
                    shell=False,
                    cwd=probe_directory,
                )
        except (OSError, subprocess.TimeoutExpired) as error:
            return SlicerProbe(
                slicer=self.definition.key,
                display_name=self.definition.display_name,
                available=False,
                executable=str(executable),
                version=None,
                source=source,
                error=type(error).__name__,
            )

        output = f"{completed.stdout}\n{completed.stderr}"
        version = parse_version(output)
        if completed.returncode != 0:
            return SlicerProbe(
                slicer=self.definition.key,
                display_name=self.definition.display_name,
                available=False,
                executable=str(executable),
                version=version,
                source=source,
                error=f"help exited {completed.returncode}",
            )

        return SlicerProbe(
            slicer=self.definition.key,
            display_name=self.definition.display_name,
            available=True,
            executable=str(executable),
            version=version,
            source=source,
        )

    @staticmethod
    def _is_executable(path: Path) -> bool:
        return path.is_file() and os.access(path, os.X_OK)


def parse_version(output: str) -> str | None:
    """Extract the first recognized slicer version from help text."""

    for pattern in VERSION_PATTERNS:
        match = pattern.search(output)
        if match:
            return match.group("version")
    return None


def probe_slicer(name: str, explicit: Path | None = None) -> SlicerProbe:
    """Probe a named supported slicer."""

    try:
        definition = DEFINITIONS[name]
    except KeyError as error:
        raise ValueError(f"unsupported slicer: {name}") from error
    return SlicerDiscovery(definition).probe(explicit)
