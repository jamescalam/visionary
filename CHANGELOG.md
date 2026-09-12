# Changelog

Breaking changes to the results contract, `.visionary.yml` keys, workflow inputs, or skill arguments are listed under **Breaking** with what an adopter has to change. Everything else under **Changed**.

## Unreleased

### Changed
- `run-agent` allows the leading word of every command in `.visionary.yml` `checks` and `bench.command`, so adopters' own tooling is not denied by the role allowlists.
- `review.yml` creates the fix label (`agent-fix-ok` by default) on first run.
- `labels.visionary` added to the config template.
