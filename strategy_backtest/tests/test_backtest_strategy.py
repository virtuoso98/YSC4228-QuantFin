"""Unit tests for invalid command line parameters for the
backtest_strategy.py file. These tests mainly look for
type-incorrect arguments even before initializing the
Portfolio class.
"""

import sys
import pytest
from backtest_strategy import execute
from tests.test_utils import generate_random_str_alpha

def test_bad_string_aum():
    for _ in range(50):
        with pytest.raises(SystemExit):
            # Bad AUM Param since it has characters
            bad_aum = generate_random_str_alpha()
            argv_head = [sys.argv[0]]
            new_args = [
                "tickers", "MSFT AAPL NVDA GOOG",
                "b", "20210315",
                "e", "20211023",
                "initial_aum", bad_aum,
                "strategy_type", "R",
                "days", "20",
                "top_pct", "75"
            ]
            sys.argv = argv_head + new_args
            execute()

def test_bad_top_pct():
    for _ in range(50):
        with pytest.raises(SystemExit):
            # Bad top_pct Param since it has characters
            bad_top_pct = generate_random_str_alpha()
            argv_head = [sys.argv[0]]
            new_args = [
                "tickers", "MSFT AAPL NVDA GOOG",
                "b", "20210315",
                "e", "20211023",
                "initial_aum", "10000",
                "strategy_type", "R",
                "days", "20",
                "top_pct", bad_top_pct
            ]
            sys.argv = argv_head + new_args
            execute()


def test_bad_days():
    for _ in range(50):
        with pytest.raises(SystemExit):
            # Bad days Param since it has characters
            bad_n_days = generate_random_str_alpha()
            argv_head = [sys.argv[0]]
            new_args = [
                "tickers", "MSFT AAPL NVDA GOOG",
                "b", "20210315",
                "e", "20211023",
                "initial_aum", "10000",
                "strategy_type", "R",
                "days", bad_n_days,
                "top_pct", "60"
            ]
            sys.argv = argv_head + new_args
            execute()
