from late_fee import calculate_late_fee


def test_on_time_no_fee():
    # Paid on time (or early) -> no fee at all
    assert calculate_late_fee(1000, days_late=0) == 0.0
    assert calculate_late_fee(1000, days_late=-5) == 0.0


def test_normal_late_fee():
    # 10 days late = rounds up to 2 weeks -> 2 x 1.5% x 1000 = 30.00
    assert calculate_late_fee(1000, days_late=10) == 30.00


def test_fee_is_capped_at_ten_percent():
    # 200 days late -> uncapped math would be way over 10%, so it caps at 100.00
    assert calculate_late_fee(1000, days_late=200) == 100.00
