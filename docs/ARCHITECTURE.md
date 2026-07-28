# Architecture

OpenPrintBench separates four evidence states:

1. **Probe** — a slicer executable was discovered and identified.
2. **Plan** — an argument array and input fingerprint were generated.
3. **Run** — the slicer process executed and produced captured outputs.
4. **Physical validation** — a human verified a print using a documented
   protocol.

No state implies the next state.

The Python package currently contains:

- `discovery.py` — executable discovery and version probing;
- `slicers/` — slicer-specific command construction;
- `fingerprint.py` — streaming SHA-256 file fingerprints;
- `plan.py` — portable JSON plan assembly;
- `profiles.py` — pinned, local Bambu profile inheritance materialization;
- `run.py` — explicit approval, isolated process execution, output
  fingerprinting, and privacy-reviewed run manifests;
- `cli.py` — user-facing `doctor`, `plan`, and `run` commands.

Slicers are executed as separate local processes using argument arrays.
OpenPrintBench does not link to, embed, or redistribute slicer code.

## Run isolation

Execution is opt-in and creates a new run directory. The slicer receives that
directory as its working directory, a private `HOME`, a private temporary
directory, and an environment with secret-like variables removed. Existing run
directories are rejected to avoid mixing evidence.

The run manifest uses placeholders instead of machine-local paths. It records
the full fixture source commit and license, input/settings hashes, slicer
version, start time, duration, exit status, timeout state, output hashes, and
the hash of a redacted log. It sets `state` to `executed` and keeps
`physical_validation` null; a successful process does not imply a physical
print.

For a bare STL, Bambu Studio's CLI needs complete machine, process, and
filament configuration. OpenPrintBench recursively resolves `inherits` and
`include` references from a user-installed profile tree, then writes complete
profiles inside the private run directory. The source tree commit, license,
leaf hashes, materializer version, and resulting hashes are recorded. Profile
source files and generated slicer outputs are never added to the repository.
