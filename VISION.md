# Vision

The steering document for visionary itself. Every role reads it when reviewing or planning changes to this repo.

## What this project is

visionary is a small framework that runs a loop of Claude Code agents over a codebase inside a vision its owner writes down. It is a Claude Code plugin plus reusable GitHub Actions workflows. It is not an orchestrator service, not a hosted product, and not a general agent framework. GitHub events are the orchestrator; GitHub objects are the state.

## What good looks like

- An adopting repo needs three files and a few caller workflows, and nothing else. Every new capability is judged by whether it adds to that list.
- Every guardrail that matters is enforced outside the model: tool allowlists, turn caps, concurrency, the bot allowlist, branch protection. Prompts describe good behaviour; workflows make bad behaviour impossible or cheap.
- Roles are cold. A role gets only the inputs its skill names. No role reads another role's transcript.
- The framework is its own first adopter. A change to a skill or workflow is reviewed by the version of visionary under review.
- Prompts are short, specific, and written for the model that runs them. If a rule can be enforced in a workflow instead, it moves there.

## Priorities when they conflict

1. Safety of the adopting repo: nothing agent-authored reaches a default branch without a cold read and a human merge.
2. Signal per human minute: fewer, better proposals and reviews beat more of them.
3. Portability across repos and languages.
4. Cost per run.

## Current direction (September 2026)

- Bed in the review, verify, plan, implement, and experiment roles on aurelio-labs/semantic-chunkers, then semantic-router.
- Mirror proposals and tranches to Linear, and post each run's summary to a Slack thread per PR or experiment, as deterministic workflow steps rather than agent tools.
- Pin adopters to a `v1` tag once the results contract and `.visionary.yml` stop changing.

## Non-goals

- Running outside GitHub Actions. The Agent SDK path is a fallback for experiments that outgrow a runner, not a second product.
- Agents approving, merging, or closing pull requests.
- Holding secrets on behalf of adopters.

## Rules for agents

- Do not change a skill's tool pre-approvals, a workflow's permissions, or a deny list without saying so in the PR body under its own heading.
- Any change to the results contract or to `.visionary.yml` keys is breaking and needs a changelog entry and a version bump in the plugin manifest.
- Templates must stay copy-and-run: every template is valid on its own with no edits other than the `setup` block.
