# Bounded v0.1 goal

```text
/goal Build and publish OpenPrintBench v0.1.0 as a local-first, reproducible
Bambu Studio slicing runner with truthful evidence states.

First action: read README.md, AGENTS.md, docs/ARCHITECTURE.md,
docs/ROADMAP.md, and docs/PROGRESS.md. Report the count of unchecked v0.1
roadmap items and AGENTS.md Iron Rules before implementation.

Scope: src/openprintbench/, tests/, docs/, packaging metadata, and GitHub CI for
the v0.1 execution path. Physical-print observations may add evidence files but
must not add printer-control features.

Constraints:
  - Never add cloud login, tokens, printer control, telemetry, or model upload.
  - Invoke user-installed slicers only as separate processes with shell=False.
  - Never conflate planned, executed, and physically validated states.
  - Do not commit proprietary models/profiles, generated G-code, credentials,
    serials, local usernames, or absolute home-directory paths.
  - Add no runtime dependency unless the standard library cannot satisfy a
    documented v0.1 requirement.
  - Existing tests failing is a regression; do not edit tests, add skip/xfail,
    or lower coverage to hide it.

Done when:
  1. docs/ROADMAP.md has every v0.1 item checked with an evidence link.
  2. `uv run ruff check .` and `uv run ruff format --check .` exit 0.
  3. `uv run mypy src` exits 0 with no errors.
  4. `uv run pytest -q --cov=openprintbench --cov-report=term-missing` exits 0,
     has zero skipped/xfail tests, and reports at least 85% branch coverage.
  5. `uv build` exits 0 and both sdist and wheel install in a clean temporary
     environment.
  6. One redistributable fixture is sliced by local Bambu Studio in an isolated
     run directory; the manifest records version, input hash, duration, exit
     status, output hashes, and a redacted log.
  7. A second run of the same fixture and settings is compared, with
     deterministic and non-deterministic fields explicitly classified.
  8. GitHub CI passes on the public v0.1 tag and the release notes link the
     evidence without claiming physical validation.

Stop if:
  - The slicer requests cloud credentials, printer access, or the optional
    networking plugin.
  - The only available fixture or profile lacks redistribution permission.
  - The implementation would require shell=True or evaluating a command string.
  - A test exposes credentials, device serials, local usernames, or absolute
    home-directory paths.
  - Existing tests fail; do not repair that by weakening or skipping tests.
  - Physical validation cannot be completed because the printer model,
    material, or human observation is unavailable; finish digital evidence and
    report the physical gate separately.

Use a token budget of 120000 tokens for this goal.
```

Audit-friendliness: excellent — eight mechanical acceptance checks, six
detectable stop conditions, and a finite release boundary.
