"""Sub-module containing utility functions for unit-testing
functions featured in the backtest strategy repository.
"""

import random
import string

def generate_random_str() -> str:
    """Generates a random string with alphabets

    Returns:
        Randomized string with at least 1 ascii alphabet
    """
    length = random.randint(1, 15)
    str_ascii_digits = string.ascii_letters + string.digits
    while True:
        random_str = ''.join(
            (random.choice(str_ascii_digits) for _ in range(length))
            )
        if random_str.isnumeric():
            continue
        return random_str
