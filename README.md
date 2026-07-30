# OpenPrintBench

OpenPrintBench is an independent, local-first toolkit for reproducible slicer
regression plans and physical-print evidence. It is designed to work with
desktop slicers already installed by the user, beginning with Bambu Studio and
later OrcaSlicer.

The current pre-alpha milestone can:

- discover a local Bambu Studio or OrcaSlicer executable;
- report the detected slicer version without using a cloud account;
- fingerprint an STL or 3MF input;
- produce an inspectable, shell-free Bambu Studio slicing command;
- emit a JSON plan that can become part of a reproducible regression report;
- execute one explicitly approved slice in a new isolated directory;
- record a portable run manifest, output hashes, and a redacted slicer log.

OpenPrintBench does not upload models, control printers, use Bambu Cloud,
request access tokens, or load proprietary network plugins.

> [!IMPORTANT]
> OpenPrintBench is not affiliated with, endorsed by, or sponsored by Bambu Lab
> or the OrcaSlicer project. Product names are used only to describe
> interoperability with user-installed software.

## Status

Pre-alpha. A run requires an explicit `--approve` flag and a fixture with pinned
source and license provenance. The project does not claim physical-print
validation. See
[the roadmap](docs/ROADMAP.md), [daily progress log](docs/PROGRESS.md), and
[evidence-gated promotion plan](docs/PROMOTION.md).

## Quick start

Requirements:

- Python 3.11 or newer
- `uv`
- Bambu Studio for the current real-machine probe

```bash
uv sync
uv run openprintbench doctor
uv run openprintbench doctor --json
```

Create a plan for a 3MF that already contains its printer, process, and
filament settings:

```bash
uv run openprintbench plan \
  --slicer bambu \
  --input path/to/project.3mf \
  --output-dir runs/example \
  --output-name sliced.3mf
```

For a bare STL, provide full machine, process, and filament settings:

```bash
uv run openprintbench plan \
  --slicer bambu \
  --input path/to/model.stl \
  --output-dir runs/example \
  --machine-settings path/to/machine.json \
  --process-settings path/to/process.json \
  --filament-settings path/to/filament.json
```

The generated command is an argument array. OpenPrintBench does not construct
or execute a shell string.

Execute an isolated run only after reviewing the plan and fixture provenance:

```bash
uv run openprintbench run \
  --input fixtures/cube-20mm.stl \
  --run-dir /tmp/openprintbench-run-001 \
  --machine-settings path/to/machine.json \
  --process-settings path/to/process.json \
  --filament-settings path/to/filament.json \
  --profile-root path/to/installed/profiles/BBL \
  --profile-source-url \
    https://github.com/bambulab/BambuStudio/tree/FULL_COMMIT/resources/profiles/BBL \
  --profile-source-commit FULL_COMMIT \
  --profile-license AGPL-3.0-only \
  --fixture-source-url \
    https://github.com/kforris/OpenPrintBench/blob/FULL_COMMIT/fixtures/cube-20mm.stl \
  --fixture-source-commit FULL_COMMIT \
  --fixture-license CC0-1.0 \
  --approve
```

The run directory must not already exist. OpenPrintBench gives the slicer a
private `HOME` and temporary directory, removes secret-like environment
variables, captures stdout/stderr into a redacted log, and fingerprints regular
files under the isolated output directory. For STL inputs, it resolves the
installed Bambu profile inheritance into complete private run-local JSON files
and records both source and materialized hashes. Generated 3MF/G-code remains
local and must not be committed.

See the first
[repeatability evidence](docs/evidence/2026-07-28-bambu-stl-repeatability.md)
for two runs using the project-authored CC0 cube fixture.

## Development

```bash
uv sync
uv run ruff check .
uv run ruff format --check .
uv run mypy src
uv run pytest -q --cov=openprintbench --cov-report=term-missing
uv build
```

## Project principles

- Local files stay local by default.
- Every result must identify its input, slicer version, and configuration.
- Planned, executed, and physically validated states are never conflated.
- Claims require machine-readable evidence plus a human-readable explanation.
- Upstream names, trademarks, and licenses remain clearly attributed.

## License

OpenPrintBench is available under the [MIT License](LICENSE). Interoperated
slicers retain their own licenses and are not redistributed by this project.
