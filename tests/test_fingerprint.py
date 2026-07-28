from pathlib import Path

import pytest

from openprintbench.fingerprint import fingerprint_file


def test_fingerprint_known_content(tmp_path: Path) -> None:
    source = tmp_path / "cube.stl"
    source.write_bytes(b"solid cube\nendsolid cube\n")

    fingerprint = fingerprint_file(source)

    assert fingerprint.name == "cube.stl"
    assert fingerprint.size_bytes == 25
    assert fingerprint.sha256 == "8cc637a8ecc11adf765232489db0e0ed160c453c1292aaa729ead41daedf8f6e"


def test_fingerprint_rejects_missing_file(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="not a regular file"):
        fingerprint_file(tmp_path / "missing.stl")


def test_fingerprint_rejects_directory(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="not a regular file"):
        fingerprint_file(tmp_path)


def test_fingerprint_serializes(tmp_path: Path) -> None:
    source = tmp_path / "model.3mf"
    source.write_bytes(b"3mf")

    result = fingerprint_file(source).to_dict()

    assert result["name"] == "model.3mf"
    assert result["size_bytes"] == 3
    assert len(result["sha256"]) == 64
