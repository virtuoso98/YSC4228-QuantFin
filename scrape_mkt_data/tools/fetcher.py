"""Module containing the Fetcher Class to get financial
 data of given ticker using the yfinance package."""

from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd

class Fetcher:
    """Class that fetches data about a given ticker

    This class does a few things:
    1.

    Attributes:
        ticker: String containing the inputted ticker name
        start_date: Beginning day of retrieved financial data
        end_date: Final day of retrieved financial data
    """
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
        # API Given Tracks until 1 day before end

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
            data: pd.DataFrame = tracker.history(
                start = self._start_date,
                end = self._end_date
            )[self._start_date : self._end_date]
            return data
        # Error can be caused as raw date is converted to seconds (Line 150):
        # https://github.com/ranaroussi/yfinance/blob/main/yfinance/base.py
        # Best solution is to try a date that's more recent, within 50 years
        except OverflowError as err:
            raise ValueError(
                "Start date too distant. Try a start date within 50 years."
                ) from err
