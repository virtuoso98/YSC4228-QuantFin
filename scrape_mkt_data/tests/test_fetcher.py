import pytest
from tools.fetcher import Fetcher

def test_bad_date_1():
    # Test without end_date argument
    # Bad beginning date since it's in the future
    input_args = {
        "ticker": "MSFT",
        "b": "20251202",
        "e": None,
        "initial_aum": 10000,
        "plot": False
    }
    with pytest.raises(ValueError) as excinfo:
        _ = Fetcher(input_args)
        assert "Start date cannot be after current time" in excinfo.value

def test_bad_date_2():
    # Bad beginning date that is earlier
    # then the end date
    input_args = {
        "ticker": "MSFT",
        "b": "20201202",
        "e": "20200604",
        "initial_aum": 10000,
        "plot": False
    }
    with pytest.raises(ValueError) as excinfo:
        _ = Fetcher(input_args)
        assert "End Date is earlier than Start Date" in excinfo.value
