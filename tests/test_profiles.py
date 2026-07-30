import json
from pathlib import Path

import pytest

from openprintbench.profiles import BambuProfileStore


def write_profile(root: Path, category: str, filename: str, payload: dict[str, object]) -> Path:
    path = root / category / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def test_materializer_merges_inheritance_and_includes(tmp_path: Path) -> None:
    root = tmp_path / "profiles"
    write_profile(root, "machine", "base.json", {"name": "base", "speed": "100"})
    write_profile(root, "machine", "template.json", {"name": "template", "gcode": "safe"})
    machine = write_profile(
        root,
        "machine",
        "leaf.json",
        {
            "name": "leaf",
            "inherits": "base",
            "include": ["template"],
            "speed": "200",
        },
    )
    process = write_profile(root, "process", "process.json", {"name": "process"})
    filament = write_profile(root, "filament", "filament.json", {"name": "filament"})

    result = BambuProfileStore(root).materialize(
        machine=machine,
        process=process,
        filaments=(filament,),
        destination=tmp_path / "materialized",
    )

    payload = json.loads(result.machine.read_text(encoding="utf-8"))
    assert payload["name"] == "leaf"
    assert payload["speed"] == "200"
    assert payload["gcode"] == "safe"
    assert payload["from"] == "User"
    assert payload["inherits"] == "leaf"
    assert len(result.filaments) == 1


def test_materializer_rejects_unresolved_parent(tmp_path: Path) -> None:
    root = tmp_path / "profiles"
    machine = write_profile(
        root,
        "machine",
        "machine.json",
        {"name": "machine", "inherits": "missing"},
    )
    process = write_profile(root, "process", "process.json", {"name": "process"})
    filament = write_profile(root, "filament", "filament.json", {"name": "filament"})

    with pytest.raises(ValueError, match="unresolved"):
        BambuProfileStore(root).materialize(
            machine=machine,
            process=process,
            filaments=(filament,),
            destination=tmp_path / "materialized",
        )


def test_materializer_rejects_source_outside_tree(tmp_path: Path) -> None:
    root = tmp_path / "profiles"
    write_profile(root, "machine", "machine.json", {"name": "machine"})
    process = write_profile(root, "process", "process.json", {"name": "process"})
    filament = write_profile(root, "filament", "filament.json", {"name": "filament"})
    outside = tmp_path / "outside.json"
    outside.write_text('{"name": "outside"}', encoding="utf-8")

    with pytest.raises(ValueError, match="outside"):
        BambuProfileStore(root).materialize(
            machine=outside,
            process=process,
            filaments=(filament,),
            destination=tmp_path / "materialized",
        )
