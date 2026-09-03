#!/usr/bin/env python3
"""One iteration of the content loop.

Read progress.md -> pick the first content file it has NOT already recorded ->
summarize it -> write the summary and the date back into progress.md.

Source: https://github.com/ShabanaHaider/ras-website/tree/master/content

Exit codes: 0 work done, 0 nothing left to do, 1 hard failure.
"""

from __future__ import annotations

import argparse
import datetime as dt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from loop import content, memory, source  # noqa: E402

ROOT = Path(__file__).resolve().parent
LOGS = ROOT / "logs"
SOURCE_LABEL = "ras-website/content"


def build_entry(*, run, date, item, path, mem, upcoming) -> str:
    if mem.seen:
        prior = ", ".join(mem.seen)
        builds_on = (
            f"run(s) before this one already recorded {len(mem.seen)} file(s) "
            f"({prior}); this run skipped them and moved on."
        )
    else:
        builds_on = "first run - the ledger was empty, so this starts the memory."

    lines = [
        f"### Run {run} - {date} - {item.iid}",
        "",
        f"- **Item:** `{item.iid}` - {item.title}",
        f"- **Source:** {source.source_url(path)}",
        f"- **Builds on:** {builds_on}",
        f"- **Summary:** {item.summary}",
    ]
    if item.carries:
        lines.append("- **Content it carries:**")
        lines.extend(f"  - {entry}" for entry in item.carries)
    lines.append(
        f"- **Next up:** {upcoming}" if upcoming
        else "- **Next up:** none - every file in the content directory is now recorded."
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run one iteration of the content loop.")
    parser.add_argument("--dry-run", action="store_true", help="report the pick without writing")
    args = parser.parse_args()

    date = dt.date.today().isoformat()
    stamp = dt.datetime.now().isoformat(timespec="seconds")

    mem = memory.read()
    paths = source.list_documents()

    def ident(path: str) -> str:
        return path[len(source.DIRECTORY) + 1:].removesuffix(".md")

    remaining = [p for p in paths if not mem.has(ident(p))]
    print(f"[{stamp}] memory: {len(mem.seen)} recorded {mem.seen or '[]'} | "
          f"source: {len(paths)} files | remaining: {len(remaining)}")

    if not remaining:
        print(f"[{stamp}] nothing new to record - the loop has consumed the whole directory.")
        return 0

    path = remaining[0]
    upcoming = ident(remaining[1]) if len(remaining) > 1 else None
    item = content.parse(path, source.fetch(path), directory=source.DIRECTORY)

    run = mem.run_count + 1
    entry = build_entry(run=run, date=date, item=item, path=path, mem=mem, upcoming=upcoming)

    if args.dry_run:
        print(entry)
        return 0

    memory.append(run=run, date=date, iid=item.iid, title=item.title,
                  source=SOURCE_LABEL, entry=entry)

    LOGS.mkdir(exist_ok=True)
    with (LOGS / "runs.log").open("a", encoding="utf-8") as handle:
        handle.write(f"{stamp}\trun={run}\titem={item.iid}\tsource={source.source_url(path)}\n")

    print(f"[{stamp}] run {run} recorded {item.iid} ({item.title}) -> progress.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
