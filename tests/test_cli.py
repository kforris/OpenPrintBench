import json
from pathlib import Path

import pytest

from openprintbench.cli import main
from openprintbench.models import SlicerProbe


def test_doctor_json_is_machine_readable(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(
        "openprintbench.cli.probe_slicer",
        lambda name, explicit=None: SlicerProbe(
            name,
            name,
            name == "bambu",
            "/fake/slicer" if name == "bambu" else None,
            "1.0.0" if name == "bambu" else None,
            "test",
        ),
    )

    assert main(["doctor", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert len(payload) == 2
    assert payload[0]["slicer"] == "bambu"


def test_orca_plan_is_explicitly_unimplemented() -> None:
    with pytest.raises(SystemExit) as error:
        main(
            [
                "plan",
                "--slicer",
                "orca",
                "--input",
                "model.3mf",
                "--output-dir",
                "run",
            ]
        )
    assert error.value.code == 2


def test_plan_writes_portable_manifest(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    executable = tmp_path / "BambuStudio"
    executable.write_text("#!/bin/sh\n", encoding="utf-8")
    executable.chmod(0o755)
    source = tmp_path / "project.3mf"
    source.write_bytes(b"3mf")
    manifest = tmp_path / "manifest.json"
    monkeypatch.setattr(
        "openprintbench.cli.probe_slicer",
        lambda name, explicit=None: SlicerProbe(
            "bambu",
            "Bambu Studio",
            True,
            str(executable),
            "2.6.0.51",
            "test",
        ),
    )

    assert (
        main(
            [
                "plan",
                "--input",
                str(source),
                "--output-dir",
                str(tmp_path / "run"),
                "--manifest",
                str(manifest),
            ]
        )
        == 0
    )
    stdout_payload = json.loads(capsys.readouterr().out)
    file_payload = json.loads(manifest.read_text(encoding="utf-8"))
    assert stdout_payload == file_payload
    assert "${INPUT}" in file_payload["command"]
