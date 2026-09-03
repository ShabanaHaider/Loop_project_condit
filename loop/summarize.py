"""Prose helpers.

Deterministic and offline -- no model call, so an unattended firing from Task
Scheduler cannot fail or drift. The content files hard-wrap their prose, so
paragraphs are rejoined before any sentence splitting.
"""

from __future__ import annotations

import re
import textwrap

SENTENCE = re.compile(r"(?<=[.!?])\s+(?=[A-Z(*`])")


def clean(text: str) -> str:
    """Strip markdown emphasis, code ticks and links; collapse whitespace."""
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"\*\*([^*]*)\*\*", r"\1", text)
    text = re.sub(r"\*([^*]+)\*", r"\1", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    return re.sub(r"\s+", " ", text).strip()


def first_sentences(body: str, count: int = 2, width: int = 420) -> str:
    """The opening prose of a markdown body, headings and lists skipped."""
    paragraph: list[str] = []
    for raw in body.splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or re.match(r"^(?:[-*+]|\d+[.)])\s", line):
            if paragraph:
                break
            continue
        paragraph.append(line)

    joined = clean(" ".join(paragraph))
    if not joined:
        return ""
    sentences = [s.strip() for s in SENTENCE.split(joined) if s.strip()]
    return textwrap.shorten(" ".join(sentences[:count]), width=width, placeholder=" ...")
