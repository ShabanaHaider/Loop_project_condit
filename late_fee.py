"""
Late payment fee calculator.

calculate_late_fee() should:
  - take invoice_amount (float) and days_late (int)
  - if days_late <= 0: no fee, return 0.0
  - otherwise: charge 1.5% of invoice_amount per week late,
    rounding UP any partial week to a full week
    (e.g. 1 day late still counts as 1 week)
  - the fee is capped at 10% of invoice_amount, no matter how late
  - return the result rounded to 2 decimal places

The tests in test_late_fee.py describe exactly what "done" looks like —
they are the checker, and they are what decided this implementation was
acceptable. Do not edit them to make the code pass.
"""

import math


def calculate_late_fee(invoice_amount, days_late):
    if days_late <= 0:
        return 0.0

    weeks_late = math.ceil(days_late / 7)
    fee = weeks_late * 0.015 * invoice_amount
    cap = 0.10 * invoice_amount
    return round(min(fee, cap), 2)
