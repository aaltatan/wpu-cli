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


def generate_column_name(column_number: int) -> str:
    """Convert a 1-based column index to Excel column letters.

    Args:
        column_number: 1-based column index

    Returns:
        str: Excel column letters

    Examples:
        >>> generate_column_name(1)
        'A'
        >>> generate_column_name(26)
        'Z'
        >>> generate_column_name(27)
        'AA'
        >>> generate_column_name(702)
        'ZZ'
        >>> generate_column_name(703)
        'AAA'

    """
    if column_number < 1:
        message = f"Column number must be >= 1: {column_number}"
        raise ValueError(message)

    result = ""

    while column_number > 0:
        # Adjust to 0-based for modulo operation
        column_number -= 1
        # Get the remainder (0-25) and convert to letter
        remainder = column_number % 26
        result = chr(ord("A") + remainder) + result
        # Move to next digit
        column_number //= 26

    return result
