# Social feedback loop

This procedure turns public feedback into maintainable project work without
manufacturing activity. GitHub is the durable source of truth; X is a discovery
and conversation channel.

## Before daily development

1. Read the current roadmap, open GitHub issues and PRs, recent CI, and
   OpenPrintBench-related X notifications, mentions, and replies.
2. Ignore unrelated timeline content. Do not inspect private messages.
3. Classify each relevant item:
   - reproducible bug or missing evidence;
   - bounded feature request;
   - documentation or support question;
   - duplicate or already resolved;
   - spam, abuse, private-data risk, or out of scope.
4. Link actionable X feedback to an existing GitHub issue. Create a new issue
   only when the report is reproducible or a bounded clarification can make it
   reproducible. Link the public post, summarize only the necessary technical
   facts, and do not copy personal data.
5. Select work by roadmap priority, user impact, reproducibility, and safety.
   Stars, follower count, or a loud reply do not override the project gates.

## During development

- Keep one atomic code/behaviour topic per PR and link its issue.
- State acceptance criteria before implementation.
- Preserve the plan, executed-slice, and physical-validation evidence states.
- If feedback requires credentials, proprietary files, printer control, private
  messages, or a security disclosure, stop public handling and request
  maintainer review.

## After development

1. Verify the change locally and in public CI according to `AGENTS.md`.
2. Update the GitHub issue with the PR, commit, test result, and evidence
   artifact or release.
3. Reply to the relevant public X conversation with a concise status and a
   durable GitHub link. Do not claim a fix before merge and green CI.
4. Close a GitHub issue only when:
   - its documented acceptance criteria are met;
   - the fix or documentation is merged;
   - required CI is green;
   - the closing comment links the evidence; and
   - any required reporter reproduction or human hardware check is complete.
5. Record material feedback, actions, public URLs, and unresolved blockers in
   the day's `docs/PROGRESS.md` entry. If nothing relevant changed, record no
   material feedback rather than inventing engagement.

## Publishing and reply boundaries

Routine OpenPrintBench milestone posts and public technical replies may be
published through the authenticated maintainer X account under the standing
authorization recorded on 2026-07-28. Before every write, verify the account,
exact text, links, image, alt text, and evidence gate; after the write, reopen
the public URL and verify the rendered result.

Do not automate likes, follows, reposts, quote-posts, private messages, generic
engagement bait, or unsolicited replies to unrelated conversations. Require
separate maintainer review for security, licensing, affiliation, legal,
financial, controversial, or private-data topics.
