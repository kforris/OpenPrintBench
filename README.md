# OpenPrintBench

OpenPrintBench is an independent, local-first toolkit for reproducible slicer
regression plans and physical-print evidence. It is designed to work with
desktop slicers already installed by the user, beginning with Bambu Studio and
later OrcaSlicer.

The first development milestone can:

- discover a local Bambu Studio or OrcaSlicer executable;
- report the detected slicer version without using a cloud account;
- fingerprint an STL or 3MF input;
- produce an inspectable, shell-free Bambu Studio slicing command;
- emit a JSON plan that can become part of a reproducible regression report.

OpenPrintBench does not upload models, control printers, use Bambu Cloud,
request access tokens, or load proprietary network plugins.

> [!IMPORTANT]
> OpenPrintBench is not affiliated with, endorsed by, or sponsored by Bambu Lab
> or the OrcaSlicer project. Product names are used only to describe
> interoperability with user-installed software.

## Status

Pre-alpha. The current code creates and validates slicing plans; it does not
yet execute a slice or claim physical-print validation. See
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
