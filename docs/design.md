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

When an agent commits, GitHub raises a `synchronize` event like any other push, and the question is whether that should start a review. The reviewer's own commits should not: the verifier in the run that made them is their cold read, and re-reviewing would never terminate. Any other role's commits should, because the responder acting on human feedback or the implementer fixing something changes the pull request as a whole, and the verifier only reads the pushed range. A gate job resolves this by reading the head commit's `Visionary-Role` trailer. Separately, the caller's concurrency group is keyed on the run id for bot-triggered runs, so a bot push never cancels the run that made it.

## Enforcement over prompting

Turn caps, tool allowlists, deny lists for force-push and merge, per-PR concurrency, the bot allowlist, and branch protection are all enforced outside the model. The prompts describe good behaviour; the workflows make bad behaviour impossible or at least cheap.

## What stays in the project

The benchmark harness is domain knowledge and lives in the adopting repo. visionary only knows the results contract and how to diff two results files. The vision is the owner's, and the planner never edits it.
