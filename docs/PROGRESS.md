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
- Prepared a two-post P0 building-in-public draft without publishing it before
  the first functional PR gate.
- Verified the logged-in X destination as `@kforris_w` and recorded the
  maintainer's standing authorization for routine OpenPrintBench posts and
  technical replies.
- Added a daily GitHub/X feedback loop with evidence-based response and issue
  closure rules.
- Kept X/Twitter cadence at no more than two original milestone posts or
  threads per week and excluded automated likes, follows, reposts, quote-posts,
  private messages, and generic engagement.
- Added the first redistributable fixture: a project-authored 20 mm ASCII STL
  cube released under CC0-1.0, with a sidecar license and pinned SHA-256.
- Implemented the explicitly approved Bambu Studio executor linked to Issue
  #1. It uses an argument array with `shell=False`, a new private run
  directory, isolated `HOME`/temporary paths, secret-like environment removal,
  a bounded timeout, redacted logging, and portable evidence manifests.
- Added a local profile materializer because Bambu Studio CLI requires complete
  machine/process/filament settings rather than installed leaf profiles.
  Source commit/license, leaf hashes, materializer version, and resulting
  profile hashes are recorded without redistributing the profiles.
- Completed two successful Bambu Studio `02.06.00.51` digital slices with the
  same fixture and settings. Both exited `0`; the G-code SHA-256 was identical.
  Start time, duration, log timestamps, timing fields in `result.json`, and the
  3MF container hash varied. No generated 3MF/G-code was committed and no
  physical-print claim was made.
- Audited GitHub and the authorized `@kforris_w` X account before development.
  Issue #1 was the only open repository item; there were no open PRs, relevant
  X mentions, or OpenPrintBench search results. No X reply or post was needed.

### Evidence

- Promotion plan: `docs/PROMOTION.md`
- Daily feedback loop: `docs/SOCIAL_FEEDBACK_LOOP.md`
- P0 draft: `docs/promotion/P0_BUILDING_IN_PUBLIC.md`
- X destination: <https://x.com/kforris_w>
- Public baseline CI remains green:
  <https://github.com/kforris/OpenPrintBench/actions/runs/30328367492>
- Fixture SHA-256:
  `369c23daac96f4cde40ec6a0e13afb9be5ec4cbbf974c071c60f1009824477c4`
- Bambu profile source:
  `b506005bc4ee62124e24bf00e0f58656db3646a6` (`AGPL-3.0-only`)
- Repeatability record:
  `docs/evidence/2026-07-28-bambu-stl-repeatability.md`
- Run 1: duration `0.650262` seconds, exit `0`, G-code SHA-256
  `f6c6365d65ecf1110f4aefd1097558378006ad4f1738648fba74c0bfa95205c5`.
- Run 2: duration `0.472667` seconds, exit `0`, G-code SHA-256
  `f6c6365d65ecf1110f4aefd1097558378006ad4f1738648fba74c0bfa95205c5`.
- Local validation after implementation: Ruff lint/format, mypy, 45 tests,
  0 skipped/xfail, 87.38% branch coverage, package build, and
  `git diff --check` passed.
- Functional PR: <https://github.com/kforris/OpenPrintBench/pull/2>
- PR CI (Python 3.11, 3.12, and 3.13):
  <https://github.com/kforris/OpenPrintBench/actions/runs/30368257211>
- No public release exists yet.

### Blockers

- The first functional PR is not merged and its `main` CI gate is not yet
  satisfied, so P0 publication remains blocked.
- Only one of the ten required redistributable fixtures is complete.
- The target Bambu printer model is not yet recorded.
- OrcaSlicer is not installed locally and no verified CI fixture is available.

### Next

1. Review the functional PR linked to Issue #1 and merge only after its CI is
   green; then verify the resulting `main` CI.
2. After that PR is merged and `main` CI is green, create and verify the P0
   visual, refresh the exact post copy, and publish through the authorized X
   account.
3. Add the next license-clear fixture or generator without weakening the
   provenance gate.
