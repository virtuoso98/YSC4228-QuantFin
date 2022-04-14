from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd

class Fetcher:
    """Class that fetches data about multiple tickers"""
    def __init__(self, args: dict) -> None:
        fetcher_args = self._check_fetcher_args(args)
        self.tickers = fetcher_args["tickers"]
        self.start_date = fetcher_args["start_date"]
        self.end_date = fetcher_args["end_date"]

    def _check_fetcher_args(self, args: dict) -> dict:

        # Datetime automatically checks for datetime argument errors
        start_date = datetime.strptime(args["b"], "%Y%m%d")
        end_date = datetime.strptime(args["e"], "%Y%m%d") \
            if args["e"] is not None else datetime.now()

        # Compensate for yfinance bug, more specifically:
        # API Given Tracks until 1 day before end
        end_date += timedelta(days = 1)

        # Start date cannot be later than current date
        if start_date > datetime.now():
            raise ValueError("Start date cannot be after current time")

        # Start date cannot be later than the ending date
        if start_date > end_date:
            raise ValueError("End Date is earlier than Start Date")

        fetcher_args = {
            "tickers": args["tickers"],
            "start_date": start_date,
            "end_date": end_date
        }
        return fetcher_args