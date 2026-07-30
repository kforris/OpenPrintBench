"""Materialize complete Bambu CLI profiles from installed profile inheritance."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

PROFILE_CATEGORIES = ("machine", "process", "filament")
MATERIALIZER_VERSION = "openprintbench-bambu-profile-merge-v1"


@dataclass(frozen=True, slots=True)
class MaterializedProfiles:
    """Paths to complete profile JSON written inside one isolated run."""

    machine: Path
    process: Path
    filaments: tuple[Path, ...]


class BambuProfileStore:
    """Resolve named profile inheritance from an installed BBL profile tree."""

    def __init__(self, root: Path) -> None:
        self.root = root.expanduser().resolve()
        if not self.root.is_dir():
            raise ValueError(f"Bambu profile root is not a directory: {root}")
        self._indexes = {category: self._build_index(category) for category in PROFILE_CATEGORIES}

    def materialize(
        self,
        *,
        machine: Path,
        process: Path,
        filaments: tuple[Path, ...],
        destination: Path,
    ) -> MaterializedProfiles:
        """Write complete profiles under a private run directory."""

        if not filaments:
            raise ValueError("at least one filament profile is required")
        prepared = {
            "machine": (machine, "machine.json"),
            "process": (process, "process.json"),
        }
        destination.mkdir(mode=0o700)
        written: dict[str, Path] = {}
        for category, (source, name) in prepared.items():
            written[category] = self._write_profile(category, source, destination / name)

        filament_paths = tuple(
            self._write_profile(
                "filament",
                source,
                destination / f"filament-{index}.json",
            )
            for index, source in enumerate(filaments, start=1)
        )
        return MaterializedProfiles(
            machine=written["machine"],
            process=written["process"],
            filaments=filament_paths,
        )

    def _build_index(self, category: str) -> dict[str, tuple[Path, dict[str, Any]]]:
        category_root = self.root / category
        if not category_root.is_dir():
            raise ValueError(f"Bambu profile category is missing: {category_root}")
        index: dict[str, tuple[Path, dict[str, Any]]] = {}
        for path in sorted(category_root.rglob("*.json")):
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as error:
                raise ValueError(f"invalid Bambu profile JSON: {path}") from error
            if not isinstance(data, dict):
                raise ValueError(f"Bambu profile must contain a JSON object: {path}")
            name = data.get("name")
            if not isinstance(name, str) or not name:
                continue
            if name in index:
                raise ValueError(f"duplicate Bambu profile name in {category}: {name}")
            index[name] = (path.resolve(), data)
        return index

    def _write_profile(self, category: str, source: Path, destination: Path) -> Path:
        resolved_source = source.expanduser().resolve()
        index = self._indexes[category]
        source_entry = next(
            (entry for entry in index.values() if entry[0] == resolved_source),
            None,
        )
        if source_entry is None:
            raise ValueError(f"{category} profile is outside the indexed profile tree: {source}")
        leaf = source_entry[1]
        leaf_name = leaf["name"]
        assert isinstance(leaf_name, str)
        merged = self._resolve(category, leaf_name, stack=())
        merged["from"] = "User"
        merged["inherits"] = leaf_name
        destination.write_text(
            f"{json.dumps(merged, indent=2, sort_keys=True)}\n",
            encoding="utf-8",
        )
        return destination

    def _resolve(
        self,
        category: str,
        name: str,
        *,
        stack: tuple[str, ...],
    ) -> dict[str, Any]:
        if name in stack:
            chain = " -> ".join((*stack, name))
            raise ValueError(f"cyclic Bambu profile inheritance: {chain}")
        try:
            _, data = self._indexes[category][name]
        except KeyError as error:
            raise ValueError(f"unresolved Bambu {category} profile: {name}") from error

        merged: dict[str, Any] = {}
        next_stack = (*stack, name)
        parent = data.get("inherits")
        if isinstance(parent, str) and parent:
            merged.update(self._resolve(category, parent, stack=next_stack))
        includes = data.get("include", [])
        if not isinstance(includes, list) or not all(isinstance(item, str) for item in includes):
            raise ValueError(f"invalid include list in Bambu {category} profile: {name}")
        for include in includes:
            merged.update(self._resolve(category, include, stack=next_stack))
        merged.update(data)
        return merged
