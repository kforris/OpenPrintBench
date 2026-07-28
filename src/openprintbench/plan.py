"""Assemble truthful, machine-readable slice plans."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from openprintbench.fingerprint import fingerprint_file
from openprintbench.models import SlicePlan, SlicerProbe
from openprintbench.slicers.bambu import BambuSliceRequest, build_bambu_slice_command

SCHEMA_VERSION = "0.1"


def create_bambu_plan(request: BambuSliceRequest, probe: SlicerProbe) -> SlicePlan:
    """Create a plan only after a successful Bambu Studio probe."""

    if probe.slicer != "bambu":
        raise ValueError("Bambu plan requires a Bambu Studio probe")
    if not probe.available or not probe.executable:
        raise ValueError("Bambu Studio is not available")

    command = build_bambu_slice_command(request)
    return SlicePlan(
        schema_version=SCHEMA_VERSION,
        state="planned",
        created_at=datetime.now(UTC).isoformat(),
        slicer=probe,
        input=fingerprint_file(request.input_path),
        plate=request.plate,
        output_name=request.output_name,
        command=command,
    )


def portable_plan(plan: SlicePlan, input_path: Path, output_dir: Path) -> dict[str, object]:
    """Replace machine-local model/output paths in a serialized plan."""

    data = plan.to_dict()
    command = list(plan.command)
    replacements = {
        str(input_path.expanduser().resolve()): "${INPUT}",
        str(output_dir.expanduser().resolve()): "${OUTPUT_DIR}",
    }
    data["command"] = [replacements.get(item, item) for item in command]
    return data
