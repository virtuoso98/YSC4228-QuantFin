import pandas as pd
from tools.processor import Processor

# pylint: disable=W0212

def test_get_final_aum():
    input_args = {
        "ticker": "AAPL",
        "b": "20220307",
        "e": "20220309",
        "initial_aum": 3000,
        "plot": False
    }

    processor = Processor(input_args)
    mock_n_stocks = 10
    mock_data = [300, 450, 540]
    mock_stock_hist = pd.Series(
        mock_data,
        index = pd.date_range("2022/03/07", freq="D", periods = 3)
    )
    actual_avg_aum = processor._get_average_aum(
        mock_stock_hist, mock_n_stocks
    )
    expected_avg_aum = 4300

    # floating point tolerance
    assert abs(expected_avg_aum - actual_avg_aum) <= 10 ** -6

def test_get_max_aum():
    input_args = {
        "ticker": "AAPL",
        "b": "20210508",
        "e": "20210510",
        "initial_aum": 9600,
        "plot": False
    }

    processor = Processor(input_args)
    mock_n_stocks = 20
    mock_data = [480, 700, 640]
    mock_stock_hist = pd.Series(
        mock_data,
        index = pd.date_range("2021/05/10", freq="D", periods = 3)
    )
    actual_avg_aum = processor._get_max_aum(
        mock_stock_hist, mock_n_stocks
    )
    expected_avg_aum = 14000

    # floating point tolerance
    assert abs(expected_avg_aum - actual_avg_aum) <= 10 ** -6

def test_get_average_aum():
    input_args = {
        "ticker": "AAPL",
        "b": "20210515",
        "e": "20210517",
        "initial_aum": 6000,
        "plot": False
    }

    processor = Processor(input_args)
    mock_n_stocks = 20
    mock_data = [300, 400, 800]
    mock_stock_hist = pd.Series(
        mock_data,
        index = pd.date_range("2021/05/15", freq="D", periods = 3)
    )
    actual_avg_aum = processor._get_average_aum(
        mock_stock_hist, mock_n_stocks
    )
    expected_avg_aum = 10000

    # floating point tolerance
    assert abs(expected_avg_aum - actual_avg_aum) <= 10 ** -6

def test_get_aum_pnl():
    input_args = {
        "ticker": "AAPL",
        "b": "20210515",
        "e": "20210517",
        "initial_aum": 6000,
        "plot": False
    }
    processor = Processor(input_args)
    mock_final_aum = 4000
    mock_initial_aum = 6000
    actual_pnl = processor._get_aum_pnl(
        mock_initial_aum, mock_final_aum
    )
    expected_pnl = -2000
    # floating point tolerance
    assert abs(actual_pnl - expected_pnl) <= 10 ** -6
