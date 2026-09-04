def calculate_total(subtotal, tax_rate, discount=0):
    """
    Calculate the final invoice total: apply a discount to the subtotal,
    then apply tax on the discounted amount.

    Example: subtotal=100, discount=20, tax_rate=0.10
    -> discounted amount = 80
    -> tax = 80 * 0.10 = 8
    -> total = 88.00
    """
    discounted = subtotal - discount

    total = discounted + (discounted * tax_rate)

    return round(total, 2)
