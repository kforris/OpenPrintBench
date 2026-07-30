"""OpenPrintBench command-line interface."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from pathlib import Path

from openprintbench import __version__
from openprintbench.discovery import DEFINITIONS, probe_slicer
from openprintbench.models import FixtureProvenance, ProfileProvenance
from openprintbench.plan import create_bambu_plan, portable_plan
from openprintbench.run import execute_bambu_slice
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

    run = subparsers.add_parser("run", help="execute one explicitly approved isolated slice")
    run.add_argument("--slicer", choices=("bambu",), default="bambu")
    run.add_argument("--executable", type=Path)
    run.add_argument("--input", type=Path, required=True)
    run.add_argument("--run-dir", type=Path, required=True)
    run.add_argument("--output-name", default="sliced.3mf")
    run.add_argument("--plate", type=int, default=0)
    run.add_argument("--debug-level", type=int, default=2)
    run.add_argument("--machine-settings", type=Path)
    run.add_argument("--process-settings", type=Path)
    run.add_argument("--filament-settings", type=Path, action="append", default=[])
    run.add_argument("--fixture-source-url", required=True)
    run.add_argument("--fixture-source-commit", required=True)
    run.add_argument("--fixture-license", required=True)
    run.add_argument("--profile-root", type=Path)
    run.add_argument("--profile-source-url")
    run.add_argument("--profile-source-commit")
    run.add_argument("--profile-license")
    run.add_argument("--timeout-seconds", type=float, default=900.0)
    run.add_argument(
        "--approve",
        action="store_true",
        help="explicitly approve launching the local slicer process",
    )
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
        if args.command == "run":
            return _run(args)
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


def _run(args: argparse.Namespace) -> int:
    probe = probe_slicer("bambu", args.executable)
    if not probe.available or probe.executable is None:
        raise ValueError(f"Bambu Studio probe failed: {probe.error or 'unknown error'}")

    run_dir = args.run_dir.expanduser().resolve()
    request = BambuSliceRequest(
        executable=Path(probe.executable),
        input_path=args.input,
        output_dir=run_dir / "output",
        output_name=args.output_name,
        plate=args.plate,
        debug_level=args.debug_level,
        machine_settings=args.machine_settings,
        process_settings=args.process_settings,
        filament_settings=tuple(args.filament_settings),
    )
    profile_values = (
        args.profile_source_url,
        args.profile_source_commit,
        args.profile_license,
    )
    if any(profile_values) and not all(profile_values):
        raise ValueError("profile source URL, commit, and license must be provided together")
    profile_provenance = ProfileProvenance(*profile_values) if all(profile_values) else None
    evidence = execute_bambu_slice(
        request,
        probe,
        run_dir=run_dir,
        provenance=FixtureProvenance(
            source_url=args.fixture_source_url,
            source_commit=args.fixture_source_commit,
            license=args.fixture_license,
        ),
        profile_root=args.profile_root,
        profile_provenance=profile_provenance,
        approved=args.approve,
        timeout_seconds=args.timeout_seconds,
    )
    print(Path(evidence.manifest_path).read_text(encoding="utf-8"), end="")
    return 0 if evidence.succeeded else 1


if __name__ == "__main__":
    sys.exit(main())
