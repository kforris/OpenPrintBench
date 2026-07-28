from pathlib import Path

import pytest

from openprintbench.models import SlicerProbe
from openprintbench.plan import create_bambu_plan, portable_plan
from openprintbench.slicers.bambu import BambuSliceRequest


@pytest.fixture
def setup_paths(tmp_path: Path) -> tuple[Path, Path]:
    executable = tmp_path / "BambuStudio"
    executable.write_text("#!/bin/sh\n", encoding="utf-8")
    executable.chmod(0o755)
    source = tmp_path / "project.3mf"
    source.write_bytes(b"3mf")
    return executable, source


def available_probe(executable: Path) -> SlicerProbe:
    return SlicerProbe(
        slicer="bambu",
        display_name="Bambu Studio",
        available=True,
        executable=str(executable.resolve()),
        version="2.6.0.51",
        source="explicit",
    )


def test_plan_state_is_truthful(setup_paths: tuple[Path, Path], tmp_path: Path) -> None:
    executable, source = setup_paths

    plan = create_bambu_plan(
        BambuSliceRequest(executable, source, tmp_path / "run"),
        available_probe(executable),
    )

    assert plan.state == "planned"
    assert plan.schema_version == "0.1"
    assert plan.input.name == "project.3mf"


def test_plan_rejects_wrong_probe(setup_paths: tuple[Path, Path], tmp_path: Path) -> None:
    executable, source = setup_paths
    probe = SlicerProbe("orca", "OrcaSlicer", True, str(executable), "2.3.1", "explicit")

    with pytest.raises(ValueError, match="Bambu"):
        create_bambu_plan(BambuSliceRequest(executable, source, tmp_path), probe)


def test_plan_rejects_unavailable_probe(setup_paths: tuple[Path, Path], tmp_path: Path) -> None:
    executable, source = setup_paths
    probe = SlicerProbe("bambu", "Bambu Studio", False, None, None, None, "missing")

    with pytest.raises(ValueError, match="not available"):
        create_bambu_plan(BambuSliceRequest(executable, source, tmp_path), probe)


def test_portable_plan_redacts_input_and_output_paths(
    setup_paths: tuple[Path, Path], tmp_path: Path
) -> None:
    executable, source = setup_paths
    output_dir = tmp_path / "run"
    plan = create_bambu_plan(
        BambuSliceRequest(executable, source, output_dir),
        available_probe(executable),
    )

    serialized = portable_plan(plan, source, output_dir)

    assert "${INPUT}" in serialized["command"]
    assert "${OUTPUT_DIR}" in serialized["command"]
    assert str(source.resolve()) not in serialized["command"]
