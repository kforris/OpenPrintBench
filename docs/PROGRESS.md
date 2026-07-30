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
4. Check GitHub issues/PRs and relevant X replies before selecting daily work;
   reply with evidence after changes and close only resolved GitHub issues.
5. Measure public repository and X signals 24 and 72 hours after the first
   post.

## 2026-07-29

### Completed

- Audited the public repository before selecting work. `main` remained at
  `26b1f280800a891d22345d2a05e9b37611b66c6a`; Issue #1 and PR #2 remained
  open.
- Confirmed PR #2 remained non-draft, mergeable, and clean at
  `817e8a7c8fb7c21264fead9229d277d3da55b6e2`, with no reviews or comments and
  green Python 3.11, 3.12, and 3.13 checks.
- Found no new external GitHub issue, pull request, review, or comment to
  classify or answer. No issue was closed and no GitHub reply was posted.
- Recorded no material implementation change rather than opening a second PR
  while the first functional PR is awaiting review and merge.
- Attempted the required read-only X mentions check in Comet, but the existing
  X session redirected to the login screen. No credentials were requested or
  entered, no private messages were inspected, and no X write was made.

### Evidence

- Public repository: <https://github.com/kforris/OpenPrintBench>
- Open Issue #1: <https://github.com/kforris/OpenPrintBench/issues/1>
- Open PR #2: <https://github.com/kforris/OpenPrintBench/pull/2>
- PR #2 CI: <https://github.com/kforris/OpenPrintBench/actions/runs/30368347793>
- Latest `main` CI:
  <https://github.com/kforris/OpenPrintBench/actions/runs/30328367492>
- Public repository snapshot: 1 star, 0 forks, no tags, and no releases.
- X feedback status: not observable because the authorized Comet session
  required re-authentication.

### Blockers

- PR #2 has not been reviewed or merged, so the required resulting green
  `main` CI does not exist and Issue #1 cannot be closed.
- The P0 visual and two-post thread remain blocked on the merged PR and green
  `main` CI gate.
- The Comet X session requires maintainer re-authentication before mentions,
  replies, publishing, or 24/72-hour metrics can be checked.
- The target Bambu printer model, material, and human observation are still
  unavailable; no physical validation is claimed.
- OrcaSlicer is not installed locally, and nine additional redistributable
  fixtures or generators remain to reach the v0.1 fixture target.

### Next

1. Monitor PR #2 for real review or merge activity; do not self-merge or create
   a second implementation PR while it remains open.
2. After PR #2 is merged, verify the resulting `main` CI, update and close
   Issue #1 with durable evidence, and mark only the proven roadmap items.
3. After the maintainer restores the authorized `@kforris_w` Comet session,
   repeat the read-only X mentions/replies audit.
4. When the P0 gate is satisfied, refresh the exact copy and metrics, create
   and inspect the evidence-backed 1600x900 visual, then publish and verify the
   authorized two-post thread.

## 2026-07-30

### Completed

- Refreshed the public repository before selecting work. `origin/main` was
  `2e61c5c29d7522d4aa4be8dcf6afdb563bde8121`; Issue #1 and PR #2 remained
  open, with no new review, review comment, issue comment, or external
  contribution.
- Found PR #2 had changed from mergeable/clean to conflicting/dirty after the
  2026-07-29 progress-only commit modified `docs/PROGRESS.md` on `main`.
- Selected one bounded unblocker instead of opening a second implementation
  PR: merged the latest `origin/main` into the existing PR branch and resolved
  the progress-log conflict without dropping either day's verified record.
- Verified the existing Comet X session was logged in as `@kforris_w`. The
  mentions view was empty and an exact latest search for `OpenPrintBench`
  returned no results after one retry. No private message was inspected and no
  X reply or post was made.

### Evidence

- Open Issue #1: <https://github.com/kforris/OpenPrintBench/issues/1>
- Open PR #2: <https://github.com/kforris/OpenPrintBench/pull/2>
- Pre-resolution PR state: `CONFLICTING` / `DIRTY` at
  `817e8a7c8fb7c21264fead9229d277d3da55b6e2`, with no reviews or comments.
- Previous PR CI:
  <https://github.com/kforris/OpenPrintBench/actions/runs/30368347793>
- Latest baseline `main` CI:
  <https://github.com/kforris/OpenPrintBench/actions/runs/30459104729>
- Local validation after conflict resolution: `uv lock --check`, Ruff
  lint/format, mypy, 45 tests with 0 skipped/xfail and 87.38% branch coverage,
  package build, and `git diff --check` passed.
- Public repository snapshot: 1 star, 0 forks, no tags, and no releases.

### Blockers

- PR #2 is still unmerged and requires review/merge; its resulting green
  `main` CI does not yet exist, so Issue #1 cannot be closed.
- The P0 visual and two-post thread remain blocked on the merged functional PR
  and resulting green `main` CI.
- The target Bambu printer model, material, and human observation remain
  unavailable; no physical validation is claimed.
- OrcaSlicer is not installed locally, and nine additional redistributable
  fixtures or generators remain to reach the v0.1 fixture target.

### Next

1. Verify the updated PR branch CI and mergeability, then wait for real review
   and merge without self-merging.
2. After PR #2 is merged, verify the resulting `main` CI, update and close
   Issue #1 with durable evidence, and mark only the proven roadmap items.
3. When the P0 gate is satisfied, refresh the exact copy and metrics, create
   and inspect the evidence-backed 1600x900 visual, then publish and verify the
   authorized two-post thread.
4. Add the next license-clear fixture or generator only after the current
   implementation PR is no longer blocking the one-topic workflow.
