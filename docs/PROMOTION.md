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
- Do not automate likes, follows, reposts, quote-posts, private messages, or
  repetitive cross-posting.
- The maintainer authorized routine OpenPrintBench milestone posts and
  project-relevant technical replies through the authenticated maintainer X
  account on 2026-07-28. No per-post confirmation is required while that
  authorization remains in force, provided the evidence gate, weekly limit, and
  safety rules in this document are satisfied.
- Before each public write, save the exact copy and verify the destination.
  Afterward, record the public URL and verify the rendered text, image, link,
  and absence of private information.
- Separate approval is still required for security disclosures, licensing or
  affiliation claims, legal or financial topics, controversial commentary,
  private information, direct messages, or a material change of project scope.

## Visual rules

- Prefer one useful visual for each milestone post: an evidence-flow diagram,
  a real terminal/result capture with private data redacted, or a clearly
  labelled illustration.
- Generated images may support a post, but must not invent dashboards, terminal
  output, user counts, benchmarks, physical prints, or product affiliation.
- Create the final visual only after the milestone evidence is current. Store
  its source or generation brief, final asset, and alt text under
  `docs/promotion/`.
- Verify the image at its final crop and resolution before publishing. Text in
  the post must remain understandable without the image.

## Milestone triggers

### P0 — public development baseline

Gate:

- public repository;
- green CI on Python 3.11, 3.12, and 3.13;
- honest pre-alpha README;
- one public v0.1 issue;
- the first non-documentation functional PR, linked to Issue #1, is merged and
  its `main` CI is green.

Content:

- one two-post “building in public” thread;
- include one verified visual and alt text;
- ask for openly licensed STL/3MF fixtures, macOS reproduction help, and
  specific technical feedback;
- explicitly state that slice execution and physical validation are not yet
  complete unless the merged PR and public evidence prove otherwise.

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
- Ask narrow questions that a reader can answer, such as whether a fixture
  license is redistributable, whether a run reproduces on a named macOS/slicer
  version, or which manifest field is missing. Do not ask for stars as a
  condition of help.

## Daily feedback loop

Run the process in [SOCIAL_FEEDBACK_LOOP.md](SOCIAL_FEEDBACK_LOOP.md) before
selecting the day's work and again after publishing a code or documentation
change. GitHub remains the durable tracker; relevant public X feedback should
link to an existing issue or be converted into one when it is reproducible and
actionable.

An issue may be closed only after its documented acceptance criteria are met,
the change is merged, required CI is green, and a closing comment links the
evidence. A public X reply may then point to the issue, PR, commit, evidence
artifact, or release. A reply alone is not evidence that a bug is fixed.

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
