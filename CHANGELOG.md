# Changelog

Breaking means an adopter has to change something: a removed or renamed `.visionary.yml` key, a changed meaning of one, a changed results-contract field, a removed workflow input, or a changed skill argument. Those go under **Breaking** with what to change, and bump the plugin manifest version. Additive keys and inputs go under **Changed**.

## Unreleased

### Changed
- A submitted review is now acknowledged too: on each of its inline comments, or with a short holding comment when it carries only a summary, since GitHub has no reactions endpoint for a review. The holding comment is deleted when the run ends.
- The responder's concurrency group moved from the workflow to the job, so a comment by the agents themselves can no longer cancel a pending human-triggered run and then skip itself.
- The bench workflow publishes what the suite writes as a downloadable artifact and links it from a marked block in the pull request description (`publish`), rebuilt on every push, and caches a run-history file between runs (`history`) so trend charts have data on a fresh runner.
- A single inline comment on the diff now triggers the responder. It arrives as a submitted review with an empty body and its text in the inline comments, which a workflow expression cannot read, so a gate job in `respond.yml` makes the decision.
- Any role whose run fails or reaches its turn cap now posts a notice on the PR or issue instead of going quiet. Review and respond turn caps raised to 160.
- The responder reacts to the triggering comment with eyes before it starts work, and posts a notice if the run fails, so silence never means "seen and working".
- A push by the responder or implementer now re-reviews the whole pull request; only the reviewer's own commits skip, since the verifier covers those. Decided from the head commit's `Visionary-Role` trailer.
- `reviewers` in `.visionary.yml`: the implementer and experimenter request those people on every PR they open.
- New `respond` role and `respond.yml` reusable workflow: acts on human comments on agent-opened PRs and issues, and on `@vision` mentions anywhere. The verifier runs after it pushes.
- Every agent comment, issue body, and PR body starts with a byline naming the role and linking the run; commits are authored as `visionary-<role>`.
- `run-agent` allows the leading word of every command in `.visionary.yml` `checks` and `bench.command`, so adopters' own tooling is not denied by the role allowlists.
- `review.yml` creates the fix label (`agent-fix-ok` by default) on first run.
- `labels.visionary` added to the config template.
