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

    # BUG: tax is being calculated on the ORIGINAL subtotal instead of
    # the discounted amount. This overcharges tax whenever a discount
    # is applied.
    total = discounted + (subtotal * tax_rate)

    return round(total, 2)
