import json
import textwrap
from pathlib import Path

import pytest

from openprintbench.models import FixtureProvenance, ProfileProvenance, SlicerProbe
from openprintbench.run import execute_bambu_slice
from openprintbench.slicers.bambu import BambuSliceRequest

SOURCE_COMMIT = "a" * 40
SOURCE_URL = (
    f"https://github.com/kforris/OpenPrintBench/blob/{SOURCE_COMMIT}/fixtures/cube-20mm.stl"
)
PROFILE_COMMIT = "b" * 40


def make_fake_slicer(path: Path, *, exit_status: int = 0, sleep_seconds: float = 0) -> Path:
    path.write_text(
        textwrap.dedent(
            f"""\
            #!/usr/bin/env python3
            import pathlib
            import sys
            import time

            time.sleep({sleep_seconds})
            output_dir = pathlib.Path(sys.argv[sys.argv.index("--outputdir") + 1])
            output_name = sys.argv[sys.argv.index("--export-3mf") + 1]
            output_dir.mkdir(parents=True, exist_ok=True)
            (output_dir / output_name).write_bytes(b"deterministic fake slice")
            print("/Users/example/private token=visible access_code=1234")
            print("stderr password=hunter2", file=sys.stderr)
            raise SystemExit({exit_status})
            """
        ),
        encoding="utf-8",
    )
    path.chmod(0o755)
    return path


def available_probe(executable: Path) -> SlicerProbe:
    return SlicerProbe(
        slicer="bambu",
        display_name="Bambu Studio",
        available=True,
        executable=str(executable.resolve()),
        version="02.06.00.51",
        source="explicit",
    )


def provenance() -> FixtureProvenance:
    return FixtureProvenance(
        source_url=SOURCE_URL,
        source_commit=SOURCE_COMMIT,
        license="CC0-1.0",
    )


def profile_provenance() -> ProfileProvenance:
    return ProfileProvenance(
        source_url=f"https://github.com/bambulab/BambuStudio/tree/{PROFILE_COMMIT}/profiles",
        source_commit=PROFILE_COMMIT,
        license="AGPL-3.0-only",
    )


def stl_request(tmp_path: Path, executable: Path) -> BambuSliceRequest:
    source = tmp_path / "cube-20mm.stl"
    source.write_text("solid cube\nendsolid cube\n", encoding="utf-8")
    profile_root = tmp_path / "profiles"
    machine = profile_root / "machine" / "machine.json"
    process = profile_root / "process" / "process.json"
    filament = profile_root / "filament" / "filament.json"
    for path, category in (
        (machine, "machine"),
        (process, "process"),
        (filament, "filament"),
    ):
        path.parent.mkdir(parents=True)
        path.write_text(
            json.dumps({"type": category, "name": f"test-{category}"}),
            encoding="utf-8",
        )
    return BambuSliceRequest(
        executable=executable,
        input_path=source,
        output_dir=tmp_path / "unused",
        machine_settings=machine,
        process_settings=process,
        filament_settings=(filament,),
    )


def profile_kwargs(tmp_path: Path) -> dict[str, object]:
    return {
        "profile_root": tmp_path / "profiles",
        "profile_provenance": profile_provenance(),
    }


def test_success_writes_portable_manifest_and_redacted_log(tmp_path: Path) -> None:
    executable = make_fake_slicer(tmp_path / "BambuStudio")
    request = stl_request(tmp_path, executable)
    run_dir = tmp_path / "run"

    evidence = execute_bambu_slice(
        request,
        available_probe(executable),
        run_dir=run_dir,
        provenance=provenance(),
        approved=True,
        **profile_kwargs(tmp_path),
    )

    assert evidence.succeeded is True
    assert evidence.output_count == 1
    assert run_dir.stat().st_mode & 0o777 == 0o700
    manifest = json.loads(Path(evidence.manifest_path).read_text(encoding="utf-8"))
    serialized = json.dumps(manifest)
    assert manifest["state"] == "executed"
    assert manifest["fixture"]["source_commit"] == SOURCE_COMMIT
    assert manifest["fixture"]["license"] == "CC0-1.0"
    assert manifest["settings"]["materializer"] == "openprintbench-bambu-profile-merge-v1"
    assert manifest["settings"]["provenance"]["source_commit"] == PROFILE_COMMIT
    assert manifest["settings"]["sources"]["machine"]["name"] == "machine.json"
    assert manifest["settings"]["materialized"]["machine"]["name"] == "machine.json"
    assert manifest["exit_status"] == 0
    assert manifest["timed_out"] is False
    assert manifest["physical_validation"] is None
    assert manifest["outputs"][0]["relative_path"] == "sliced.3mf"
    assert "${SLICER}" in manifest["command"]
    assert "${INPUT}" in manifest["command"]
    assert "${OUTPUT_DIR}" in manifest["command"]
    portable_command = " ".join(manifest["command"])
    assert "${MACHINE_SETTINGS}" in portable_command
    assert "${PROCESS_SETTINGS}" in portable_command
    assert "${FILAMENT_SETTINGS_1}" in portable_command
    assert str(tmp_path) not in serialized
    log = Path(evidence.log_path).read_text(encoding="utf-8")
    assert "/Users/example" not in log
    assert "visible" not in log
    assert "hunter2" not in log
    assert log.count("<redacted>") == 3


def test_approval_is_required_before_run_directory_creation(tmp_path: Path) -> None:
    executable = make_fake_slicer(tmp_path / "BambuStudio")
    run_dir = tmp_path / "run"

    with pytest.raises(ValueError, match="explicit approval"):
        execute_bambu_slice(
            stl_request(tmp_path, executable),
            available_probe(executable),
            run_dir=run_dir,
            provenance=provenance(),
            approved=False,
        )

    assert not run_dir.exists()


def test_existing_run_directory_is_rejected(tmp_path: Path) -> None:
    executable = make_fake_slicer(tmp_path / "BambuStudio")
    run_dir = tmp_path / "run"
    run_dir.mkdir()

    with pytest.raises(ValueError, match="must not already exist"):
        execute_bambu_slice(
            stl_request(tmp_path, executable),
            available_probe(executable),
            run_dir=run_dir,
            provenance=provenance(),
            approved=True,
            **profile_kwargs(tmp_path),
        )


def test_nonzero_exit_still_writes_evidence(tmp_path: Path) -> None:
    executable = make_fake_slicer(tmp_path / "BambuStudio", exit_status=7)

    evidence = execute_bambu_slice(
        stl_request(tmp_path, executable),
        available_probe(executable),
        run_dir=tmp_path / "run",
        provenance=provenance(),
        approved=True,
        **profile_kwargs(tmp_path),
    )

    manifest = json.loads(Path(evidence.manifest_path).read_text(encoding="utf-8"))
    assert evidence.succeeded is False
    assert evidence.exit_status == 7
    assert manifest["exit_status"] == 7
    assert manifest["outputs"]


def test_timeout_is_recorded_without_an_exit_status(tmp_path: Path) -> None:
    executable = make_fake_slicer(tmp_path / "BambuStudio", sleep_seconds=0.2)

    evidence = execute_bambu_slice(
        stl_request(tmp_path, executable),
        available_probe(executable),
        run_dir=tmp_path / "run",
        provenance=provenance(),
        approved=True,
        timeout_seconds=0.01,
        **profile_kwargs(tmp_path),
    )

    manifest = json.loads(Path(evidence.manifest_path).read_text(encoding="utf-8"))
    assert evidence.succeeded is False
    assert evidence.timed_out is True
    assert manifest["timed_out"] is True
    assert manifest["exit_status"] is None


@pytest.mark.parametrize(
    "source_commit",
    ["short", "z" * 40],
)
def test_provenance_requires_full_git_sha(tmp_path: Path, source_commit: str) -> None:
    executable = make_fake_slicer(tmp_path / "BambuStudio")

    with pytest.raises(ValueError, match="full 40-character"):
        execute_bambu_slice(
            stl_request(tmp_path, executable),
            available_probe(executable),
            run_dir=tmp_path / "run",
            provenance=FixtureProvenance(SOURCE_URL, source_commit, "CC0-1.0"),
            approved=True,
        )


def test_timeout_is_bounded(tmp_path: Path) -> None:
    executable = make_fake_slicer(tmp_path / "BambuStudio")

    with pytest.raises(ValueError, match="timeout"):
        execute_bambu_slice(
            stl_request(tmp_path, executable),
            available_probe(executable),
            run_dir=tmp_path / "run",
            provenance=provenance(),
            approved=True,
            timeout_seconds=0,
        )


def test_stl_execution_requires_profile_provenance(tmp_path: Path) -> None:
    executable = make_fake_slicer(tmp_path / "BambuStudio")

    with pytest.raises(ValueError, match="profile root"):
        execute_bambu_slice(
            stl_request(tmp_path, executable),
            available_probe(executable),
            run_dir=tmp_path / "run",
            provenance=provenance(),
            approved=True,
        )
