# Write your corrected implementation for Task 1 here.
# Do not modify `task1.py`.
def calculate_average_order_value(orders):
    """
    Calculate the average order value for non-cancelled orders.

    Args:
        orders: List of order dictionaries with 'status' and 'amount' keys
    
    Returns:
        float: Average order value, or 0.0 if no valid orders
    """

    if not orders: # handles, None, empty list, empty tuple
        return 0.0
    
    total = 0.0
    correct_count = 0

    for order in orders:
        # skip if not a Dict or missing keys
        if not isinstance(order, dict):
            continue
        if "status" not in order or "amount" not in order:
            continue 

        # Skip cancelled orders
        if order.get("status") == "cancelled":
            continue
        
        # try to convert amount to float
        try:
            amount = float(order["amount"])
            total += amount 
            correct_count += 1

        except (ValueError, TypeError):
            # skip invalid amounts
            continue
        
    return total / correct_count if correct_count > 0 else 0.0