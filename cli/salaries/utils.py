def generate_column_idx(column_name: str) -> int:
    """Convert Excel column letters to a 1-based column index.

    Args:
        column_name: Excel column letters (e.g., 'A', 'AA', 'ZZ')

    Returns:
        int: 1-based column index

    """
    result = 0
    for char in column_name.upper():
        value = ord(char) - ord("A") + 1
        result = result * 26 + value

    return result
