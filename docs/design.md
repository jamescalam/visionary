# Design notes

## No orchestrator process

GitHub events and one cron are the orchestrator. Each role is a fresh, separately triggered Claude Code run whose last act is to produce a GitHub object that triggers the next role. No component knows the whole graph, which is what makes any stage easy to pause, replay, or override by hand.

## Skills as roles

Each role is a plugin skill invoked as the run's prompt (`/visionary:review ...`). Skills carry their own tool pre-approvals, and the run-agent action passes a matching `--allowedTools` list so the action starts the MCP servers those tools need. The conventions skill holds the rules every role shares; each role skill reads it first.

## Cold verification

The verifier gets only the commit range the reviewer pushed and the review's public claims. It never sees the reviewer's transcript. That is the point: its value is a second reading with no shared context. It runs at a higher effort than the reviewer because it reads less and judges more.

## Tranches

A tranche is a milestone. Completion is a property of GitHub state (no open PRs, no open issues in the milestone), checked on every PR close, so the planner runs when work actually finishes rather than on a schedule. Reports from the experimenter queue as inputs for the next plan rather than triggering one; that keeps proposal churn low.

## The reviewer's own push

When the reviewer commits fixes, GitHub raises a `synchronize` event like any other push. Two things keep that from looping or self-cancelling: the caller's concurrency group is keyed on the run id for bot-triggered runs so they never cancel the human-triggered run that made them, and the review job skips synchronize events whose actor is the bot. The verifier in the original run is the check on those commits.

## Enforcement over prompting

Turn caps, tool allowlists, deny lists for force-push and merge, per-PR concurrency, the bot allowlist, and branch protection are all enforced outside the model. The prompts describe good behaviour; the workflows make bad behaviour impossible or at least cheap.

## What stays in the project

The benchmark harness is domain knowledge and lives in the adopting repo. visionary only knows the results contract and how to diff two results files. The vision is the owner's, and the planner never edits it.
