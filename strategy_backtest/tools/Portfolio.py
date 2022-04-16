"""This is a class that is separate from Strategizer and Fetcher.
This is because Portfolio serves mainly as a calculator and
displayer of relevant statistics. However, it isn't a specific
instance of Fetcher or Strategizer, which is why this is a class
in itself.
"""

import pandas as pd
from tools.Strategizer import Strategizer

class Portfolio(Strategizer):
    def __init__(self, args: dict) -> None:
        super().__init__(args)
        self.info_map = {}

    def print_stats(self) -> None:
        start = self.get_start_date()
        end = self.get_end_date()
        n_calender_days = self.get_calender_days(start, end)
        total_stock_return = self.get_stock_return()
        total_aum_return = self.get_stock_return()

    def get_start_date(self) -> pd.Timestamp:
        """Returns first trading day for portfolio"""
        return self.daily_aum_hist.index[0]

    def get_end_date(self) -> pd.Timestamp:
        """Returns first trading day for portfolio"""
        return self.daily_aum_hist.index[-1]

    def get_calender_days(self, end: pd.Timestamp, start: pd.Timestamp) -> int:
        """Returns time difference between 2 periods as integer number of days"""
        return (end - start).days

    def get_stock_return(self) -> float:
        pass

    def plot_graph(self):
        pass

