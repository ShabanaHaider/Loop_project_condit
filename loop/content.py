"""Turn one content file into the unit the loop records.

These files are structured content, not prose: the substance lives in the YAML
frontmatter (client lists, office addresses, service groups, team credentials)
and the markdown body is usually a sentence or two of framing. So the summary
is built from the frontmatter first and falls back to the body only when there
is nothing structured to report.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

import yaml

from .summarize import clean, first_sentences

FRONTMATTER = re.compile(r"\A---\r?\n(?P<yaml>.*?)\r?\n---\r?\n?(?P<body>.*)\Z", re.DOTALL)
HEADING = re.compile(r"^#{1,6}\s+(?P<text>.+)$", re.MULTILINE)
COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)

# Keys that describe the page rather than its content.
META_KEYS = {"title", "metatitle", "metadescription", "slug", "order",
             "summary", "summarysource", "intro", "standfirst", "name", "shortname"}


@dataclass
class Item:
    iid: str                       # ledger key, e.g. "about" or "services/tax-compliance"
    title: str
    summary: str
    carries: list[str] = field(default_factory=list)


def _describe(key: str, value: object) -> str | None:
    if isinstance(value, list):
        if not value:
            return None
        noun = "entry" if len(value) == 1 else "entries"
        labels = [
            str(v.get("label") or v.get("name") or v.get("designation") or v.get("authority") or "")
            for v in value if isinstance(v, dict)
        ]
        named = [l for l in labels if l][:3]
        detail = f" ({', '.join(named)}{', ...' if len(value) > len(named) else ''})" if named else ""
        return f"{key}: {len(value)} {noun}{detail}"
    if isinstance(value, dict):
        return f"{key}: {', '.join(list(value)[:5])}"
    text = clean(str(value))
    return f"{key}: {text[:150]}" if text else None


def parse(path: str, text: str, directory: str = "content") -> Item:
    iid = path[len(directory) + 1:].removesuffix(".md") if path.startswith(directory) else path

    match = FRONTMATTER.match(text)
    if match:
        try:
            meta = yaml.safe_load(match.group("yaml")) or {}
        except yaml.YAMLError:
            meta = {}
        body = match.group("body")
    else:
        meta, body = {}, text

    if not isinstance(meta, dict):
        meta, body = {}, text

    body = COMMENT.sub("", body)

    title = clean(str(meta.get("title") or meta.get("name") or ""))
    if not title:
        heading = HEADING.search(body)
        title = clean(heading.group("text")) if heading else iid.replace("-", " ").title()

    summary = clean(str(meta.get("summary") or meta.get("intro")
                        or meta.get("standfirst") or meta.get("metaDescription") or ""))
    if not summary:
        summary = first_sentences(body, 2)
    if not summary:
        summary = f"Structured content file with no prose body ({len(meta)} frontmatter keys)."

    carries = []
    for key, value in meta.items():
        if key.lower() in META_KEYS:
            continue
        described = _describe(key, value)
        if described:
            carries.append(described)

    return Item(iid=iid, title=title, summary=summary, carries=carries[:5])
