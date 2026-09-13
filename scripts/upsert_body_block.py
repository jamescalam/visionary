"""Insert or replace a marked block in a pull request's body.

Usage: upsert_body_block.py <pr-number> <marker> <block-file>

The marker is an HTML comment such as ``<!-- visionary:artifacts -->``; the
block is delimited by it and its closing form ``<!-- /visionary:artifacts -->``
so a later run replaces exactly what an earlier one wrote and never disturbs
the prose around it. A body that has no such block gets one appended.

Needs GH_TOKEN and GITHUB_REPOSITORY in the environment.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys


def gh(*args: str, input: str | None = None) -> str:
    return subprocess.run(
        ["gh", *args], check=True, capture_output=True, text=True, input=input
    ).stdout


def main() -> int:
    number, marker, block_file = sys.argv[1], sys.argv[2], sys.argv[3]
    repo = os.environ["GITHUB_REPOSITORY"]
    closing = marker.replace("<!-- ", "<!-- /", 1)

    with open(block_file, encoding="utf-8") as fh:
        block = fh.read().strip()
    section = f"{marker}\n{block}\n{closing}"

    body = json.loads(gh("api", f"repos/{repo}/pulls/{number}", "--jq", "{body: .body}"))["body"] or ""
    pattern = re.compile(
        re.escape(marker) + r".*?" + re.escape(closing), re.S
    )
    if pattern.search(body):
        new_body = pattern.sub(lambda _: section, body, count=1)
        action = "replaced"
    else:
        new_body = (body.rstrip() + "\n\n" + section + "\n") if body.strip() else section + "\n"
        action = "appended"

    if new_body == body:
        print("body already current")
        return 0

    gh(
        "api",
        "-X",
        "PATCH",
        f"repos/{repo}/pulls/{number}",
        "--input",
        "-",
        input=json.dumps({"body": new_body}),
    )
    print(f"{action} the {marker} block in #{number}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
