# visionary

An event-driven loop of Claude Code agents that maintains and researches a codebase inside a vision its owner writes down. Five roles, each a fresh Claude Code run triggered by a GitHub event, handing off through GitHub objects. Humans decide at exactly three points: which proposals are approved, what gets merged, and who holds the live keys.

visionary is packaged as a Claude Code plugin plus reusable GitHub Actions workflows. A project adopts it by adding a `VISION.md`, an `AGENTS.md`, a small config file, and a few caller workflows that are little more than `uses:` lines.

## The loop

| Role | Trigger | Reads | Writes | Hands off to |
|---|---|---|---|---|
| **review** | every pull request | diff, `AGENTS.md`, `VISION.md`, check results | inline comments, one summary comment; fix commits when allowed | verify, if it pushed |
| **verify** | the reviewer pushed | only the pushed commits and the review's claims | one comment | one more review round, if it requests changes |
| **experiment** | nightly cron | `VISION.md`, past reports, the benchmark | a report PR under `reports/` | the next plan |
| **plan** | a tranche closes, or `VISION.md` changes | the whole repo state, including open PRs | a tranche milestone and proposal issues | you, to approve |
| **implement** | you label a proposal `approved` | the issue, the code | a pull request | review |
| **respond** | a human comments on anything an agent opened, or mentions `@vision` anywhere | the comment, unresolved threads, the code | changes on the PR branch, a revised proposal, an answer, or a reaction | verify, if it pushed |

An implementer's PR goes through the same review path as a human PR. Nothing agent-authored reaches `main` without a cold read and a human merge.

**Talking to it.** Comment on any PR or issue an agent opened and the responder reads it and acts, which may mean doing nothing and leaving a thumbs-up. Anywhere else, mention `@vision`. Every comment an agent posts starts with a byline naming the role and linking its run, and its commits are authored as `visionary-<role>`, because all roles share the one Claude GitHub App identity.

**Tranches.** Each planner run creates a milestone `tranche-N` that every proposal and implementer PR carries. When the milestone has no open PRs and no open issues, it closes and the planner runs again with the full repo state. A push to `main` that touches `VISION.md` also re-runs the planner, which will flag in-flight PRs that no longer fit with a `reconsider` label rather than closing them. Human PRs outside the milestone never hold a tranche open.

## Adopt it

1. Install the [Claude GitHub App](https://github.com/apps/claude) on the org or repo, and add a `CLAUDE_CODE_OAUTH_TOKEN` secret from `claude setup-token` (or run `/install-github-app` from Claude Code, which does both).
2. Copy `templates/VISION.md`, `templates/AGENTS.md`, and `templates/.visionary.yml` to the repo root and fill them in. The vision is the steering control; spend time on it.
3. Copy the caller workflows you want from `templates/` into `.github/workflows/`. Start with `visionary-review.yml` and `visionary-respond.yml`. Adjust the `setup` block to your toolchain.
4. Protect `main`: require a pull request and one human approval. Agents cannot approve, so this is the merge gate.
5. Open a PR. The reviewer runs on it.

Add `visionary-plan.yml`, `visionary-tranche.yml`, and `visionary-implement.yml` when you want proposals. Add `visionary-bench.yml` and `visionary-research.yml` once the repo has a benchmark that follows the [results contract](plugin/skills/experiment/results-schema.md).

Run any role locally: `claude --plugin-dir ./plugin` in the adopting repo, then `/visionary:review owner/repo 123 comment`.

## Layout

```
.claude-plugin/marketplace.json   one-entry marketplace
plugin/                           the Claude Code plugin
  skills/conventions              rules every role follows
  skills/review, verify, plan, implement, experiment
actions/run-agent                 run one role with a turn cap and structured output
actions/tranche-check             is the tranche done; close it
actions/bench-delta               bench head vs base, comment the table
.github/workflows/*.yml           reusable workflows (workflow_call)
scripts/                          deterministic helpers the actions call
templates/                        what an adopting repo copies
docs/                             design notes
```

## Guardrails

- The Claude GitHub App is the bot identity. Its pushes trigger CI, unlike the default workflow token, and it appears as `claude[bot]`.
- Bot-authored events are ignored by default; `claude[bot]` is allowlisted only so implementer PRs get reviewed. Actor filters and per-PR concurrency groups stop loops.
- Every run has a turn cap and a tool allowlist enforced by the action, not by the prompt. Comment-mode reviews have no edit tools at all.
- Fork PRs get no secrets, so the reviewer runs only on same-repo branches.
- Secrets live in the adopting repo. visionary holds none.

## Status

Early. The review loop is in use; plan, implement, tranche, and experiment are wired and being exercised on [aurelio-labs/semantic-chunkers](https://github.com/aurelio-labs/semantic-chunkers). Slack mirroring and Linear sync are next.

MIT.
