"""Validate the visionary plugin and repo: manifests parse, every skill has
frontmatter with name and description, and nothing token-shaped is committed.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOKEN_PATTERNS = [
    r"sk-ant-[A-Za-z0-9_-]{20,}",
    r"ghp_[A-Za-z0-9]{30,}",
    r"github_pat_[A-Za-z0-9_]{30,}",
    r"xox[bp]-[A-Za-z0-9-]{20,}",
    r"lin_api_[A-Za-z0-9]{20,}",
    r"sk-proj-[A-Za-z0-9_-]{20,}",
]


def fail(msg: str) -> None:
    print(f"FAIL {msg}")
    fail.count += 1  # type: ignore[attr-defined]


fail.count = 0  # type: ignore[attr-defined]


def check_json(path: Path, required: list[str]) -> None:
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        fail(f"{path}: {exc}")
        return
    for field in required:
        if field not in data:
            fail(f"{path}: missing {field}")


def frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text()
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        fail(f"{path}: no frontmatter")
        return {}
    fm: dict[str, str] = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm


def main() -> int:
    check_json(ROOT / ".claude-plugin" / "marketplace.json", ["name", "owner", "plugins"])
    check_json(ROOT / "plugin" / ".claude-plugin" / "plugin.json", ["name", "version"])

    skills = sorted((ROOT / "plugin" / "skills").glob("*/SKILL.md"))
    if not skills:
        fail("no skills found")
    for skill in skills:
        fm = frontmatter(skill)
        for field in ("name", "description"):
            if field not in fm:
                fail(f"{skill}: frontmatter missing {field}")
        if fm.get("name") and fm["name"] != skill.parent.name:
            fail(f"{skill}: name {fm['name']} does not match directory {skill.parent.name}")
        body = skill.read_text()
        if "conventions" not in body and skill.parent.name != "conventions":
            fail(f"{skill}: does not reference the conventions skill")

    for path in ROOT.rglob("*"):
        if path.is_dir() or ".git" in path.parts or path.name.endswith((".png", ".jpg")):
            continue
        try:
            text = path.read_text()
        except (UnicodeDecodeError, PermissionError):
            continue
        for pattern in TOKEN_PATTERNS:
            if re.search(pattern, text):
                fail(f"{path}: token-shaped string matches {pattern}")

    if fail.count:  # type: ignore[attr-defined]
        return 1
    print(f"ok: {len(skills)} skills validated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
