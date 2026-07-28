# P0 building-in-public draft

Status: publication authorized, but blocked until the first functional PR
linked to Issue #1 is merged and `main` CI is green. Refresh all counts and
claims immediately before publishing.

## Post 1

Building OpenPrintBench: reproducible, local-first slicer regression tests for
Bambu Studio; OrcaSlicer is planned.

Pre-alpha: CLI detection, hashed STL/3MF inputs, shell-free plans, 32 tests,
87.7% branch coverage.

Feedback:
https://github.com/kforris/OpenPrintBench

## Post 2

Not claiming executed slicing or physical validation yet. Next: an isolated
Bambu Studio run with version, input/output hashes, timing, exit status, and a
redacted log.

Looking for openly licensed STL/3MF fixtures:
https://github.com/kforris/OpenPrintBench/issues/1

## Visual brief

- Format: 1600 x 900, readable in X's 16:9 preview.
- Content: a labelled pre-alpha flow from local model hash, to shell-free slice
  plan, to the next isolated execution/evidence step.
- Evidence: use only repository capabilities and current public test/coverage
  results verified after the first functional PR.
- Style: dark technical canvas, geometric pipeline, restrained accent colour,
  no Bambu Lab or OrcaSlicer logos, no invented UI or physical-print image.
- Required label: `PRE-ALPHA — executed slicing and physical validation are
  separate evidence gates`.
- Alt text: write after the final image is visually checked; it must name the
  three stages and identify which stage is not yet complete.
