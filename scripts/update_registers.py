#!/usr/bin/env python3
"""Refresh the register block in README.md from public GitHub data.

Only public data is used, even if the token can see more. The README is left
untouched on any failure, and it is only written when a value changed.
"""

import datetime
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

USER = "alyxcial"
README = Path(__file__).resolve().parent.parent / "README.md"
COMMENT_WIDTH = 15  # keeps each line within 40 columns for phones

REGISTER_BLOCK = re.compile(
    r"(?P<head>^; =+ R E G I S T E R S =+\n)(?:^; R[A-Z]{2} .*\n)+",
    re.MULTILINE,
)


def search(kind, query, **params):
    url = "https://api.github.com/search/{}?{}".format(
        kind, urllib.parse.urlencode({"q": query, **params})
    )
    request = urllib.request.Request(
        url, headers={"Accept": "application/vnd.github+json"}
    )
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        request.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def read_registers(today):
    latest = next(
        item
        for item in search(
            "commits",
            f"author:{USER} is:public",
            sort="committer-date",
            order="desc",
            per_page=30,
        )["items"]
        if not item["repository"]["private"]
    )
    commits = search(
        "commits",
        f"author:{USER} is:public committer-date:>={today.year}-01-01",
        per_page=1,
    )["total_count"]
    repos = search("repositories", f"user:{USER} is:public", per_page=1)[
        "total_count"
    ]

    return {
        "sha": latest["sha"],
        "repo": latest["repository"]["name"],
        "date": latest["commit"]["committer"]["date"][:10],
        "repos": repos,
        "commits": commits,
        "year": today.year,
    }


def clip(text):
    return text if len(text) <= COMMENT_WIDTH else text[: COMMENT_WIDTH - 1] + "~"


def render(registers):
    # RDX reads as a date in hex, 0x20261102 for 2026-11-02.
    date = int(registers["date"].replace("-", ""), 16)
    rows = [
        ("RIP", registers["sha"][:16], registers["repo"]),
        ("RAX", f"{registers['repos']:016X}", "public repos"),
        ("RCX", f"{registers['commits']:016X}", f"{registers['year']} commits"),
        ("RDX", f"{date:016X}", "last commit"),
    ]
    return "".join(f"; {name} {value} ; {clip(note)}\n" for name, value, note in rows)


def main():
    text = README.read_text(encoding="utf-8")
    today = datetime.datetime.now(datetime.timezone.utc).date()
    block = render(read_registers(today))
    updated, count = REGISTER_BLOCK.subn(
        lambda match: match["head"] + block, text
    )
    if count != 1:
        sys.exit(f"expected one register block in README.md, found {count}")
    if updated != text:
        README.write_text(updated, encoding="utf-8")


if __name__ == "__main__":
    main()
