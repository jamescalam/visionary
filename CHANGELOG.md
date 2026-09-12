# Changelog

Breaking means an adopter has to change something: a removed or renamed `.visionary.yml` key, a changed meaning of one, a changed results-contract field, a removed workflow input, or a changed skill argument. Those go under **Breaking** with what to change, and bump the plugin manifest version. Additive keys and inputs go under **Changed**.

## Unreleased

### Changed
- A push by the responder or implementer now re-reviews the whole pull request; only the reviewer's own commits skip, since the verifier covers those. Decided from the head commit's `Visionary-Role` trailer.
- `reviewers` in `.visionary.yml`: the implementer and experimenter request those people on every PR they open.
- New `respond` role and `respond.yml` reusable workflow: acts on human comments on agent-opened PRs and issues, and on `@vision` mentions anywhere. The verifier runs after it pushes.
- Every agent comment, issue body, and PR body starts with a byline naming the role and linking the run; commits are authored as `visionary-<role>`.
- `run-agent` allows the leading word of every command in `.visionary.yml` `checks` and `bench.command`, so adopters' own tooling is not denied by the role allowlists.
- `review.yml` creates the fix label (`agent-fix-ok` by default) on first run.
- `labels.visionary` added to the config template.
