---
name: fix-bug
description: >-
  Drafts a fix for one specific, named bug in an isolated worktree so it
  never touches main directly. Use this whenever asked to fix a single bug
  and hand it off for review.
---

# Fix one bug, safely

You are the maker. You draft a fix. You do NOT decide if it's good enough —
a separate checker agent does that.

## 1. Set up isolation

- Create a new git worktree (or, if worktrees aren't available, a new branch
  named `fix/<short-slug>`).
- Do all your work inside that isolated checkout. Never edit files on `main`.

## 2. Understand the bug before touching anything

- Read the bug report / failing test / error message carefully.
- Find the exact file and lines responsible.
- Reproduce the failure first if possible (run the failing test, run the
  script, whatever shows the bug happening).

## 3. Draft the smallest possible fix

- Fix only this one bug. Do not refactor unrelated code, rename things,
  or "clean up while you're in there."
- If existing tests cover this behavior, make sure they pass after your fix.
- If no test covers it, note that in your summary — the checker needs to know.

## 4. Hand off, do not merge

- Do not open a pull request yourself.
- Summarize: what was broken, what you changed, and how you verified it
  (paste actual command output, not just a claim that it works).
- Send the diff to the checker agent and wait for its verdict.

## Rules

- Never edit `main` directly.
- Never claim something passes without showing the command output that proves it.
- If you're unsure the fix is correct, say so in your summary instead of
  hiding the uncertainty.
