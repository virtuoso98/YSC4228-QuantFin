"""Unit tests file for the initiation of the Fetcher
Class, along with some basic sanity tests.
"""
import random
import pytest
from backtest_two_signal_strategy import check_validity
from tests.test_utils import generate_random_str_exclu

def test_invalid_strategy1_param():
    valid_strat_param = ["R", "M"]
    for _ in range(50):
        invalid_strat = generate_random_str_exclu(valid_strat_param)
        # The sys argv has been tested in test_backtest_strategy
        # so we skip straight to input args
        input_args = {
            "tickers": "AAPL,TSLA,GOOG,NVDA",
            "b": "20211604",
            "e": "20211604",
            "initial_aum": 10 ** 6,
            "strategy1_type": invalid_strat,
            "days1": 30,
            "strategy2_type": random.choice(valid_strat_param),
            "days2": 30,
            "top_pct": 40
        }

        with pytest.raises(ValueError) as excinfo:
            check_validity(input_args)
            assert "--strategy1_type: Only 'R'(Reversal) or 'M'(Momentum)" \
                 in excinfo.value

def test_invalid_strategy2_param():
    valid_strat_param = ["R", "M"]
    for _ in range(50):
        invalid_strat = generate_random_str_exclu(valid_strat_param)
        # The sys argv has been tested in test_backtest_strategy
        # so we skip straight to input args
        input_args = {
            "tickers": "AAPL,TSLA,GOOG,NVDA",
            "b": "20211604",
            "e": "20211604",
            "initial_aum": 10 ** 6,
            "strategy1_type": random.choice(valid_strat_param),
            "days1": 50,
            "strategy2_type": invalid_strat,
            "days2": 30,
            "top_pct": 40
        }

        with pytest.raises(ValueError) as excinfo:
            check_validity(input_args)
            assert "--strategy2_type: Only 'R'(Reversal) or 'M'(Momentum)" \
                 in excinfo.value

def test_valid_strategy_params():
    valid_strat_param = ["R", "M"]
    for strat1 in valid_strat_param:
        for strat2 in valid_strat_param:
            input_args = {
                "tickers": "AAPL,TSLA,GOOG,NVDA",
                "b": "20180104",
                "e": "20190403",
                "initial_aum": 10 ** 6,
                "strategy1_type": strat1,
                "days1": 50,
                "strategy2_type": strat2,
                "days2": 30,
                "top_pct": 40
            }

            processed_args = check_validity(input_args)
            assert isinstance(processed_args, dict)

def test_bad_negative_days1():
    valid_strat_param = ["R", "M"]
    for _ in range(50):
        bad_negative_days = random.randint(- (10 ** 6), -1)
        valid_days = random.randint(1, 365)
        input_args = {
            "tickers": "AAPL,TSLA,GOOG,NVDA",
            "b": "20190403",
            "e": "20201201",
            "initial_aum": 10 ** 6,
            "strategy1_type": random.choice(valid_strat_param),
            "days1": bad_negative_days,
            "strategy2_type": random.choice(valid_strat_param),
            "days2": valid_days,
            "top_pct": 40
        }

        with pytest.raises(ValueError) as excinfo:
            check_validity(input_args)
            assert "--days1: Trading days Param must be positive." \
                 in excinfo.value

def test_bad_negative_days2():
    valid_strat_param = ["R", "M"]
    for _ in range(50):
        bad_negative_days = random.randint(- (10 ** 6), -1)
        valid_days = random.randint(1, 365)
        input_args = {
            "tickers": "AAPL,TSLA,GOOG,NVDA",
            "b": "20190403",
            "e": "20201201",
            "initial_aum": 10 ** 6,
            "strategy1_type": random.choice(valid_strat_param),
            "days1": valid_days,
            "strategy2_type": random.choice(valid_strat_param),
            "days2": bad_negative_days,
            "top_pct": 40
        }

        with pytest.raises(ValueError) as excinfo:
            check_validity(input_args)
            assert "--days2: Trading days Param must be positive." \
                 in excinfo.value

def test_bad_positive_days1():
    valid_strat_param = ["R", "M"]
    for _ in range(50):
        bad_positive_day = random.randint(251, 10 ** 6)
        valid_days = random.randint(1, 365)
        input_args = {
            "tickers": "AAPL,TSLA,GOOG,NVDA",
            "b": "20210504",
            "e": "20211204",
            "initial_aum": 10 ** 5,
            "strategy1_type": random.choice(valid_strat_param),
            "days1": bad_positive_day,
            "strategy2_type": random.choice(valid_strat_param),
            "days2": valid_days,
            "top_pct": 60
        }

        with pytest.raises(ValueError) as excinfo:
            check_validity(input_args)
            assert "--days1: Trading Days Exceed 250." \
                 in excinfo.value

def test_bad_positive_days2():
    valid_strat_param = ["R", "M"]
    for _ in range(50):
        bad_positive_day = random.randint(251, 10 ** 6)
        valid_days = random.randint(1, 365)
        input_args = {
            "tickers": "AAPL,TSLA,GOOG,NVDA",
            "b": "20210504",
            "e": "20211204",
            "initial_aum": 10 ** 5,
            "strategy1_type": random.choice(valid_strat_param),
            "days1": valid_days,
            'strategy2_type': random.choice(valid_strat_param),
            "days2": bad_positive_day,
            "top_pct": 60
        }

        with pytest.raises(ValueError) as excinfo:
            check_validity(input_args)
            assert "--days2: Trading Days Exceed 250." \
                 in excinfo.value
