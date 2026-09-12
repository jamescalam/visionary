"""Diff two benchmark results files (see plugin/skills/experiment/results-schema.md)
and print a markdown table. Usage: bench_delta.py head.json [base.json]
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def load(path: str) -> dict | None:
    p = Path(path)
    if not p.exists():
        return None
    return json.loads(p.read_text())


def key(suite: dict) -> tuple[str, str]:
    return (suite.get("name", ""), suite.get("variant", ""))


def fmt(value: float) -> str:
    if isinstance(value, float):
        return f"{value:.4g}"
    return str(value)


def main() -> int:
    head = load(sys.argv[1])
    base = load(sys.argv[2]) if len(sys.argv) > 2 else None
    if head is None:
        print("<!-- visionary:bench -->\n## Benchmark\n\nNo results file produced on this branch.")
        return 0
    directions = head.get("directions", {})
    base_by_key = {key(s): s for s in (base or {}).get("suites", [])}

    lines = ["<!-- visionary:bench -->", "## Benchmark", ""]
    lines.append(f"head `{head.get('commit', '?')}`" + (f" vs base `{base.get('commit', '?')}`" if base else " (no base results)"))
    lines.append("")
    lines.append("| suite | variant | metric | base | head | delta | |")
    lines.append("|---|---|---|---:|---:|---:|:-:|")
    for suite in head.get("suites", []):
        b = base_by_key.get(key(suite))
        for metric, value in sorted(suite.get("metrics", {}).items()):
            bval = (b or {}).get("metrics", {}).get(metric)
            if bval is None or not isinstance(value, (int, float)) or not isinstance(bval, (int, float)):
                delta, mark, bstr = "", "", "" if bval is None else fmt(bval)
            else:
                d = value - bval
                rel = f" ({d / bval * 100:+.1f}%)" if bval else ""
                delta = f"{d:+.4g}{rel}"
                direction = directions.get(metric)
                if direction is None or abs(d) < 1e-12:
                    mark = ""
                elif (direction == "up") == (d > 0):
                    mark = "better"
                else:
                    mark = "worse"
                bstr = fmt(bval)
            lines.append(f"| {suite.get('name','')} | {suite.get('variant','')} | {metric} | {bstr} | {fmt(value)} | {delta} | {mark} |")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
