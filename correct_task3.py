# Write your corrected implementation for Task 3 here.
# Do not modify `task3.py`.
def average_valid_measurements(values):
    """
    Calculate the average of valid numeric measurements.
    
    Args:
        values: List of measurement values (can include None, strings, numbers)
        
    Returns:
        float: Average of valid numeric measurements, or 0.0 if no valid values
        
    Important:
        Skips None values and non-numeric entries gracefully.
        Only numeric values (or strings convertible to float) are included in average.
    """
    if not values:
        return 0.0
    
    total = 0.0
    correct_count = 0
    
    for v in values:
        # Skip None values
        if v is None:
            continue
        
        # Try to convert to float
        try:
            measurement = float(v)
            total += measurement
            correct_count += 1
        except (ValueError, TypeError):
            # Skip non-numeric values
            continue
    
    return total / correct_count if correct_count > 0 else 0.0