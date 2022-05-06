import pandas as pd
from backtest_two_signal_strategy import check_validity
from tools.portfolio import Portfolio

# pylint: disable=W0212

def test_get_final_aum():
    input_args = check_validity({
        "tickers": "AAPL,TSLA,GOOG,NVDA",
        "b": "20170504",
        "e": "20170609",
        "initial_aum": 300,
        "strategy1_type": "R",
        "days1": 60,
        "strategy2_type": "R",
        "days2": 75,
        "top_pct": 100
    })

    portfolio = Portfolio(input_args)
    mock_aum = [300, 450, 540]
    portfolio.daily_aum_hist = pd.Series(
        mock_aum,
        index = pd.date_range("2022/03/07", freq="D", periods = 3)
    )
    expected_final_aum = 540
    actual_final_aum = portfolio.get_final_aum()

    assert expected_final_aum == actual_final_aum

def test_get_max_aum():
    input_args = check_validity({
        "tickers": "TSLA,GOOG,NVDA",
        "b": "20181104",
        "e": "20191225",
        "initial_aum": 760,
        "strategy1_type": "M",
        "days1": 10,
        "strategy2_type": "R",
        "days2": 45,
        "top_pct": 100
    })

    portfolio = Portfolio(input_args)
    mock_aum = [760, 1200, 1190]
    portfolio.daily_aum_hist = pd.Series(
        mock_aum,
        index = pd.date_range("2020/01/02", freq="D", periods = 3)
    )
    expected_max_aum = 1200
    actual_max_aum = portfolio.get_max_daily_aum()

    assert expected_max_aum == actual_max_aum

def test_get_average_daily_aum():
    input_args = check_validity({
        "tickers": "GOOG,NVDA",
        "b": "20160104",
        "e": "20160209",
        "initial_aum": 2000,
        "strategy1_type": "M",
        "days1": 140,
        "strategy2_type": "M",
        "days2": 250,
        "top_pct": 1
    })

    portfolio = Portfolio(input_args)
    mock_aum = [2000, 4000, 3900]
    portfolio.daily_aum_hist = pd.Series(
        mock_aum,
        index = pd.date_range("2021/04/03", freq="D", periods = 3)
    )
    expected_avg_aum = 3300
    actual_avg_aum = portfolio.get_avg_daily_aum()

    assert expected_avg_aum == actual_avg_aum

def test_get_init_pnl():
    input_args = check_validity({
        "tickers": "TSLA,NVDA",
        "b": "20140612",
        "e": "20140729",
        "initial_aum": 2000,
        "strategy1_type": "M",
        "days1": 20,
        "strategy2_type": "R",
        "days2": 15,
        "top_pct": 50
    })

    portfolio = Portfolio(input_args)
    mock_aum = [2000, 9000, 1000]
    portfolio.daily_aum_hist = pd.Series(
        mock_aum,
        index = pd.date_range("2014/06/12", freq="D", periods = 3)
    )
    expected_init_aum = 2000
    actual_init_aum = portfolio.get_init_aum()

    # floating point tolerance
    assert expected_init_aum == actual_init_aum
