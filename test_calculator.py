from calculator import calculate_total


def test_calculate_total_no_discount():
    # No discount: 100 subtotal, 10% tax -> 110.00
    assert calculate_total(100, 0.10) == 110.00


def test_calculate_total_with_discount():
    # 100 subtotal, 20 discount -> 80 discounted amount
    # Tax should be 10% of the DISCOUNTED amount: 80 * 0.10 = 8
    # Expected total: 80 + 8 = 88.00
    assert calculate_total(100, 0.10, discount=20) == 88.00
