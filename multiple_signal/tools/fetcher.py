"""Module containing the Fetcher class. This class fetches financial
data about all the tickers listed in the arguments and cleans them
slightly before being used to execute backtesting via the Strategizer
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
        strat1: strategy 1's type ('R' for reversal, 'M' for momentum)
        days1: number of days used to compute strategy 1 signal returns
        strat2: strategy 2's type ('R' for reversal, 'M' for momentum)
        days2: number of days used to compute strategy 2 signal returns
        data: Raw financial information about ticker
        LINE_SEPARATOR: Constant in line separating for presentability
    """
    def __init__(self, args: dict) -> None:
        self.n_months = None
        self.LINE_SEPARATOR = "*" * 50
        self.begin_date: datetime = args["b"]
        self.end_date: datetime = args["e"]
        self.strat1 = args["strategy1_type"]
        self.days1 = args["days1"] if self.strat1 == "R" \
            else args["days1"] + 20
        self.strat2 = args["strategy2_type"]
        self.days2 = args["days2"] if self.strat2 == "R" \
            else args["days2"] + 20
        self.data = self.setup_data(args["tickers"])

    def determine_period(self, days: int) -> int:
        """Conservatively Determines which day to start fetching data

        Args:
            days: number indicated in --days parameter

        Returns:
            Number of trading days before --b to start fetching data from
        """
        # Depending on number of days, determine timing window
        return ceil(35 + (7 / 4 * days))


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
        # pick max days ensure sufficient data retrieved
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

        This implementation circumvents the possibility that
        each ticker might have different trading days. In addition,
        this also includes the month before the beginning date
        because we also need to collect data regarding the signals then

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

        # We now start collect signals from previous month
        data_begin_date = datetime(
            year = self.begin_date.year if self.begin_date.month != 1 else \
                self.begin_date.year - 1,
            month = 12 if self.begin_date.month == 1 else \
                self.begin_date.month - 1,
            day = 1
        )
        dates_np_filter = list(filter(lambda x:
            data_begin_date <= x <= self.end_date, dates_list
        ))
        # Check if stocks have the same time-frame
        if self.n_months is None:
            self.n_months = len(dates_np_filter)
        elif self.n_months != len(dates_np_filter):
            raise ValueError(f"{ticker} might not be trading in entire period")
        return dates_np_filter
