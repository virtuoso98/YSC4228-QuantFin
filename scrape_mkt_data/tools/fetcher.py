"""Module to get financial data using yfinance"""

from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd

class Fetcher:
    def __init__(self, args: dict) -> None:
        fetcher_args = self._check_fetcher_validity(args)
        self._ticker = fetcher_args["ticker"]
        self._start_date = fetcher_args["start_date"]
        self._end_date = fetcher_args["end_date"]

    def _check_fetcher_validity(self, args: dict) -> dict:
        # Check for possible ticker errors
        ticker = args["ticker"]
        if len(ticker) != 4:
            raise ValueError("Ticker should have 4 Characters")
        if not ticker.isalpha():
            raise ValueError("Ticker should only consist of letters")

        # Datetime automatically checks for datetime argument errors
        start_date = datetime.strptime(args["b"], "%Y%m%d")
        end_date = datetime.strptime(args["e"], "%Y%m%d") \
            if args["e"] is not None else datetime.now()

        # Compensate for yfinance bug, more specifically:
        # Tracks from 1 day before start until 1 day before end
        start_date += timedelta(days = 1)
        end_date += timedelta(days = 1)

        if start_date > datetime.now():
            raise ValueError("Start date cannot be after current time")

        if start_date > end_date:
            raise ValueError("End Date is earlier than Start Date")

        fetcher_args = {
            "ticker": ticker,
            "start_date": start_date,
            "end_date": end_date
        }
        return fetcher_args


    def fetch_data(self) -> pd.DataFrame:
        tracker = yf.Ticker(self._ticker)
        try:
            data = tracker.history(
                start = self._start_date,
                end = self._end_date
            )
            return data
        # Error can be caused because raw date is converted to seconds:
        # https://github.com/ranaroussi/yfinance/blob/main/yfinance/base.py
        # Best solution is to try a date that's more recent, within 50 years
        except OverflowError as err:
            raise ValueError(
                "Start date too distant. Try a start date within 50 years."
                ) from err
