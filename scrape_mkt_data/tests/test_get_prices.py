import sys
import pytest
from get_prices import execute

def test_bad_string_aum():
    with pytest.raises(SystemExit):
        # Bad AUM since it's not a number
        bad_aum = "abcde"
        argv_head = [sys.argv[0]]
        new_args = [
            "ticker", "MSFT",
            "b", "20210310",
            "e", "20210520",
            "initial_aum", bad_aum,
            "plot"
        ]
        sys.argv = argv_head + new_args
        execute()

def test_bad_plot_arg():
    with pytest.raises(SystemExit):
        # Bad plot arg since it does not accept
        # any parameters
        bad_plot_arg = "True"
        argv_head = [sys.argv[0]]
        new_args = [
            "ticker", "MSFT",
            "b", "20210310",
            "e", "20210520",
            "initial_aum", "10000",
            "plot", bad_plot_arg
        ]
        sys.argv = argv_head + new_args
        execute()

