# Late Payment Fee Calculator — Maker-Checker Loop

Same exercise as the invoice-calculator project, different business rule:

- **Concept 5 (conditional loop):** a loop that keeps running *while a
  condition is false*, with a hard cap so it can't run forever.
- **Concept 11 (maker-checker):** Claude Code does the work (maker),
  pytest decides if the work is acceptable (checker). The loop only
  trusts the checker's exit code — never the maker's own claim of "done."

## The business rule

`calculate_late_fee(invoice_amount, days_late)`:

- If `days_late <= 0` → no fee, return `0.0`.
- Otherwise → charge **1.5% of invoice_amount per week late**, rounding
  UP any partial week to a full week (so 1 day late still counts as
  "1 week").
- The fee is **capped at 10% of invoice_amount**, no matter how late.
- Result rounded to 2 decimal places.

## What's in here

- `late_fee.py` — the implementation. Started out as a placeholder that
  failed every test; now solved (see the walkthrough below).
- `test_late_fee.py` — 3 tests:
  1. `test_on_time_no_fee` — paid on time or early → no fee.
  2. `test_normal_late_fee` — 10 days late → rounds up to 2 weeks → 30.00.
  3. `test_fee_is_capped_at_ten_percent` — 200 days late → capped at 100.00,
     not the much larger uncapped number.
- `run_until_pass.ps1` — the loop, capped at 6 attempts.

## How to run it

1. `pip install pytest` (if you don't have it).
2. Open a PowerShell terminal **inside this folder**, where the `claude`
   command (Claude Code) is installed and logged in.
3. `.\run_until_pass.ps1`

If PowerShell blocks the script, run it for this session only with:
`powershell -ExecutionPolicy Bypass -File .\run_until_pass.ps1`

To watch it work from scratch again, first break `late_fee.py` — replace
the body of `calculate_late_fee` with `raise NotImplementedError` — so the
checker has something real to fail on.

## What "done" looks like

The script exits `0` and prints:
```
Checker says PASS on attempt N. Stopping loop.
```

## What actually happened, in plain English

You had a small task: "build a function that calculates a late payment
fee." Instead of just writing the code and hoping it was right, you set up
a checking system first — three simple test cases describing exactly what a
correct answer looks like (pay on time = no fee, 10 days late = a specific
small fee, 200 days late = fee stays capped, doesn't run away).

Then you had an automated helper (Claude Code) try to write the actual
code. But instead of the helper deciding for itself "yep, I'm done, looks
good to me" — which is exactly the kind of thing that goes wrong — you had
an independent, mechanical judge (the test runner) check its work every
single time. No opinions, no self-grading. Just: does the answer match what
was expected, yes or no.

Here's the sequence:

1. **First try** — there was no real code yet, just a placeholder. The
   judge said "fail" on all three checks, honestly.
2. **The helper was told to go fix it** — and importantly, it wasn't handed
   the answers directly. It had to go read the test cases itself to figure
   out what was expected, write the logic, and try again.
3. **Second try** — the judge ran the same three checks again against the
   new code. This time, all three passed.
4. **Done.** The process stopped itself, on its own, the moment the judge
   was satisfied — nobody had to eyeball the code and declare "looks good
   to me."

The point of building it this way: the helper never got to grade its own
homework. A separate, unbiased, consistent check decided when the work was
actually acceptable — same as how in accounting you wouldn't let the person
who prepared a number also be the one who signs off that it's correct. And
there was also a safety limit (stop after 6 tries) so that if the checks
and the code never lined up, it wouldn't just run forever — it would stop
and tell you something needs rethinking, instead of pretending to succeed.

## The likely trip-up

The cap test is the one worth watching. A first implementation often gets
the "1.5% per week" part right but forgets the 10% cap entirely — so
attempt 1 may pass 2 of 3 tests and fail the cap test, which is exactly
the kind of thing the checker exists to catch. If it takes 2-3 attempts
instead of 1, that's the exercise working as intended, not something
wrong with the loop.

## If it keeps hitting the cap

If it exhausts all 6 attempts, that means the fix prompt or the tests
need attention — not that the cap should be raised. Raising the cap only
buys more attempts at a process that isn't converging; it doesn't make the
work correct.
