"""Explicit, isolated slicer execution with privacy-reviewed evidence."""

from __future__ import annotations

import getpass
import json
import os
import re
import subprocess
from dataclasses import replace
from datetime import UTC, datetime
from pathlib import Path
from time import monotonic
from typing import Any

from openprintbench.fingerprint import fingerprint_file
from openprintbench.models import (
    FixtureProvenance,
    OutputFingerprint,
    ProfileProvenance,
    RunEvidence,
    SlicerProbe,
)
from openprintbench.profiles import (
    MATERIALIZER_VERSION,
    BambuProfileStore,
)
from openprintbench.slicers.bambu import BambuSliceRequest, build_bambu_slice_command

RUN_SCHEMA_VERSION = "0.1"
DEFAULT_TIMEOUT_SECONDS = 900.0
MAX_TIMEOUT_SECONDS = 3600.0
SENSITIVE_ENV_MARKERS = (
    "AUTH",
    "CREDENTIAL",
    "KEY",
    "PASSWORD",
    "SECRET",
    "SESSION",
    "TOKEN",
)
SENSITIVE_ASSIGNMENT = re.compile(
    r"(?i)\b(api[_-]?key|access[_ -]?code|authorization|password|passwd|"
    r"secret|serial(?:[_ -]?number)?|token)\b(\s*[:=]\s*)([^\s,;]+)"
)
USER_HOME_PATH = re.compile(r"(?<![A-Za-z0-9])/(?:Users|home)/[^/\s]+")
FULL_COMMIT = re.compile(r"[0-9a-fA-F]{40}")


def execute_bambu_slice(
    request: BambuSliceRequest,
    probe: SlicerProbe,
    *,
    run_dir: Path,
    provenance: FixtureProvenance,
    profile_root: Path | None = None,
    profile_provenance: ProfileProvenance | None = None,
    approved: bool,
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
) -> RunEvidence:
    """Execute one approved Bambu Studio process and write a portable manifest."""

    _validate_run_request(
        request,
        probe,
        run_dir=run_dir,
        provenance=provenance,
        profile_root=profile_root,
        profile_provenance=profile_provenance,
        approved=approved,
        timeout_seconds=timeout_seconds,
    )
    profile_store = BambuProfileStore(profile_root) if profile_root is not None else None
    resolved_run_dir = run_dir.expanduser().resolve()
    resolved_run_dir.mkdir(mode=0o700)
    output_dir = resolved_run_dir / "output"
    output_dir.mkdir(mode=0o700)
    private_home = resolved_run_dir / "home"
    private_home.mkdir(mode=0o700)
    private_tmp = resolved_run_dir / "tmp"
    private_tmp.mkdir(mode=0o700)

    isolated_request = replace(request, output_dir=output_dir)
    if profile_store is not None:
        assert request.machine_settings is not None
        assert request.process_settings is not None
        materialized = profile_store.materialize(
            machine=request.machine_settings,
            process=request.process_settings,
            filaments=request.filament_settings,
            destination=resolved_run_dir / "config",
        )
        isolated_request = replace(
            isolated_request,
            machine_settings=materialized.machine,
            process_settings=materialized.process,
            filament_settings=materialized.filaments,
        )
    command = build_bambu_slice_command(isolated_request)
    environment = _isolated_environment(private_home, private_tmp)
    started_at = datetime.now(UTC)
    started_clock = monotonic()
    timed_out = False
    exit_status: int | None
    stdout = ""
    stderr = ""

    try:
        completed = subprocess.run(
            command,
            cwd=resolved_run_dir,
            env=environment,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout_seconds,
            shell=False,
        )
        exit_status = completed.returncode
        stdout = completed.stdout
        stderr = completed.stderr
    except subprocess.TimeoutExpired as error:
        timed_out = True
        exit_status = None
        stdout = _timeout_text(error.stdout)
        stderr = _timeout_text(error.stderr)

    duration_seconds = monotonic() - started_clock
    redactions = _redaction_values(isolated_request, resolved_run_dir, private_home, private_tmp)
    redacted_log = _redact_log(
        _format_log(stdout, stderr, timed_out=timed_out),
        redactions=redactions,
    )
    log_path = resolved_run_dir / "slicer.log"
    log_path.write_text(redacted_log, encoding="utf-8")

    outputs = _fingerprint_output_tree(output_dir)
    manifest = _build_manifest(
        isolated_request,
        probe,
        provenance,
        source_request=request,
        profile_provenance=profile_provenance,
        command=command,
        started_at=started_at,
        duration_seconds=duration_seconds,
        exit_status=exit_status,
        timed_out=timed_out,
        outputs=outputs,
        log_path=log_path,
    )
    _assert_manifest_private(manifest)
    manifest_path = resolved_run_dir / "manifest.json"
    manifest_path.write_text(
        f"{json.dumps(manifest, indent=2, sort_keys=True)}\n",
        encoding="utf-8",
    )
    return RunEvidence(
        manifest_path=str(manifest_path),
        log_path=str(log_path),
        exit_status=exit_status,
        timed_out=timed_out,
        output_count=len(outputs),
    )


def _validate_run_request(
    request: BambuSliceRequest,
    probe: SlicerProbe,
    *,
    run_dir: Path,
    provenance: FixtureProvenance,
    profile_root: Path | None,
    profile_provenance: ProfileProvenance | None,
    approved: bool,
    timeout_seconds: float,
) -> None:
    if not approved:
        raise ValueError("slice execution requires explicit approval")
    if probe.slicer != "bambu" or not probe.available or not probe.executable:
        raise ValueError("Bambu Studio must be successfully probed before execution")
    if Path(probe.executable).expanduser().resolve() != request.executable.expanduser().resolve():
        raise ValueError("request executable does not match the successful probe")
    resolved_run_dir = run_dir.expanduser().resolve()
    if resolved_run_dir.exists():
        raise ValueError(f"run directory must not already exist: {run_dir}")
    if not resolved_run_dir.parent.is_dir():
        raise ValueError(f"run directory parent does not exist: {run_dir.parent}")
    if not 0 < timeout_seconds <= MAX_TIMEOUT_SECONDS:
        raise ValueError(
            f"timeout must be greater than 0 and at most {MAX_TIMEOUT_SECONDS:g} seconds"
        )
    _validate_provenance(
        provenance.source_url,
        provenance.source_commit,
        provenance.license,
        label="fixture",
    )
    if request.input_path.suffix.lower() == ".stl" and (
        profile_root is None or profile_provenance is None
    ):
        raise ValueError("STL execution requires a profile root and pinned profile provenance")
    if (profile_root is None) != (profile_provenance is None):
        raise ValueError("profile root and profile provenance must be provided together")
    if profile_provenance is not None:
        _validate_provenance(
            profile_provenance.source_url,
            profile_provenance.source_commit,
            profile_provenance.license,
            label="profile",
        )


def _validate_provenance(
    source_url: str,
    source_commit: str,
    license_name: str,
    *,
    label: str,
) -> None:
    if not source_url.startswith("https://"):
        raise ValueError(f"{label} source URL must use https")
    if FULL_COMMIT.fullmatch(source_commit) is None:
        raise ValueError(f"{label} source commit must be a full 40-character Git SHA")
    if not license_name.strip():
        raise ValueError(f"{label} license must be recorded")


def _isolated_environment(private_home: Path, private_tmp: Path) -> dict[str, str]:
    environment = {
        key: value
        for key, value in os.environ.items()
        if not any(marker in key.upper() for marker in SENSITIVE_ENV_MARKERS)
    }
    environment.update(
        {
            "HOME": str(private_home),
            "TMPDIR": str(private_tmp),
            "XDG_CACHE_HOME": str(private_home / ".cache"),
            "XDG_CONFIG_HOME": str(private_home / ".config"),
            "XDG_DATA_HOME": str(private_home / ".local" / "share"),
        }
    )
    return environment


def _timeout_text(value: str | bytes | None) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return value


def _format_log(stdout: str, stderr: str, *, timed_out: bool) -> str:
    status = "timeout" if timed_out else "completed"
    return f"[openprintbench] process={status}\n[stdout]\n{stdout}\n[stderr]\n{stderr}\n"


def _redaction_values(
    request: BambuSliceRequest,
    run_dir: Path,
    private_home: Path,
    private_tmp: Path,
) -> dict[str, str]:
    values = {
        str(Path.home()): "${HOME}",
        str(run_dir): "${RUN_DIR}",
        str(private_home): "${PRIVATE_HOME}",
        str(private_tmp): "${PRIVATE_TMP}",
        str(request.executable.expanduser().resolve()): "${SLICER}",
        str(request.input_path.expanduser().resolve()): "${INPUT}",
        str(request.output_dir.expanduser().resolve()): "${OUTPUT_DIR}",
    }
    if request.machine_settings is not None:
        values[str(request.machine_settings.expanduser().resolve())] = "${MACHINE_SETTINGS}"
    if request.process_settings is not None:
        values[str(request.process_settings.expanduser().resolve())] = "${PROCESS_SETTINGS}"
    for index, path in enumerate(request.filament_settings, start=1):
        values[str(path.expanduser().resolve())] = f"${{FILAMENT_SETTINGS_{index}}}"
    return values


def _redact_log(log: str, *, redactions: dict[str, str]) -> str:
    result = log
    for original, replacement in sorted(
        redactions.items(), key=lambda item: len(item[0]), reverse=True
    ):
        if original:
            result = result.replace(original, replacement)
    result = USER_HOME_PATH.sub("${HOME}", result)
    result = SENSITIVE_ASSIGNMENT.sub(
        lambda match: f"{match.group(1)}{match.group(2)}<redacted>", result
    )
    return result


def _fingerprint_output_tree(output_dir: Path) -> tuple[OutputFingerprint, ...]:
    fingerprints: list[OutputFingerprint] = []
    for path in sorted(output_dir.rglob("*")):
        if path.is_symlink():
            raise ValueError(
                f"output tree contains a symbolic link: {path.relative_to(output_dir)}"
            )
        if not path.is_file():
            continue
        fingerprint = fingerprint_file(path)
        fingerprints.append(
            OutputFingerprint(
                relative_path=path.relative_to(output_dir).as_posix(),
                size_bytes=fingerprint.size_bytes,
                sha256=fingerprint.sha256,
            )
        )
    return tuple(fingerprints)


def _build_manifest(
    request: BambuSliceRequest,
    probe: SlicerProbe,
    provenance: FixtureProvenance,
    source_request: BambuSliceRequest,
    profile_provenance: ProfileProvenance | None,
    *,
    command: tuple[str, ...],
    started_at: datetime,
    duration_seconds: float,
    exit_status: int | None,
    timed_out: bool,
    outputs: tuple[OutputFingerprint, ...],
    log_path: Path,
) -> dict[str, Any]:
    redactions = _redaction_values(
        request,
        request.output_dir.parent,
        request.output_dir.parent / "home",
        request.output_dir.parent / "tmp",
    )
    portable_command = [_replace_paths(item, redactions) for item in command]
    settings: dict[str, Any] = {
        "materializer": MATERIALIZER_VERSION if profile_provenance is not None else None,
        "provenance": profile_provenance.to_dict() if profile_provenance is not None else None,
        "sources": {
            "machine": _optional_fingerprint(source_request.machine_settings),
            "process": _optional_fingerprint(source_request.process_settings),
            "filaments": [
                fingerprint_file(path).to_dict() for path in source_request.filament_settings
            ],
        },
        "materialized": {
            "machine": _optional_fingerprint(request.machine_settings),
            "process": _optional_fingerprint(request.process_settings),
            "filaments": [fingerprint_file(path).to_dict() for path in request.filament_settings],
        },
    }
    log_fingerprint = fingerprint_file(log_path)
    return {
        "schema_version": RUN_SCHEMA_VERSION,
        "state": "executed",
        "approval": "explicit_cli_flag",
        "started_at": started_at.isoformat(),
        "duration_seconds": round(duration_seconds, 6),
        "exit_status": exit_status,
        "timed_out": timed_out,
        "slicer": {
            "name": probe.display_name,
            "version": probe.version,
            "executable": "${SLICER}",
        },
        "fixture": {
            **provenance.to_dict(),
            "input": fingerprint_file(request.input_path).to_dict(),
        },
        "settings": settings,
        "command": portable_command,
        "outputs": [output.to_dict() for output in outputs],
        "log": {
            "name": log_path.name,
            "size_bytes": log_fingerprint.size_bytes,
            "sha256": log_fingerprint.sha256,
        },
        "physical_validation": None,
    }


def _optional_fingerprint(path: Path | None) -> dict[str, Any] | None:
    return fingerprint_file(path).to_dict() if path is not None else None


def _replace_paths(value: str, redactions: dict[str, str]) -> str:
    result = value
    for original, replacement in sorted(
        redactions.items(), key=lambda item: len(item[0]), reverse=True
    ):
        if original:
            result = result.replace(original, replacement)
    return result


def _assert_manifest_private(manifest: dict[str, Any]) -> None:
    serialized = json.dumps(manifest, sort_keys=True)
    forbidden = {str(Path.home()), f"/Users/{getpass.getuser()}", f"/home/{getpass.getuser()}"}
    leaked = [value for value in forbidden if value and value in serialized]
    if leaked:
        raise ValueError("manifest contains a local home path")
    if SENSITIVE_ASSIGNMENT.search(serialized):
        raise ValueError("manifest contains a sensitive assignment")
