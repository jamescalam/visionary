"""Decide whether the current tranche is complete and close its milestone.

A tranche is the highest-numbered milestone named tranche-N. It is complete
when it has no open pull requests and no open issues at all: every proposal
was either approved and shipped, or closed as rejected. Human PRs outside the
milestone never hold a tranche open.

Reads GH_TOKEN and REPO from the environment; writes complete= and tranche=
to GITHUB_OUTPUT.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys


def gh(*args: str) -> str:
    return subprocess.run(["gh", *args], check=True, capture_output=True, text=True).stdout


def out(key: str, value: str) -> None:
    path = os.environ.get("GITHUB_OUTPUT")
    line = f"{key}={value}"
    print(line)
    if path:
        with open(path, "a", encoding="utf-8") as fh:
            fh.write(line + "\n")


def main() -> int:
    repo = os.environ["REPO"]
    milestones = json.loads(gh("api", f"repos/{repo}/milestones?state=open&per_page=100"))
    tranches = []
    for m in milestones:
        match = re.fullmatch(r"tranche-(\d+)", m["title"])
        if match:
            tranches.append((int(match.group(1)), m))
    if not tranches:
        out("complete", "false")
        out("tranche", "")
        print("no open tranche milestone")
        return 0
    number, milestone = max(tranches, key=lambda t: t[0])
    title = milestone["title"]
    out("tranche", title)

    open_items = json.loads(
        gh(
            "api",
            f"repos/{repo}/issues?milestone={milestone['number']}&state=open&per_page=100",
        )
    )
    # The issues endpoint returns pull requests too; both count.
    open_prs = [i for i in open_items if "pull_request" in i]
    open_issues = [i for i in open_items if "pull_request" not in i]
    print(f"{title}: {len(open_prs)} open PRs, {len(open_issues)} open issues")
    if open_prs or open_issues:
        out("complete", "false")
        return 0

    gh("api", "-X", "PATCH", f"repos/{repo}/milestones/{milestone['number']}", "-f", "state=closed")
    print(f"closed {title}")
    out("complete", "true")
    return 0


if __name__ == "__main__":
    sys.exit(main())
