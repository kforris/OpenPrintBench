"""OpenPrintBench command-line interface."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from pathlib import Path

from openprintbench import __version__
from openprintbench.discovery import DEFINITIONS, probe_slicer
from openprintbench.plan import create_bambu_plan, portable_plan
from openprintbench.slicers.bambu import BambuSliceRequest


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""

    parser = argparse.ArgumentParser(prog="openprintbench")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    subparsers = parser.add_subparsers(dest="command", required=True)

    doctor = subparsers.add_parser("doctor", help="discover local slicers")
    doctor.add_argument("--json", action="store_true", help="emit machine-readable JSON")

    plan = subparsers.add_parser("plan", help="create a non-executed slice plan")
    plan.add_argument("--slicer", choices=tuple(DEFINITIONS), default="bambu")
    plan.add_argument("--executable", type=Path)
    plan.add_argument("--input", type=Path, required=True)
    plan.add_argument("--output-dir", type=Path, required=True)
    plan.add_argument("--output-name", default="sliced.3mf")
    plan.add_argument("--plate", type=int, default=0)
    plan.add_argument("--debug-level", type=int, default=2)
    plan.add_argument("--machine-settings", type=Path)
    plan.add_argument("--process-settings", type=Path)
    plan.add_argument("--filament-settings", type=Path, action="append", default=[])
    plan.add_argument("--manifest", type=Path, help="write the portable JSON plan")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the CLI and return a process exit code."""

    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "doctor":
            return _doctor(as_json=args.json)
        if args.command == "plan":
            return _plan(args)
    except ValueError as error:
        parser.error(str(error))

    parser.error(f"unsupported command: {args.command}")
    return 2


def _doctor(*, as_json: bool) -> int:
    probes = [probe_slicer(name) for name in DEFINITIONS]
    if as_json:
        print(json.dumps([probe.to_dict() for probe in probes], indent=2, sort_keys=True))
    else:
        for probe in probes:
            status = "available" if probe.available else "missing"
            version = f" {probe.version}" if probe.version else ""
            print(f"{probe.display_name}: {status}{version}")
    return 0


def _plan(args: argparse.Namespace) -> int:
    if args.slicer != "bambu":
        raise ValueError("OrcaSlicer planning is not implemented yet; use doctor to probe it")

    probe = probe_slicer("bambu", args.executable)
    if not probe.available or probe.executable is None:
        raise ValueError(f"Bambu Studio probe failed: {probe.error or 'unknown error'}")

    request = BambuSliceRequest(
        executable=Path(probe.executable),
        input_path=args.input,
        output_dir=args.output_dir,
        output_name=args.output_name,
        plate=args.plate,
        debug_level=args.debug_level,
        machine_settings=args.machine_settings,
        process_settings=args.process_settings,
        filament_settings=tuple(args.filament_settings),
    )
    plan = create_bambu_plan(request, probe)
    serialized = portable_plan(plan, args.input, args.output_dir)
    output = json.dumps(serialized, indent=2, sort_keys=True)
    print(output)

    if args.manifest:
        destination = args.manifest.expanduser().resolve()
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(f"{output}\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
