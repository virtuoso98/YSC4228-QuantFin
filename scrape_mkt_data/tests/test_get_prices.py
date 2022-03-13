import sys
import pytest
from get_prices import execute

def test_bad_numeric_ticker_name():
    """Test with a bad ticker name which is numeric"""
    with pytest.raises() as excinfo:
        assert "" in excinfo.value