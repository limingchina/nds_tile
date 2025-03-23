import logging

logger = logging.getLogger(__name__)

def format_binary_representation(value):
    """
    Converts an integer to its binary representation and formats it with spaces 
    every 4 bits starting from the right for readability.

    Args:
        value: The integer to convert.

    Returns:
        A string representing the formatted binary representation of the integer.
    """
    binary_representation = bin(value)[2:][::-1]
    formatted_binary = ' '.join(binary_representation[i:i+4] for i in range(0, len(binary_representation), 4))
    return formatted_binary[::-1]


def print_binary_representation(value, label="Value"):
    """
    Prints the formatted binary representation of an integer along with a label.

    Args:
        value: The integer to print in binary.
        label: An optional label to print before the binary representation.
               Defaults to "Value".
    """
    formatted_binary = format_binary_representation(value)
    logger.debug("%s: %s", label, formatted_binary)

# Example usage (you can remove this if you only need the functions):
if __name__ == "__main__":
    logging.basicConfig()
    logger.setLevel(logging.DEBUG)

    test_value1 = 123456789
    test_value2 = 255
    test_value3 = 10

    print_binary_representation(test_value1, "Test Value 1")
    print_binary_representation(test_value2, "Test Value 2")
    print_binary_representation(test_value3)  # Using the default label
