"""This is a class that is separate from Strategizer and Fetcher.
This is because Portfolio serves mainly as a calculator and
displayer of relevant statistics. However, it isn't a specific
instance of Fetcher or Strategizer, which is why this is a class
in itself.
"""

import pandas as pd

class Portfolio():
    def __init__(self, cul_ic: pd.Series, daily_aum: pd.Series) -> None:
        self.cul_ic = cul_ic
        self.daily_aum = daily_aum

    def print_stats(self) -> None:
        print(self.begin_date)

    def plot_graph(self) -> None:
        pass