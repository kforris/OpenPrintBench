import subprocess
from pathlib import Path

import pytest

from openprintbench.discovery import BAMBU, SlicerDiscovery, parse_version, probe_slicer


@pytest.mark.parametrize(
    ("output", "expected"),
    [
        ("BambuStudio-02.06.00.51:", "02.06.00.51"),
        ("OrcaSlicer 2.3.1", "2.3.1"),
        ("version: 1.2.3", "1.2.3"),
        ("no version here", None),
    ],
)
def test_parse_version(output: str, expected: str | None) -> None:
    assert parse_version(output) == expected


def test_explicit_non_executable_is_rejected(tmp_path: Path) -> None:
    candidate = tmp_path / "slicer"
    candidate.write_text("not executable", encoding="utf-8")

    located, source = SlicerDiscovery(BAMBU).locate(candidate)

    assert located is None
    assert source is None


def test_environment_candidate_has_priority(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    candidate = tmp_path / "bambu"
    candidate.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
    candidate.chmod(0o755)
    monkeypatch.setenv(BAMBU.env_var, str(candidate))

    located, source = SlicerDiscovery(BAMBU).locate()

    assert located == candidate.resolve()
    assert source == f"environment:{BAMBU.env_var}"


def test_probe_rejects_unknown_slicer() -> None:
    with pytest.raises(ValueError, match="unsupported slicer"):
        probe_slicer("unknown")


def test_probe_success(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    candidate = tmp_path / "BambuStudio"
    candidate.write_text("#!/bin/sh\n", encoding="utf-8")
    candidate.chmod(0o755)
    observed_cwd: list[str] = []

    def successful_help(*args: object, **kwargs: object) -> subprocess.CompletedProcess[str]:
        observed_cwd.append(str(kwargs["cwd"]))
        return subprocess.CompletedProcess(args[0], 0, "BambuStudio-02.06.00.51:\n", "")

    monkeypatch.setattr(
        subprocess,
        "run",
        successful_help,
    )

    probe = SlicerDiscovery(BAMBU).probe(candidate)

    assert probe.available is True
    assert probe.version == "02.06.00.51"
    assert probe.error is None
    assert len(observed_cwd) == 1
    assert "openprintbench-probe-" in observed_cwd[0]


def test_probe_reports_nonzero_help(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    candidate = tmp_path / "BambuStudio"
    candidate.write_text("#!/bin/sh\n", encoding="utf-8")
    candidate.chmod(0o755)
    monkeypatch.setattr(
        subprocess,
        "run",
        lambda *args, **kwargs: subprocess.CompletedProcess(args[0], 7, "", "failed"),
    )

    probe = SlicerDiscovery(BAMBU).probe(candidate)

    assert probe.available is False
    assert probe.error == "help exited 7"


def test_probe_reports_timeout(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    candidate = tmp_path / "BambuStudio"
    candidate.write_text("#!/bin/sh\n", encoding="utf-8")
    candidate.chmod(0o755)

    def raise_timeout(*args: object, **kwargs: object) -> None:
        raise subprocess.TimeoutExpired(cmd="BambuStudio", timeout=12)

    monkeypatch.setattr(subprocess, "run", raise_timeout)

    probe = SlicerDiscovery(BAMBU).probe(candidate)

    assert probe.available is False
    assert probe.error == "TimeoutExpired"
