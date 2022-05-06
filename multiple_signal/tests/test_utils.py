"""Sub-module containing utility functions for unit-testing
functions featured in the backtest strategy repository.
"""

import random
import string

def generate_random_str_alpha() -> str:
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

def generate_random_str_exclu(forbid: set) -> str:
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
        if random_str in forbid:
            continue
        return random_str

def generate_random_ticker_dummy() -> "list[str]":
    n_tickers = random.randint(1, 100)
    tickers = []
    str_ascii_digits = string.ascii_letters + string.digits
    for _ in range(n_tickers):
        length = random.randint(2, 5)
        dummy_ticker = ''.join(
            (random.choice(str_ascii_digits) for _ in range(length))
        )
        tickers.append(dummy_ticker)
    return tickers
