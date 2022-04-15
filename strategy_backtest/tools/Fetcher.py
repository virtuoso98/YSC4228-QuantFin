from datetime import datetime, timedelta
from math import ceil
import yfinance as yf
import pandas as pd

class Fetcher:
    """Class that fetches data about multiple tickers"""
    def __init__(self, args: dict) -> None:
        self.begin_date = args["b"]
        self.end_date = args["e"]
        self.days = args["days"]
        self.strat = args["strategy_type"]
        self.data = self.setup_data(args["tickers"])


    def determine_period(self, days: int) -> int:
        """Conservatively Determines which day to start fetching data"""
        # Depending on number of days, determine timing window
        if self.strat == "M":
            return ceil(30 + (7 / 4 * days))
        # Timing window if strategy is Reversal
        return ceil(10 + (7 / 4 * days))


    def setup_data(self, tickers: "list[str]") -> dict:
        data = {}
        start_retrieve = self.begin_date - \
            timedelta(days = self.determine_period(self.days))
        end_retrieve = self.end_date
        for ticker in tickers:
            ticker_df = self.fetch_data(ticker, start_retrieve, end_retrieve)
            processed_df = self.process_df(ticker_df)
            last_trading_days = self.find_last_days(ticker_df)
            data[ticker]["data"] = processed_df
            data[ticker]["last_days"] = last_trading_days
        return data

    def fetch_data(self, ticker: str,
        start_retri: datetime,
        end_retri: datetime) -> pd.DataFrame:
        tracker = yf.Ticker(ticker)
        try:
            data: pd.DataFrame = tracker.history(
                start = start_retri,
                end = end_retri
            )[start_retri: end_retri]
            if len(data) == 0:
                raise Exception(f"No data available for ticker {ticker}")
            return data
        except OverflowError as err:
            raise ValueError(
                "Start date too distant. Try something within 10 years."
            ) from err
        except BaseException as err:
            raise err

    def process_df(self, df: pd.DataFrame) -> pd.DataFrame:
        df["Close_Adjusted"] = (
            df["Close"] + df["Dividends"].cumsum()
        )
        return df

    def find_last_days(self, df: pd.DataFrame) -> pd.DataFrame:
        pass