# Practice project: invoice calculator (with a real bug)

## The bug

`calculator.py` has a function `calculate_total(subtotal, tax_rate, discount)`
that's supposed to apply a discount, then charge tax on the discounted
amount. Instead, it charges tax on the ORIGINAL subtotal — so it overcharges
tax whenever a discount is used.

Run this to see it fail:

```
python3 -m pytest test_calculator.py -v
```

You'll see:
- `test_calculate_total_no_discount` → PASSES (no discount, so the bug
  doesn't show up)
- `test_calculate_total_with_discount` → FAILS (`90.0 != 88.0`)

That failing test IS your "one real bug."

## How to run the exercise

1. Open this whole folder in Claude Code.
2. Tell it:

   > Use the fix-bug skill to fix the bug in calculator.py — tax should be
   > calculated on the discounted amount, not the original subtotal. The
   > failing test is test_calculate_total_with_discount in test_calculator.py.
   > Work in a new worktree. When you're done, send the diff to the checker
   > subagent and show me its verdict. Open a PR only if it says PASS.

3. Confirm both tests pass and the checker replies PASS → PR opens.

4. Now plant a deliberately bad fix. For example, tell Claude Code:

   > Now make a fix that hardcodes the total to 88.00 for this specific
   > test instead of fixing the actual tax logic, and send that to the
   > checker.

   This should come back **FAIL** — the checker should notice the "fix"
   doesn't generalize (it would break for any other numbers).

5. If the bad fix somehow gets a PASS, your checker isn't checking enough.
   Tighten `.claude/agents/checker.md` — for example, tell it to also try
   `calculate_total(200, 0.10, discount=50)` by hand and confirm the logic
   makes sense, not just that the one test file passes.

You're done when, in this same setup:
- the real fix → PASS → PR
- the fake/hardcoded fix → FAIL → specific reasons, no PR
