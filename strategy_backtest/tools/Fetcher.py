from datetime import datetime, timedelta
from math import ceil
import yfinance as yf
import pandas as pd
import numpy as np

class Fetcher:
    """Class that fetches data about multiple tickers"""
    def __init__(self, args: dict) -> None:
        self.n_months = None
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
        """Setups up data so that it is more easily processed"""
        data = {ticker: {} for ticker in tickers}
        start_retrieve = self.begin_date - \
            timedelta(days = self.determine_period(self.days))
        end_retrieve = self.end_date
        for ticker in tickers:
            ticker_df = self.fetch_data(ticker, start_retrieve, end_retrieve)
            processed_df = self.process_df(ticker_df)
            last_trading_days = self.find_last_days(ticker, ticker_df)
            data[ticker]["df"] = processed_df
            data[ticker]["last_days"] = last_trading_days
        return data

    def fetch_data(self, ticker: str,
        start_retri: datetime,
        end_retri: datetime) -> pd.DataFrame:
        tracker = yf.Ticker(ticker)
        try:
            df: pd.DataFrame = tracker.history(
                start = start_retri,
                end = end_retri
            )[start_retri: end_retri]
            if len(df) == 0:
                raise Exception(f"No data available for ticker {ticker}")
            return df
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

    def find_last_days(self, ticker: str, df: pd.DataFrame) -> np.array:
        dates_idx = df.loc[
            df.groupby(df.index.to_period('M')).apply(lambda x: x.index.max())
        ].index
        dates_list = dates_idx.to_list()
        dates_np_filter = list(filter(lambda x:
            self.begin_date <= x <= self.end_date, dates_list
        ))
        # Check if stocks have the same time-frame
        if self.n_months is None:
            self.n_months = len(dates_np_filter)
        elif self.n_months != len(dates_np_filter):
            raise ValueError(f"{ticker} might not be trading in entire period")
        return dates_np_filter
