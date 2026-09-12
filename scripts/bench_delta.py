"""Diff two benchmark results files (see plugin/skills/experiment/results-schema.md)
and print a markdown comment. Usage: bench_delta.py head.json [base.json]

Headline table: one row per suite/variant, one column per metric that has a
direction. Every other metric goes into a collapsed full table.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

MARKER = "<!-- visionary:bench -->"


def load(path: str) -> dict | None:
    p = Path(path)
    if not p.exists():
        return None
    return json.loads(p.read_text())


def key(suite: dict) -> tuple[str, str]:
    return (suite.get("name", ""), suite.get("variant", ""))


def fmt(value) -> str:
    if isinstance(value, bool):
        return str(value)
    if isinstance(value, float):
        return f"{value:.4g}"
    return str(value)


def cell(metric: str, head, base, directions: dict) -> str:
    if base is None or not isinstance(head, (int, float)) or not isinstance(base, (int, float)):
        return fmt(head)
    d = head - base
    if abs(d) < 1e-12:
        return f"{fmt(head)} (=)"
    direction = directions.get(metric)
    rel = f" {d / base * 100:+.1f}%" if base else ""
    verdict = ""
    if direction == "up":
        verdict = " better" if d > 0 else " worse"
    elif direction == "down":
        verdict = " better" if d < 0 else " worse"
    return f"{fmt(base)} → {fmt(head)} ({d:+.4g}{rel}{verdict})"


def main() -> int:
    head = load(sys.argv[1])
    base = load(sys.argv[2]) if len(sys.argv) > 2 else None
    if head is None:
        print(f"{MARKER}\n## Benchmark\n\nNo results file produced on this branch.")
        return 0
    directions = head.get("directions", {})
    base_by_key = {key(s): s for s in (base or {}).get("suites", [])}
    suites = head.get("suites", [])

    headline = [m for m in directions if any(m in s.get("metrics", {}) for s in suites)]
    others = sorted({m for s in suites for m in s.get("metrics", {})} - set(headline))

    lines = [MARKER, "## Benchmark", ""]
    if base:
        lines.append(f"head `{head.get('commit', '?')}` against base `{base.get('commit', '?')}`. Cells read base → head (delta, verdict).")
    else:
        lines.append(f"head `{head.get('commit', '?')}`, no base results (the base has no benchmark yet or it failed).")
    lines.append("")
    lines.append("| suite | variant | " + " | ".join(headline) + " |")
    lines.append("|---|---|" + "|".join(["---:"] * len(headline)) + "|")
    for s in suites:
        if s.get("error"):
            lines.append(f"| {s.get('name','')} | {s.get('variant','')} | failed: `{s['error'][:120]}` |" + " |" * (len(headline) - 1))
            continue
        b = base_by_key.get(key(s), {}).get("metrics", {})
        row = [cell(m, s["metrics"].get(m), b.get(m), directions) if m in s["metrics"] else "" for m in headline]
        lines.append(f"| {s.get('name','')} | {s.get('variant','')} | " + " | ".join(row) + " |")

    if others:
        lines += ["", "<details><summary>All metrics</summary>", "", "| suite | variant | " + " | ".join(others) + " |", "|---|---|" + "|".join(["---:"] * len(others)) + "|"]
        for s in suites:
            b = base_by_key.get(key(s), {}).get("metrics", {})
            row = [cell(m, s["metrics"].get(m), b.get(m), directions) if m in s["metrics"] else "" for m in others]
            lines.append(f"| {s.get('name','')} | {s.get('variant','')} | " + " | ".join(row) + " |")
        lines += ["", "</details>"]
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
