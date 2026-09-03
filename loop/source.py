"""Locate and fetch the content files the loop reads.

Target: https://github.com/ShabanaHaider/ras-website/tree/master/content

The directory is listed live on every run (one API call), so a file added to
the repo shows up as new work on the next firing without any code change.
Only the one file a run actually needs is downloaded.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request

REPO = os.environ.get("CONTENT_REPO", "ShabanaHaider/ras-website")
BRANCH = os.environ.get("CONTENT_BRANCH", "master")
DIRECTORY = os.environ.get("CONTENT_DIR", "content")

TREE_API = f"https://api.github.com/repos/{REPO}/git/trees/{BRANCH}?recursive=1"
RAW_BASE = f"https://raw.githubusercontent.com/{REPO}/{BRANCH}"


def _request(url: str, accept: str) -> bytes:
    request = urllib.request.Request(
        url, headers={"User-Agent": "loop-spine/1.0", "Accept": accept}
    )
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        request.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return response.read()
    except urllib.error.HTTPError as exc:
        raise SystemExit(f"HTTP {exc.code} fetching {url}")
    except urllib.error.URLError as exc:
        raise SystemExit(f"network error fetching {url}: {exc.reason}")


def list_documents() -> list[str]:
    """Every markdown file under the content directory, in a stable order."""
    payload = json.loads(_request(TREE_API, "application/vnd.github+json"))
    if payload.get("truncated"):
        raise SystemExit("repository tree came back truncated; narrow CONTENT_DIR")

    prefix = f"{DIRECTORY.rstrip('/')}/"
    paths = [
        entry["path"]
        for entry in payload.get("tree", [])
        if entry.get("type") == "blob"
        and entry["path"].startswith(prefix)
        and entry["path"].endswith(".md")
    ]
    if not paths:
        raise SystemExit(f"no markdown files under {prefix} in {REPO}@{BRANCH}")
    return sorted(paths)


def fetch(path: str) -> str:
    return _request(f"{RAW_BASE}/{path}", "text/plain").decode("utf-8")


def source_url(path: str) -> str:
    return f"https://github.com/{REPO}/blob/{BRANCH}/{path}"
