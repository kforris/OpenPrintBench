## Problem

<!-- Link the issue and describe the single behavior being changed. -->

## Evidence state

- [ ] Probe
- [ ] Plan
- [ ] Run
- [ ] Physical validation

## Validation

- [ ] `uv run ruff check .`
- [ ] `uv run ruff format --check .`
- [ ] `uv run mypy src`
- [ ] `uv run pytest -q --cov=openprintbench --cov-report=term-missing`
- [ ] `uv build`
- [ ] `git diff --check`

## Privacy and provenance

- [ ] No credentials, serials, usernames, or absolute home paths are included.
- [ ] Every fixture and profile may be redistributed.
- [ ] No slicer binary or proprietary network plugin is redistributed.

