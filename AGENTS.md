# OpenPrintBench agent instructions

## Scope

Build a local-first, reproducible slicer regression and physical-print evidence
tool. The project invokes user-installed slicer executables as separate
processes and does not redistribute them.

## Iron rules

- Never add cloud login, printer-control, token handling, telemetry, or model
  upload features.
- Never invoke slicers through `shell=True` or construct a command string for
  shell evaluation.
- Never report a plan as an executed slice or an executed slice as a physical
  print.
- Never commit user models, proprietary profiles, generated G-code, local
  usernames, absolute home-directory paths, credentials, or device serials.
- Do not weaken tests, add skip/xfail markers, or lower coverage to pass CI.
- Keep Bambu Studio and OrcaSlicer integrations optional; tests must use fakes
  or temporary files unless explicitly marked as local integration checks.
- Public claims require a reproducible command, version, hash, and evidence
  artifact.

## Required validation

Before committing code changes:

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy src
uv run pytest -q --cov=openprintbench --cov-report=term-missing
uv build
git diff --check
```
