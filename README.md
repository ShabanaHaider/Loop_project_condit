# Content Loop - a loop with a spine

A scheduled job that runs **once per firing**, reads its own memory, learns
exactly one new thing, and writes what it learned back. Continuity lives in a
file, not in a process, so the loop survives reboots, crashes, and long gaps.

## The spine

`progress.md` is the only state. Every run:

1. reads the ledger in `progress.md` to see which files it already knows;
2. lists the content directory live;
3. picks the **first file not in the ledger**;
4. writes a short summary plus the date back into `progress.md`.

Nothing is repeated, because step 3 consults step 1. That is the whole claim
being tested.

## Source

```
https://github.com/ShabanaHaider/ras-website/tree/master/content
```

18 markdown files - the RAS website copy: pages, the eight service files under
`content/services/`, and site-wide values. The directory is listed on every run
(one API call), so a file added to the repo becomes new work on the next firing
with no code change. Only the one file a run needs is downloaded.

Overrides: `CONTENT_REPO`, `CONTENT_BRANCH`, `CONTENT_DIR`, and `GITHUB_TOKEN`
if the repository is ever made private.

## Layout

```
run_once.py            one iteration; the scheduler's entry point
progress.md            THE MEMORY - ledger + one entry per run
loop/
  memory.py            read/append the progress.md ledger
  source.py            list the content directory, fetch one file
  content.py           frontmatter + body -> the unit the loop records
  summarize.py         prose helpers (no model call at runtime)
scripts/schedule.ps1   register the Windows Scheduled Task
scripts/unschedule.ps1 remove it
logs/runs.log          append-only trace of every firing
requirements.txt       PyYAML
```

## Run it

```powershell
pip install -r requirements.txt
python run_once.py             # do one unit of work
python run_once.py --dry-run   # show the pick without writing
```

Schedule it:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\schedule.ps1 -At 09:00
Start-ScheduledTask -TaskName ContentLoop     # fire immediately
```

## Proof that the memory works

Two consecutive runs, no arguments, no state passed between them:

```
RUN 1  memory: 0 recorded []         | remaining: 18 | recorded about (About Us)
RUN 2  memory: 1 recorded ['about']  | remaining: 17 | recorded achievements (Affiliations & Achievements)
```

Run 2 read run 1's ledger, saw `about`, skipped it, and moved to `achievements`.
That is the claim proven: the second run started from the first run's memory
and did not repeat it.

`progress.md` is the evidence, not scratch state - don't delete it. The loop
picks up wherever the ledger left off, so the next firing takes `clients` and
the 15 after it. When all 18 are recorded it reports `nothing new to record`
and writes nothing; re-running is safe and idempotent.

## Note on summarizing

These are structured content files: the substance sits in YAML frontmatter
(client lists, office addresses, service groups, team credentials) and the
markdown body is usually a sentence or two of framing. So `content.py` reads
the frontmatter first - `summary`, `intro`, `standfirst`, then
`metaDescription` - and falls back to the body's opening sentences only when
none of those exist. It also reports what structured data the file carries
(`clients: 19 entries`, `offices: 2 entries (Head Office, Branch Office)`),
which is the part a prose-only summary would miss entirely.

Extraction is deterministic - no model call at runtime, so an unattended firing
cannot fail or drift.
