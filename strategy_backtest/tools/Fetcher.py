"""Module containing the Fetcher class. This class fetches financial
data about all the tickers listed in the arguments and cleans them
slightly before being used to execute backtesting via the Executor
Class."""

from datetime import datetime, timedelta
from math import ceil
import yfinance as yf
import pandas as pd

class Fetcher:
    """Class that fetches data about multiple tickers

    This class also performs basic data preparation for tickers
    and sanity checks for whether the data contains proper entries
    or not.

    Attributes:
        n_months: number of months that rebalancing is done
        begin_date: date of which position is taken at end of month
        end_date: final day to take position
        days: number of days used to compute strategy-related returns
        data: Raw financial information about ticker
    """
    def __init__(self, args: dict) -> None:
        self.n_months = None
        self.begin_date = args["b"]
        self.end_date = args["e"]
        self.strat = args["strategy_type"]
        self.days = args["days"] if self.strat == "R" \
            else args["days"] + 20
        self.data = self.setup_data(args["tickers"])

    def determine_period(self, days: int) -> int:
        """Conservatively Determines which day to start fetching data

        Args:
            days: number indicated in --days parameter

        Returns:
            Number of trading days before --b to start fetching data from
        """
        # Depending on number of days, determine timing window
        if self.strat == "M":
            return ceil(30 + (7 / 4 * days))
        # Timing window if strategy is Reversal
        return ceil(10 + (7 / 4 * days))


    def setup_data(self, tickers: "list[str]") -> dict:
        """Setups up data so that it is more easily processed

        Maps tickers to its respective last trading days and processed
        dataframe so that data is well set up for calculation later on.

        Args:
            tickers: list of tickers being tracked

        Returns:
            dictionary of tickers as keys and its data as values
        """
        # self.data contains tickers, mapped to its data frame and
        # last trading day. Essentially, data is a dict of dict
        data = {ticker: {} for ticker in tickers}
        start_retrieve = self.begin_date - \
            timedelta(days = self.determine_period(self.days))
        end_retrieve = self.end_date
        # Initialize data for each ticker
        for ticker in tickers:
            print(f"Retrieving yfinance data for {ticker}")
            ticker_df = self.fetch_data(ticker, start_retrieve, end_retrieve)
            processed_df = self.process_df(ticker_df)
            last_trading_days = self.find_last_days(ticker, ticker_df)
            data[ticker]["df"] = processed_df
            data[ticker]["last_days"] = last_trading_days
        print("Raw data for all necessary tickers fetched")
        return data

    def fetch_data(self, ticker: str,
            start_retri: datetime,
            end_retri: datetime
        ) -> pd.DataFrame:
        """Fetches relevant financial data from the yfinance tracker.

        Args:
            tickers: name of ticker being tracked
            start_retri: date to start retrieving data from
            end_retri: final date to retrieve data from

        Returns:
            Dataframe of financial data from the given ticker
        """
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
        """Adds the stocks adjusted for dividends column to df

        Args:
            df: dataframe of data w/o stocks adjusted for dividends

        Returns:
            dataframe of data with stocks adjusted for dividends
        """
        # cumsum used for Culminative Dividends
        df["Close_Adjusted"] = (
            df["Close"] + df["Dividends"].cumsum()
        )
        return df

    def find_last_days(self, ticker: str, df: pd.DataFrame) -> "list":
        """Finds the last days of the month for each ticker

        Circumvents the possibility that each ticker
        might have different trading days

        Args:
            ticker: stock to track
            df: dataframe of financial data with date as index

        Returns:
            list of last trading days of the month for given ticker
        """
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
