# AGENTS.md

What an agent needs to work in this repository. The direction is in `VISION.md`; adoption steps are in `docs/adopting.md`.

## Overview

visionary is a Claude Code plugin (`plugin/`) plus reusable GitHub Actions workflows (`.github/workflows/*.yml` with `on: workflow_call`) and composite actions (`actions/`). Adopting repos copy the caller workflows from `templates/`, which point at the reusable workflows here; those check out this repo at a pinned ref into `.visionary/` and load the plugin from that path with `--plugin-dir`.

Roles are skills invoked as the run's prompt: `/visionary:review owner/repo 12 comment`. `plugin/skills/conventions/SKILL.md` holds the rules every role follows; each role skill reads it first.

## Commands

```bash
python3 scripts/validate_plugin.py      # manifests, skill frontmatter, token grep
python3 -m py_compile scripts/*.py      # script syntax
actionlint -ignore SC2016               # workflows, actions, templates
claude --plugin-dir ./plugin            # load the plugin locally, then /visionary:<role> ...
```

CI runs the first three. There is no test suite beyond that yet; the workflows are tested by running them on this repo's own PRs and on semantic-chunkers.

## Layout

```
.claude-plugin/marketplace.json   one-entry marketplace
plugin/.claude-plugin/plugin.json manifest; bump version on breaking changes
plugin/skills/<role>/SKILL.md     conventions, review, verify, plan, implement, experiment
plugin/skills/experiment/results-schema.md   the benchmark results contract
actions/run-agent                 runs one role: plugin path, turn cap, allowlist, JSON schema, push detection
actions/tranche-check             closes a tranche milestone when nothing in it is open
actions/bench-delta               bench head vs merge base, comment the table
.github/workflows/review.yml      reviewer -> verifier -> one more review round
.github/workflows/plan.yml, tranche.yml, implement.yml, experiment.yml, bench.yml
.github/workflows/ci.yml          validation for this repo
.github/workflows/visionary-review.yml   self review caller
scripts/                          deterministic helpers the actions call
templates/                        what adopters copy
docs/                             adopting.md, design.md
```

## Conventions

- Conventional commit messages; the trailer `Visionary-Role: <role>` on agent commits.
- Workflow inputs are strings with defaults; secrets are declared explicitly and mapped by callers, never `secrets: inherit`.
- Tool allowlists live in the workflows, not only in skill frontmatter, because the action starts MCP servers only for tools named in `--allowedTools`.
- Comment markers (`<!-- visionary:<role> ... -->`) identify every comment a role posts so reruns edit instead of duplicating.

## Gotchas

- The Claude action refuses to run a caller workflow whose content differs from the default branch. A PR that changes a `visionary-*.yml` caller cannot test itself; merge the caller change first.
- A called workflow cannot hold more permissions than its caller, and `id-token: write` is never default. Every caller template carries an explicit `permissions` block.
- The plugin path passed to Claude Code must be absolute. `run-agent` resolves it.
- Bot-authored events are rejected unless the bot is in `allowed_bots`; `claude[bot]` is allowlisted so implementer PRs get reviewed.
- `run-agent` allows the leading word of every command in `.visionary.yml` `checks` and `bench.command`; anything else an adopter's checks call must already be on the role's allowlist.
