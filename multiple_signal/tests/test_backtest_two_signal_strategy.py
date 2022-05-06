"""Unit tests for invalid command line parameters for the
backtest_strategy.py file. These tests mainly look for
type-incorrect arguments even before initializing the
Portfolio class.
"""

import sys
import pytest
from backtest_two_signal_strategy import execute
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
                "strategy1_type", "R",
                "days1", "20",
                "strategy2_type", "M",
                "days2", "10",
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
                "strategy1_type", "M",
                "days1", "10",
                "strategy2_type", "M",
                "days2", "30",
                "top_pct", bad_top_pct
            ]
            sys.argv = argv_head + new_args
            execute()


def test_bad_days1():
    for _ in range(50):
        with pytest.raises(SystemExit):
            # Bad days Param since it has characters
            bad_n_days1 = generate_random_str_alpha()
            argv_head = [sys.argv[0]]
            new_args = [
                "tickers", "MSFT AAPL NVDA GOOG",
                "b", "20210315",
                "e", "20211023",
                "initial_aum", "10000",
                "strategy1_type", "R",
                "days1", bad_n_days1,
                "strategy2_type", "M",
                "days2", "60"
                "top_pct", "60"
            ]
            sys.argv = argv_head + new_args
            execute()

def test_bad_days2():
    for _ in range(50):
        with pytest.raises(SystemExit):
            # Bad days Param since it has characters
            bad_n_days2 = generate_random_str_alpha()
            argv_head = [sys.argv[0]]
            new_args = [
                "tickers", "MSFT AAPL NVDA GOOG",
                "b", "20210315",
                "e", "20211023",
                "initial_aum", "10000",
                "strategy_type", "R",
                "days1", "40",
                "strategy2_type", "M",
                "days2", bad_n_days2,
                "top_pct", "60"
            ]
            sys.argv = argv_head + new_args
            execute()