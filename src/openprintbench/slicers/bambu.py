"""Bambu Studio command construction based on its documented CLI."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

SUPPORTED_INPUT_SUFFIXES = {".3mf", ".stl"}


@dataclass(frozen=True, slots=True)
class BambuSliceRequest:
    """Inputs needed to plan one Bambu Studio slice."""

    executable: Path
    input_path: Path
    output_dir: Path
    output_name: str = "sliced.3mf"
    plate: int = 0
    debug_level: int = 2
    machine_settings: Path | None = None
    process_settings: Path | None = None
    filament_settings: tuple[Path, ...] = ()


def build_bambu_slice_command(request: BambuSliceRequest) -> tuple[str, ...]:
    """Build an argument array; never execute a shell command."""

    executable = request.executable.expanduser().resolve()
    input_path = request.input_path.expanduser().resolve()
    output_dir = request.output_dir.expanduser().resolve()

    _require_file(executable, "Bambu Studio executable")
    _require_file(input_path, "input")

    suffix = input_path.suffix.lower()
    if suffix not in SUPPORTED_INPUT_SUFFIXES:
        supported = ", ".join(sorted(SUPPORTED_INPUT_SUFFIXES))
        raise ValueError(f"unsupported input type {suffix!r}; expected one of: {supported}")
    if request.plate < 0:
        raise ValueError("plate must be zero or greater")
    if request.debug_level not in range(0, 6):
        raise ValueError("debug level must be between 0 and 5")
    if Path(request.output_name).name != request.output_name:
        raise ValueError("output name must be a filename, not a path")
    if not request.output_name.lower().endswith(".3mf"):
        raise ValueError("output name must end in .3mf")

    settings: list[Path] = []
    if request.machine_settings is not None:
        settings.append(_resolved_file(request.machine_settings, "machine settings"))
    if request.process_settings is not None:
        settings.append(_resolved_file(request.process_settings, "process settings"))

    filaments = tuple(
        _resolved_file(path, "filament settings") for path in request.filament_settings
    )

    if suffix == ".stl" and (
        request.machine_settings is None
        or request.process_settings is None
        or not request.filament_settings
    ):
        raise ValueError(
            "STL planning requires machine, process, and at least one filament settings file"
        )

    command = [
        str(executable),
        "--slice",
        str(request.plate),
        "--debug",
        str(request.debug_level),
        "--outputdir",
        str(output_dir),
    ]
    if suffix == ".stl":
        command.extend(("--orient", "1", "--arrange", "1"))
    if settings:
        command.extend(("--load-settings", ";".join(str(path) for path in settings)))
    if filaments:
        command.extend(("--load-filaments", ";".join(str(path) for path in filaments)))
    command.extend(("--export-3mf", request.output_name, str(input_path)))
    return tuple(command)


def _require_file(path: Path, label: str) -> None:
    if not path.is_file():
        raise ValueError(f"{label} is not a regular file: {path}")


def _resolved_file(path: Path, label: str) -> Path:
    resolved = path.expanduser().resolve()
    _require_file(resolved, label)
    return resolved
