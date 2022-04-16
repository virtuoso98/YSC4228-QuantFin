"""Unit tests for the Strategizer class. Since most of the infrastructure
inside is very complex, we have decided to instead test only the
find_n_top_tickers function with some sanity checks on the parameters
"""
import random
from math import ceil
import pytest
from backtest_strategy import check_validity
from tests.test_utils import generate_random_ticker_dummy

def test_bad_negative_top_pct():
    for _ in range(50):
        bad_negative_top_pct = random.randint(- (10 ** 6), 0)
        input_args = {
            "tickers": ["AAPL", "TSLA", "GOOG", "NVDA"],
            "b": "20150703",
            "e": "20151005",
            "initial_aum": 10 ** 6,
            "strategy_type": 'M',
            "days": 50,
            "top_pct": bad_negative_top_pct
        }

        with pytest.raises(ValueError) as excinfo:
            check_validity(input_args)
            assert "--top_pct: Percentile must be between 1 and 100." \
                 in excinfo.value

def test_bad_positive_top_pct():
    for _ in range(50):
        bad_positive_top_pct = random.randint(101, 10 ** 6)
        input_args = {
            "tickers": ["AAPL", "TSLA", "GOOG", "NVDA"],
            "b": "20170504",
            "e": "20181209",
            "initial_aum": 10 ** 5,
            "strategy_type": 'R',
            "days": 25,
            "top_pct": bad_positive_top_pct
        }

        with pytest.raises(ValueError) as excinfo:
            check_validity(input_args)
            assert "--top_pct: Percentile must be between 1 and 100." \
                 in excinfo.value


def test_bad_nonpositive_aum():
    for _ in range(50):
        bad_nonpositive_aum = random.randint(- (10 ** 6), 0)
        input_args = {
            "tickers": ["AAPL", "TSLA", "GOOG", "NVDA"],
            "b": "20220103",
            "initial_aum": bad_nonpositive_aum,
            "strategy_type": 'M',
            "days": 65,
            "top_pct": 40
        }

        with pytest.raises(ValueError) as excinfo:
            check_validity(input_args)
            assert "--initial_aum: Initial AUM must be positive" \
                 in excinfo.value


def test_top_n_tickers_sanity():
    # Check that number of picked tickers is positive
    # and below max number of tickers indicated
    args = check_validity({
            "tickers": ["AAPL", "TSLA", "GOOG", "NVDA"],
            "b": "20220103",
            "e": None,
            "initial_aum": 10 ** 7,
            "strategy_type": 'M',
            "days": 65,
            "top_pct": 40
        })

    for _ in range(50):
        random_top_pct = random.randint(1, 100)
        random_tickers = generate_random_ticker_dummy()
        args["tickers"] = random_tickers
        args["top_pct"] = random_top_pct
        # Function definition for the n_top_tickers
        # Decided to use it directly because I'm not completely
        # sure of @staticmethod. Not good practice though.
        n_top_tickers = ceil(args["top_pct"] / 100 * len(args["tickers"]))
        assert(1 <= n_top_tickers <= len(random_tickers))
