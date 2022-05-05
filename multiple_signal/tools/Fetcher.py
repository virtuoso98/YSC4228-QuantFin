from datetime import datetime, timedelta
from math import ceil
import yfinance as yf
import pandas as pd

class Fetcher:
    def __init__(self, args: dict) -> None:
        self.n_months = None
        self.LINE_SEPARATOR = "*" * 50
        self.begin_date = args["b"]
        self.end_date = args["e"]
        self.strat1 = args["strategy1_type"]
        self.days1 = args["days1"] if self.strat1 == "R" \
            else args["days1"] + 20
        self.strat2 = args["strategy2_type"]
        self.days2 = args["days2"] if self.strat2 == "R" \
            else args["days2"] + 20
        self.data = self.setup_data(args["tickers"])

    def determine_period(self, days: int) -> int:
        # TODO : Check if 25 should be added to both
        # Depending on number of days, determine timing window
        return ceil(35 + (7 / 4 * days))


    def setup_data(self, tickers: "list[str]") -> dict:
        # self.data contains tickers, mapped to its data frame and
        # last trading day. Essentially, data is a dict of dict
        data = {ticker: {} for ticker in tickers}
        max_days = max(self.days1, self.days2)
        start_retrieve = self.begin_date - \
            timedelta(days = self.determine_period(max_days))
        end_retrieve = self.end_date
        # Initialize data for each ticker
        print(self.LINE_SEPARATOR)
        for ticker in tickers:
            print(f"Retrieving yfinance data for {ticker}")
            ticker_df = self.fetch_data(ticker, start_retrieve, end_retrieve)
            processed_df = self.process_df(ticker_df)
            last_trading_days = self.find_last_days(ticker, ticker_df)
            data[ticker]["df"] = processed_df
            data[ticker]["last_days"] = last_trading_days
        print("Raw data for all necessary tickers fetched")
        print(self.LINE_SEPARATOR)
        return data

    def fetch_data(self, ticker: str,
            start_retri: datetime,
            end_retri: datetime
        ) -> pd.DataFrame:
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
        # cumsum used for Culminative Dividends
        df["Close_Adjusted"] = (
            df["Close"] + df["Dividends"].cumsum()
        )
        return df

    def find_last_days(self, ticker: str, df: pd.DataFrame) -> "list":
        dates_idx = df.loc[
            df.groupby(df.index.to_period('M')).apply(lambda x: x.index.max())
        ].index
        dates_list = dates_idx.to_list()

        # TODO: Add timedelta of 1 so that we can backtrack previous month
        dates_np_filter = list(filter(lambda x:
            self.begin_date <= x <= self.end_date, dates_list
        ))
        # Check if stocks have the same time-frame
        if self.n_months is None:
            self.n_months = len(dates_np_filter)
        elif self.n_months != len(dates_np_filter):
            raise ValueError(f"{ticker} might not be trading in entire period")
        print(dates_np_filter)
        return dates_np_filter
