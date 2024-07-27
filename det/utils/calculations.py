def calculate_equal_split(amount, participants):
    """Calculate equal split for expenses."""
    return amount / participants

def calculate_exact_split(splits):
    """Return exact amounts for each participant."""
    return splits

def calculate_percentage_split(amount, percentages):
    """Calculate amounts based on percentage splits."""
    return [amount * (percentage / 100) for percentage in percentages]
