"""progress.md is the spine.

Everything the loop knows about its own past lives in this one file: which
content files are already recorded, and in what order. Nothing else is
persisted.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROGRESS = ROOT / "progress.md"

LEDGER_START = "<!-- ledger:start -->"
LEDGER_END = "<!-- ledger:end -->"

TEMPLATE = f"""# Progress

Working memory for the RAS content loop. Each run reads this file, records
**one** content file that is not already listed below, and writes itself back.
The ledger is the loop's memory: if a file appears there, no later run touches
it again.

## Ledger

{LEDGER_START}
| Run | Date | Item | Title | Source |
| --- | --- | --- | --- | --- |
{LEDGER_END}

## Entries
"""


@dataclass
class Memory:
    seen: list[str]          # item ids already recorded, in order
    run_count: int

    def has(self, iid: str) -> bool:
        return iid in self.seen


def _ensure() -> str:
    if not PROGRESS.exists():
        PROGRESS.write_text(TEMPLATE, encoding="utf-8")
    return PROGRESS.read_text(encoding="utf-8")


def read() -> Memory:
    text = _ensure()
    try:
        block = text.split(LEDGER_START, 1)[1].split(LEDGER_END, 1)[0]
    except IndexError:
        raise SystemExit(f"{PROGRESS.name} is missing its ledger markers; delete it to regenerate")

    seen: list[str] = []
    for line in block.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 3:
            continue
        if not re.fullmatch(r"\d+", cells[0]):   # skip header and separator rows
            continue
        iid = cells[2]
        if iid and iid not in seen:
            seen.append(iid)
    return Memory(seen=seen, run_count=len(seen))


def append(*, run: int, date: str, iid: str, title: str, source: str, entry: str) -> None:
    text = _ensure()
    row = f"| {run} | {date} | {iid} | {title} | {source} |\n"

    head, rest = text.split(LEDGER_START, 1)
    block, tail = rest.split(LEDGER_END, 1)
    if not block.endswith("\n"):
        block += "\n"
    text = f"{head}{LEDGER_START}{block}{row}{LEDGER_END}{tail}"

    if not text.endswith("\n"):
        text += "\n"
    text += "\n" + entry.rstrip() + "\n"

    PROGRESS.write_text(text, encoding="utf-8")
