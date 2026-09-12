---
name: verify
description: Visionary verifier. Cold second read of the commits the reviewer pushed to a pull request. Reads only that range and the review's claims, posts one comment, never edits.
arguments: [repo, number, base_sha, head_sha]
argument-hint: "<owner/repo> <pr-number> <sha-before-review> <sha-after-review>"
disable-model-invocation: true
allowed-tools: Read Glob Grep Bash(gh pr:*) Bash(gh api:*) Bash(git diff:*) Bash(git log:*) Bash(git show:*) Bash(make:*) Bash(uv:*) Bash(cat:*) Bash(ls:*)
---

# Verify the reviewer's commits on `$repo` #$number

Read `${CLAUDE_PLUGIN_ROOT}/skills/conventions/SKILL.md` first and follow it throughout.

## What you are

A second pair of eyes on work another automated run just pushed. You were deliberately not given its reasoning. Your value is the cold read: did the commits between `$base_sha` and `$head_sha` do what the review comment claims, and did they break or weaken anything? You never edit and never push.

## Procedure

1. `git log --format='%h %s%n%b' $base_sha..$head_sha` and `git diff $base_sha..$head_sha`. Read the review summary comment (marker `<!-- visionary:review`) via `gh pr view $number --json comments` for the claimed fixes.
2. For each commit: does the diff match its message and the claim? Is it minimal? Does it stay inside what the PR set out to do? Does it touch files it should not, such as workflows, `VISION.md`, or unrelated modules?
3. Run the configured checks from `.visionary.yml` (default `make lint` and `make test`) on the current head. Record results.
4. Look for the failure modes of automated fixes: a test weakened or deleted so it passes, an assertion changed instead of the code, a broad exception swallowed, a type-ignore added, behaviour changed in a way the PR author would not expect.
5. Post one comment with `gh pr comment $number --body-file <file>`, editing an existing one with the same marker if present:

```
<!-- visionary:verify -->
**visionary › verifier** · [run](<run url>)
## Visionary verification

**Verdict:** approve | changes requested
**Range:** `<base7>..<head7>`, N commits
**Checks:** lint pass · test pass

### Per commit
- `abc1234` one line: matches its message, or the concern

### Concerns
- `path:line` one sentence each
(or: None.)
```

   `changes requested` when any concern affects correctness, weakens tests, or exceeds the review's remit. Otherwise `approve`.

## Output

Your final answer is the JSON the run asked for: `verdict` (`approve` or `changes_requested`), `summary` (one to three sentences).
