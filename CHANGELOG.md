# Changelog

Breaking means an adopter has to change something: a removed or renamed `.visionary.yml` key, a changed meaning of one, a changed results-contract field, a removed workflow input, or a changed skill argument. Those go under **Breaking** with what to change, and bump the plugin manifest version. Additive keys and inputs go under **Changed**.

## Unreleased

### Changed
- `run-agent` allows the leading word of every command in `.visionary.yml` `checks` and `bench.command`, so adopters' own tooling is not denied by the role allowlists.
- `review.yml` creates the fix label (`agent-fix-ok` by default) on first run.
- `labels.visionary` added to the config template.
