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
- `cli.py` — user-facing `doctor` and `plan` commands.

Slicers are executed as separate local processes using argument arrays.
OpenPrintBench does not link to, embed, or redistribute slicer code.
