"""Module containing the Strategizer class, which takes data
taken from the Fetcher class and applies either the Reversal
or Momentum Strategy to invest. This class also calculates the
monthly IC, which is then converted to culminative IC.
"""

from math import ceil
from functools import reduce
import pandas as pd
from tools.Fetcher import Fetcher

class Strategizer(Fetcher):
    """Class that performs reversal/ momentum strategy and calcualtes IC

    This class performs the nitty gritty data processing, whose results
    are passed over to the portfolio class for printing and computing
    of relevant statistics.

    Attributes:
        curr_aum: current assets under management, based on month measured
        n_top_tickers: number of top tickers to allocate AUM to
        cul_info_coef: Culminative information coefficient
        daily_aum_hist: Daily AUM history of stocks
    """
    def __init__(self, args: dict) -> None:
        super().__init__(args)
        self.curr_aum = args["initial_aum"]
        self.n_top_tickers = self.find_n_top_tickers(args)
        self.cul_info_coef: pd.Series= None
        self.daily_aum_hist: pd.Series = None

    def find_n_top_tickers(self, args: dict) -> int:
        """Find number of top tickers to invest on, based on strategy

        Args:
            args: input arguments in the command line

        Returns:
            Number of top tickers to allocate AUM on
        """
        return ceil(args["top_pct"] / 100 * len(args["tickers"]))

    def strategize(self) -> None:
        """Overall Function that performs the strategizing"""
        # Raw AUM and IC, later converted to Pandas Series
        monthly_ic = {}
        daily_aum = []
        top_tickers_hist = []

        # Specifying which strategy to use
        strat = 'Reversal' if self.strat == 'R' else 'Momentum'
        print(f"Executing {strat} strategy")
        for i in range(self.n_months):
            top_tickers_hist.append(self.find_top_tickers(i))
            # Only evaluate first set of tickers 1 month after allocating
            if i != 0:
                self.track_aum(top_tickers_hist, daily_aum, monthly_ic)
        print("Infomation coefficient and daily AUM change recorded.")
        print("Tidying up IC and AUM Data.")

        # Cuminative information coefficient, so we take cumsum
        self.cul_info_coef = pd.Series(monthly_ic).cumsum()
        self.daily_aum_hist = \
            pd.concat(daily_aum).drop_duplicates(keep = "first")

    def find_top_tickers(self, month: int) -> "list[dict]":
        """Finds the top tickers based on strategy to allocate AUM to

        Params:
            month: the nth-time (in terms of month) for portfolio reallocation.

        Returns:
            List of dictionaries of tickers to invest with relevant data
        """
        monthly_returns = []
        for ticker, data in self.data.items():
            # Get indexes for start and end date
            end_window = data["last_days"][month]
            end_idx = data["df"].index.get_loc(end_window)
            start_idx = end_idx - self.days
            start_window = data["df"].index[start_idx]

            # Get Returns then append to array
            start_price = data["df"].at[start_window, "Close_Adjusted"]
            end_price = data["df"].at[end_window, "Close_Adjusted"]
            returns = (end_price - start_price) / start_price
            monthly_returns.append({
                "ticker": ticker,
                "returns": returns,
                "start": start_window,
                "end": end_window
            })

        # Whether to take firms with lowest/ highest returns
        is_descending = self.strat == 'R'

        # Filter based on returns, and take the top n tickers
        sorted_returns = sorted(monthly_returns,
            key = lambda x: x["returns"],
            reverse = is_descending
        )
        return sorted_returns[:self.n_top_tickers]

    def track_aum(self,
        top_tickers_hist: "list[list]",
        daily_aum: pd.Series,
        monthly_ic: dict) -> None:
        """

        Args:
            top_tickers_hist:
            daily_aum:
            monthly_ic:
        """
        # Assume all tickers have have last trading day of month
        end: pd.Timestamp = top_tickers_hist[-1][0]["end"]
        # Start of the last month to track from
        start: pd.Timestamp = top_tickers_hist[-2][0]["end"]
        asset_per_ticker = self.curr_aum / self.n_top_tickers
        aum_by_ticker = []
        # Take second last entry because that's the entry to track
        for packet in top_tickers_hist[-2]:
            ticker_df = self.data[packet["ticker"]]["df"]
            filter_df = ticker_df.loc[start:end, "Close_Adjusted"]
            # find AUM change for the asset
            aum_change = filter_df / filter_df[0] * asset_per_ticker
            aum_by_ticker.append(aum_change)

        # Pointwise addition of series in an array
        gross_aum_change = reduce(lambda a, b: a + b, aum_by_ticker)
        daily_aum.append(gross_aum_change)

        # Current AUM should be updated to the last trading day
        self.curr_aum = gross_aum_change[-1]
        self.evaluate_ic(aum_by_ticker, end, monthly_ic)


    def evaluate_ic(self,
        aum_by_ticker: "list",
        day: pd.Timestamp,
        monthly_ic: dict) -> None:
        """Calculates Information coefficient for the given month

        Args:
            aum_by_ticker:
            day:
            monthly_ic:

        Returns:
            

        """
        n_increase = 0
        for ticker_df in aum_by_ticker:
            n_increase += 1 if ticker_df[-1] > ticker_df[0] else 0

        ic = (n_increase / self.n_top_tickers * 2) - 1
        monthly_ic[day] = ic
