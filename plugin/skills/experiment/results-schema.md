# Benchmark results contract

A repo that adopts visionary exposes one command (`bench.command` in `.visionary.yml`, usually `make bench`) that writes one JSON file (`bench.results`, usually `benchmarks/results.json`). The bench-delta action and the experiment skill read only this file.

```json
{
  "schema": 1,
  "commit": "556de2c",
  "timestamp": "2026-09-12T18:00:00Z",
  "directions": { "boundary_f1": "up", "pk": "down", "windowdiff": "down", "wall_s": "down", "encoder_calls": "down" },
  "suites": [
    {
      "name": "synthetic-boundaries",
      "variant": "statistical/minilm/w5",
      "config": { "chunker": "statistical", "encoder": "all-MiniLM-L6-v2", "window_size": 5 },
      "metrics": { "boundary_f1": 0.81, "pk": 0.12, "windowdiff": 0.15, "wall_s": 12.4, "encoder_calls": 4 }
    }
  ]
}
```

Rules:

- `directions` names every metric that appears and whether higher (`up`) or lower (`down`) is better. Metrics without a direction are reported without a verdict.
- A suite entry is identified by `name` plus `variant`. Deltas are computed between entries with the same identity on two commits.
- `metrics` values are numbers. Anything else belongs in `config`.
- The command must be deterministic for a fixed `config` and seed, or must record the seed in `config`.
- The command may accept an experiment config path as its first argument; `bench.experiments` in `.visionary.yml` says where those live.
