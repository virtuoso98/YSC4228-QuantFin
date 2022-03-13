import pytest
from tools.fetcher import Fetcher

def test_start_date_later_then_today():
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

def test_start_date_later_then_end_date():
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

def test_start_date_improper_format():
    # Bad beginning date that is earlier
    # then the end date
    input_args = {
        "ticker": "MSFT",
        "b": "202e1z02",
        "e": "20200604",
        "initial_aum": 10000,
        "plot": False
    }
    with pytest.raises(ValueError) as excinfo:
        # datetime based error
        _ = Fetcher(input_args)
        assert "does not match format" in excinfo.value

def test_end_date_improper_format():
    # Bad beginning date that is earlier
    # then the end date
    input_args = {
        "ticker": "AAPL",
        "b": "20190214",
        "e": "2020ef13",
        "initial_aum": 10000,
        "plot": False
    }
    with pytest.raises(ValueError) as excinfo:
        # datetime based error
        _ = Fetcher(input_args)
        assert "does not match format" in excinfo.value
