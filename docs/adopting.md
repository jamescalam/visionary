# Adopting visionary

## Prerequisites

- The Claude GitHub App installed on the repo (or org). When the workflows omit `github_token`, the action authenticates as this app, and its commits trigger other workflows.
- A `CLAUDE_CODE_OAUTH_TOKEN` secret, from `claude setup-token`. An org-level secret scoped to the repos that adopt visionary is the easiest to rotate. The token is tied to the subscription of whoever generated it; a dedicated bot account keeps pipeline usage separate from a person's.
- `main` protected: pull request required, one human approval. Agents cannot approve.

## Files in the adopting repo

| Path | Purpose |
|---|---|
| `VISION.md` | The owner's steering document. Read by every role. A push to `main` that changes it re-runs the planner. |
| `AGENTS.md` | How the code is organised, tested, and what to watch for. |
| `.visionary.yml` | Check commands, bench contract, labels, caps. |
| `.github/workflows/visionary-*.yml` | Callers: triggers plus `uses:` lines. |
| `benchmarks/`, `reports/` | Only if the repo runs experiments. |

## Secrets and names

| Secret | Purpose | Needed by |
|---|---|---|
| `CLAUDE_CODE_OAUTH_TOKEN` | Claude Code in CI | all roles |
| `OPENAI_API_KEY` (in a `live` environment) | paid encoders | experiment |
| `VISIONARY_SLACK_BOT_TOKEN` | thread per PR or experiment | planned |
| `VISIONARY_LINEAR_API_KEY` | mirror proposals to Linear | planned |

Callers map secrets explicitly (`secrets: {claude_code_oauth_token: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}}`) rather than `secrets: inherit`, so visionary's workflow code never sees secrets it does not need.

## Permissions

A called workflow cannot hold more permissions than its caller, and `id-token: write` (needed for the Claude GitHub App token exchange) is never granted by default. Every caller template therefore carries an explicit `permissions` block. Removing it makes the run fail at startup with no job output.

## Pinning

Callers reference `jamescalam/visionary/.github/workflows/<name>.yml@<ref>`. The reusable workflow checks out the same ref of visionary into `.visionary/` and loads the plugin from there, so workflows, actions, and prompts always match. Use `@main` while things move quickly; pin to a tag once you want stability.

## Labels

The plan workflow creates these on first run: `visionary`, `proposal`, `approved`, `in-progress`, `reconsider`, `experiment`, `experiment-report`, `agent-fix-ok`. Only `approved` and `agent-fix-ok` are meant to be added by a person.

## Who reviews

List the people who should be asked to review agent-authored PRs under `reviewers` in `.visionary.yml`. The implementer and experimenter request them on every PR they open. Agents cannot approve, so branch protection plus a requested human reviewer is the merge gate.

The GitHub identity the agents act as is the Claude GitHub App (`claude[bot]`), which is separate from the Claude subscription that pays for the runs. To move the spend onto a bot account, generate `CLAUDE_CODE_OAUTH_TOKEN` from that account's own Claude subscription; the GitHub identity is unaffected.

## Talking to the agents

The responder runs on every human comment on a PR or issue an agent opened, and on any comment mentioning `//vision` elsewhere. Reviews with inline comments arrive as one `pull_request_review` event, so leave a review and submit it; each inline thread you left is read. On a proposal issue, a comment can ask the responder to revise the proposal body; it never adds `approved`. The phrase is `//vision`, deliberately not an @-mention: GitHub links every `@name` in a comment to a real user, so an invented handle would notify a stranger, and `@claude` collides with the Claude GitHub App's own mention handling. Change it in the caller's `if:` if you want another.

## Fix mode

The reviewer pushes commits only when the PR author is `claude[bot]` or the PR carries `agent-fix-ok`. Otherwise it has no edit tools. Add the label to a human PR when you want the reviewer to fix what it finds.
