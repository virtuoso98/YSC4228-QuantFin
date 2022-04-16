"""This module contains the class Portfolio, that is supposed to
Consolidate the portfolio data we have and present some statistics.
Since many of the methods used here are atomic, I have shaved the
documnetation to occupy minimal space and minimize clutter
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tools.Strategizer import Strategizer

class Portfolio(Strategizer):
    """Class that computes the relevant statistics of the portfolio.

    Attributes:
        YEAR_TO_TRADING_DAYS: constant set at 250.
    """
    def __init__(self, args: dict) -> None:
        super().__init__(args)
        self.YEAR_TO_TRADING_DAYS = 250

    def print_stats(self) -> None:
        start = self.get_start_date()
        end = self.get_end_date()
        # Not sure about total stock returns, but i'm assuming
        # it's the same as AUM returns
        total_stock_return = self.get_aum_return()
        total_aum_return = self.get_aum_return()
        init_aum = self.get_init_aum()
        final_aum = self.get_final_aum()
        avg_daily_aum_return = self.get_avg_daily_aum_return(total_aum_return)
        daily_sd_aum = self.get_sd_daily_aum()

        statistics = [
            ("1. Begin Date:", start),
            ("2. End Date:", end),
            ("3. Number of Calender days:", self.get_calender_days(end, start)),
            ("4. Total Stock Return:", total_stock_return),
            ("5. Total AUM Return:", total_aum_return),
            ("6. Annualized RoR:", self.get_annualized_ror(total_aum_return)),
            ("7. Initial AUM:", init_aum),
            ("8. Final AUM:", final_aum),
            ("9. Average daily AUM:", self.get_avg_daily_aum()),
            ("10. Maximum daily AUM:", self.get_max_daily_aum()),
            ("11. PnL of AUM Invested:", self.get_pnl_aum(init_aum, final_aum)),
            ("12. Average daily AUM return:", avg_daily_aum_return),
            ("13. Daily S.D of portfolio returns:", daily_sd_aum),
            ("14. Daily Sharpe Ratio of portfolio", \
                self.get_daily_sharpe_ratio(daily_sd_aum, avg_daily_aum_return))
        ]
        print(self.LINE_SEPARATOR)
        print("Relevant Information of AUM over time:")
        for category, number in statistics:
            print(category, number)

    def get_start_date(self) -> pd.Timestamp:
        """Returns first trading day for portfolio"""
        return self.daily_aum_hist.index[0]

    def get_end_date(self) -> pd.Timestamp:
        """Returns first trading day for portfolio"""
        return self.daily_aum_hist.index[-1]

    def get_calender_days(self, end: pd.Timestamp, start: pd.Timestamp) -> int:
        """Returns time difference between 2 periods in number of days"""
        return (end - start).days

    def get_aum_return(self) -> float:
        """Returns total AUM returns over the period"""
        init_aum = self.daily_aum_hist[0]
        final_aum = self.daily_aum_hist[-1]
        return (final_aum - init_aum) / init_aum

    def get_annualized_ror(self, total_aum_return: np.float64) -> np.float64:
        """Returns Annualized RoR of AUM invested"""
        years = self.daily_aum_hist.size / self.YEAR_TO_TRADING_DAYS
        a_ror = (total_aum_return + 1) ** (1 / years) - 1
        return a_ror

    def get_init_aum(self) -> np.float64:
        """Returns Initial AUM (Same as inputted parameter)"""
        return self.daily_aum_hist[0]

    def get_final_aum(self) -> np.float64:
        """Returns Final AUM over the period"""
        return self.daily_aum_hist[-1]

    def get_avg_daily_aum(self) -> np.float64:
        """Returns average daily AUM over the period"""
        return self.daily_aum_hist.mean()

    def get_max_daily_aum(self) -> np.float64:
        """Returns maximum AUM over the period"""
        return self.daily_aum_hist.max()

    def get_pnl_aum(self,
        init_aum: np.float64,
        final_aum: np.float64) -> np.float64:
        """Returns AUM PnL over the period"""
        return final_aum - init_aum

    def get_avg_daily_aum_return(self,
        total_aum_return: np.float64) -> np.float64:
        """Returns average daily return of stock"""
        return total_aum_return / self.daily_aum_hist.size

    def get_sd_daily_aum(self) -> np.float64:
        """Returns daily AUM standard deviation over the period"""
        aum_copy = self.daily_aum_hist.copy()
        pct_change = aum_copy.pct_change().dropna()
        return pct_change.std()

    def get_daily_sharpe_ratio(
        self, daily_aum_sd: np.float64,
        avg_daily_aum_return: np.float64,
        risk_free: np.float64 = np.float64(0.0001)) -> np.float64:
        """Returns daily AUM Sharpe ratio over the period"""
        return (avg_daily_aum_return - risk_free) / daily_aum_sd

    def plot_graph(self):
        cul_info_coef = self.cul_info_coef.copy()
        daily_aum_hist = self.daily_aum_hist.copy()

