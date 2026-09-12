"""Create or update a PR/issue comment identified by a hidden marker.
Usage: upsert_comment.py <number> <marker> <body-file>
Needs GH_TOKEN and GITHUB_REPOSITORY in the environment.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys


def gh(*args: str) -> str:
    return subprocess.run(["gh", *args], check=True, capture_output=True, text=True).stdout


def main() -> int:
    number, marker, body_file = sys.argv[1], sys.argv[2], sys.argv[3]
    repo = os.environ["GITHUB_REPOSITORY"]
    comments = json.loads(gh("api", f"repos/{repo}/issues/{number}/comments?per_page=100"))
    existing = next((c for c in comments if marker in (c.get("body") or "")), None)
    if existing:
        gh("api", "-X", "PATCH", f"repos/{repo}/issues/comments/{existing['id']}", "-F", f"body=@{body_file}")
        print(f"updated comment {existing['id']}")
    else:
        gh("api", "-X", "POST", f"repos/{repo}/issues/{number}/comments", "-F", f"body=@{body_file}")
        print("created comment")
    return 0


if __name__ == "__main__":
    sys.exit(main())
