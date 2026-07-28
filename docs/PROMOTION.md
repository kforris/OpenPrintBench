# Promotion plan

Promotion exists to find real users, fixtures, and maintainers—not to
manufacture activity. Stars are a useful discovery signal, but they are not a
substitute for releases, issue triage, reproducible evidence, or actual use.

## Publication rules

- Every claim must link to a public commit, CI run, issue, release, or evidence
  artifact.
- Always label pre-alpha work, planned slices, executed slices, and physical
  validation accurately.
- Never publish credentials, device serials, private models or profiles, local
  usernames, absolute home paths, or private analytics.
- Do not imply affiliation with Bambu Lab or OrcaSlicer.
- Do not automate likes, follows, replies, quote-posts, or repetitive
  cross-posting.
- Drafts may be prepared automatically. Publishing to a social account requires
  the account owner's confirmation of the exact text and destination.

## Milestone triggers

### P0 — public development baseline

Gate:

- public repository;
- green CI on Python 3.11, 3.12, and 3.13;
- honest pre-alpha README;
- one public v0.1 issue.

Content:

- one two-post “building in public” thread;
- ask for openly licensed STL/3MF fixtures and technical feedback;
- explicitly state that slice execution and physical validation are not yet
  complete.

### P1 — first reproducible slice

Gate:

- a redistributable fixture with pinned provenance;
- two isolated runs using the same inputs and settings;
- slicer version, input/output hashes, duration, exit status, and redacted logs;
- green CI for the execution path.

Content:

- one technical result post with the evidence artifact;
- explain deterministic and non-deterministic fields;
- invite reproduction on another macOS machine.

### P2 — v0.1.0 release

Gate:

- every v0.1 roadmap item that does not require unavailable human hardware
  evidence is complete;
- release tag and distributions are public;
- installation and first-run instructions have been tested from a clean
  environment;
- the remaining physical validation gate is stated plainly if incomplete.

Content:

- one launch thread with problem, evidence, supported workflow, limitations,
  and repository link;
- one concise visual showing the plan/run/evidence flow;
- pin the launch post temporarily.

### P3 — independent use

Gate:

- an external user provides a reproducible issue, fixture result, or public
  feedback;
- the maintainer responds with triage or a documented change.

Content:

- thank the contributor with permission;
- describe what changed without exposing private data;
- link the issue, fix, and release.

## Cadence and channels

- X/Twitter: at most two original milestone posts or threads per week.
- GitHub: releases, issues, discussions, and README remain the source of truth.
- Reddit, Discord, forums, or slicer communities: only after reading each
  community's current self-promotion rules; never paste the same message
  everywhere.
- Replies should answer real technical questions. Do not post generic
  engagement bait.

## Measurement

Review public signals 24 and 72 hours after each post:

- impressions and engagements when visible to the account owner;
- repository visits when available;
- stars, forks, watchers, issues, and unique external contributors;
- fixture submissions or completed reproductions.

Internal first-month target:

- 10 authentic stars;
- one external tester or reproducible feedback item;
- one maintainer response that results in triage, documentation, or code.

These are internal planning targets, not OpenAI program requirements and not a
guarantee of acceptance.
