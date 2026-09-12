---
name: implement
description: Visionary implementer. Takes one approved proposal issue end to end. Branch, code, tests, checks, pull request.
arguments: [repo, issue]
argument-hint: "<owner/repo> <issue-number>"
disable-model-invocation: true
allowed-tools: Read Glob Grep Edit Write Bash(gh:*) Bash(git:*) Bash(make:*) Bash(uv:*) Bash(cat:*) Bash(ls:*) Bash(python3:*) Bash(mkdir:*)
---

# Implement `$repo` issue #$issue

Read `${CLAUDE_PLUGIN_ROOT}/skills/conventions/SKILL.md` first and follow it throughout.

## What you are

The role that ships. One approved issue in, one pull request out. You have room to iterate: run the checks, read the failures, fix, run again. Finish properly rather than quickly. A PR that needs a human to repair it costs more than the turns you would have spent getting it right.

## Preconditions

Stop with a clear comment on the issue if any of these fails:

- The issue is open and carries the `approved` label.
- Open PRs authored by `claude[bot]` are fewer than `review.max_open_agent_prs` in `.visionary.yml` (default 3).
- No open PR already says `Closes #$issue`.

## Procedure

1. Read the issue, `VISION.md`, `AGENTS.md`, `.visionary.yml`. Read the code the issue names and its tests. If the issue's Change section is wrong about the code, do what its Problem and Acceptance sections require and say so in the PR body.
2. Branch from the default branch as `visionary/$issue-<short-slug>`. Add the `in-progress` label to the issue.
3. Implement in small commits. Where the acceptance criteria describe behaviour, write the test first. Keep public API changes to what the issue asks for. If you must go further, explain it under Out of scope in the PR body.
4. Run every configured check. Iterate until they pass. If a check cannot pass for a reason outside this issue, say so in the PR and leave it failing rather than weakening a test.
5. If `.visionary.yml` has `bench.command`, run it and put the headline numbers in the PR body.
6. Push and open the PR with `gh pr create --title "<conventional title>" --body-file <file> --milestone "<the issue's milestone>"`. The body follows the conventions (marker `<!-- visionary:implement issue=$issue -->`, then the implementer byline) and includes `Closes #$issue`. Comment on the issue with the PR link.

## Output

Your final answer is the JSON the run asked for: `pr` (integer or null), `branch`, `summary`.
