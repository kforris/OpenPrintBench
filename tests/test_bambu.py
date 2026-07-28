from pathlib import Path

import pytest

from openprintbench.slicers.bambu import BambuSliceRequest, build_bambu_slice_command


@pytest.fixture
def executable(tmp_path: Path) -> Path:
    path = tmp_path / "BambuStudio"
    path.write_text("#!/bin/sh\n", encoding="utf-8")
    path.chmod(0o755)
    return path


def test_3mf_plan_uses_embedded_settings(executable: Path, tmp_path: Path) -> None:
    source = tmp_path / "project.3mf"
    source.write_bytes(b"3mf")

    command = build_bambu_slice_command(
        BambuSliceRequest(
            executable=executable,
            input_path=source,
            output_dir=tmp_path / "output",
        )
    )

    assert command[0] == str(executable.resolve())
    assert command[-1] == str(source.resolve())
    assert "--slice" in command
    assert "--load-settings" not in command
    assert "--load-filaments" not in command


def test_stl_requires_all_settings(executable: Path, tmp_path: Path) -> None:
    source = tmp_path / "model.stl"
    source.write_text("solid model\nendsolid model\n", encoding="utf-8")

    with pytest.raises(ValueError, match="requires machine, process"):
        build_bambu_slice_command(
            BambuSliceRequest(
                executable=executable,
                input_path=source,
                output_dir=tmp_path / "output",
            )
        )


def test_stl_includes_settings(executable: Path, tmp_path: Path) -> None:
    source = tmp_path / "model.stl"
    machine = tmp_path / "machine.json"
    process = tmp_path / "process.json"
    filament = tmp_path / "filament.json"
    for path in (machine, process, filament):
        path.write_text("{}", encoding="utf-8")
    source.write_text("solid model\nendsolid model\n", encoding="utf-8")

    command = build_bambu_slice_command(
        BambuSliceRequest(
            executable=executable,
            input_path=source,
            output_dir=tmp_path / "output",
            machine_settings=machine,
            process_settings=process,
            filament_settings=(filament,),
        )
    )

    settings_index = command.index("--load-settings")
    filament_index = command.index("--load-filaments")
    assert command[settings_index + 1] == f"{machine.resolve()};{process.resolve()}"
    assert command[filament_index + 1] == str(filament.resolve())


@pytest.mark.parametrize("plate", [-1, -10])
def test_plate_must_be_non_negative(executable: Path, tmp_path: Path, plate: int) -> None:
    source = tmp_path / "project.3mf"
    source.write_bytes(b"3mf")

    with pytest.raises(ValueError, match="plate"):
        build_bambu_slice_command(
            BambuSliceRequest(
                executable=executable,
                input_path=source,
                output_dir=tmp_path,
                plate=plate,
            )
        )


@pytest.mark.parametrize("debug_level", [-1, 6])
def test_debug_level_is_bounded(executable: Path, tmp_path: Path, debug_level: int) -> None:
    source = tmp_path / "project.3mf"
    source.write_bytes(b"3mf")

    with pytest.raises(ValueError, match="debug level"):
        build_bambu_slice_command(
            BambuSliceRequest(
                executable=executable,
                input_path=source,
                output_dir=tmp_path,
                debug_level=debug_level,
            )
        )


@pytest.mark.parametrize("output_name", ["../escape.3mf", "nested/result.3mf", "result.gcode"])
def test_output_name_is_safe(executable: Path, tmp_path: Path, output_name: str) -> None:
    source = tmp_path / "project.3mf"
    source.write_bytes(b"3mf")

    with pytest.raises(ValueError, match="output name"):
        build_bambu_slice_command(
            BambuSliceRequest(
                executable=executable,
                input_path=source,
                output_dir=tmp_path,
                output_name=output_name,
            )
        )


def test_input_suffix_is_limited(executable: Path, tmp_path: Path) -> None:
    source = tmp_path / "model.obj"
    source.write_text("obj", encoding="utf-8")

    with pytest.raises(ValueError, match="unsupported input type"):
        build_bambu_slice_command(
            BambuSliceRequest(
                executable=executable,
                input_path=source,
                output_dir=tmp_path,
            )
        )
