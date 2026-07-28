# Daily progress

This append-only log records material work, verification, blockers, and the
next highest-priority action. A day with no material change should say so
instead of manufacturing activity.

## 2026-07-27

### Completed

- Confirmed the project as the primary 30-day OSS-readiness candidate under
  the P3rkLab digital-manufacturing direction.
- Chose an independent repository boundary instead of modifying the existing
  non-Git P3rkLab frontend directory.
- Verified local Python 3.11, `uv`, Bambu Studio
  `02.06.00.51`, and the official Bambu Studio command-line interface.
- Created the package, Bambu/Orca discovery, Bambu slice planner, tests,
  governance documents, and a bounded v0.1 goal.
- Added a three-version macOS CI matrix with action revisions pinned to commit
  SHAs, plus structured issue and pull-request templates.

### Evidence

- Local slicer executable:
  `/Applications/BambuStudio.app/Contents/MacOS/BambuStudio`
- `BambuStudio --help` exited `0` and reported version `02.06.00.51`.
- Ruff lint and formatting: passed.
- Mypy strict type-check: passed.
- Pytest: 32 passed, 0 skipped/xfail.
- Branch coverage: 87.61%, above the 85% gate.
- Source distribution and wheel build: passed.
- Public repository: <https://github.com/kforris/OpenPrintBench>
- Baseline commit: `8f63b9c50600442d758fc9ce6cca047600bb11e1`
- Three-version CI:
  <https://github.com/kforris/OpenPrintBench/actions/runs/30327749606>
- First v0.1 issue:
  <https://github.com/kforris/OpenPrintBench/issues/1>

### Blockers

- The target Bambu printer model is not yet recorded.
- OrcaSlicer is not currently installed locally.
- No redistributable STL/3MF fixture has been selected yet.

### Next

1. Complete local lint, type-check, tests, coverage, and build.
2. Publish the reviewed initial repository and enable CI.
3. Select the first open fixture and execute an isolated Bambu Studio slice.

## 2026-07-28

### Completed

- Added an evidence-gated promotion plan covering the public baseline, first
  reproducible slice, v0.1 release, and first independent use.
- Prepared a two-post P0 building-in-public draft without publishing it.
- Limited X/Twitter cadence to two original milestone posts or threads per
  week, with exact-text account-owner confirmation required before publishing.

### Evidence

- Promotion plan: `docs/PROMOTION.md`
- P0 draft: `docs/promotion/P0_BUILDING_IN_PUBLIC.md`
- Public baseline CI remains green:
  <https://github.com/kforris/OpenPrintBench/actions/runs/30327838692>

### Blockers

- The X/Twitter destination account has not been identified or connected.
- The account owner has not approved the P0 draft for publication.
- The target Bambu printer model is not yet recorded.

### Next

1. Confirm the X/Twitter account and review the P0 draft.
2. Select the first open fixture and execute an isolated Bambu Studio slice.
3. Measure public repository signals 24 and 72 hours after the first post.
