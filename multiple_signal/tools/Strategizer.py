"""Module containing the Strategizer class, which takes data
taken from the Fetcher class and applies either the Reversal
or Momentum Strategy to invest. This class also calculates the
monthly IC, which is then converted to culminative IC.
"""

from datetime import datetime
from math import ceil
from functools import reduce
from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np
from tools.fetcher import Fetcher

class Strategizer(Fetcher):
    """Class that performs reversal/ momentum strategy and calcualtes IC

    This class performs the nitty gritty data processing, whose results
    are passed over to the portfolio class for printing and computing
    of relevant statistics.

    Attributes:
        curr_aum: current assets under management, based on month
        n_top_tickers: number of top tickers to allocate AUM to
        cul_info_coef: Culminative information coefficient
        daily_aum_hist: Daily AUM history of stocks
        sk_ols: scikit-learn ordinary-least-squares variable
        x_train: 2 column (x1, x2) feature matrix for linear regression
        y_train: 1 column (y) target matrix used for linear regression
        model_stats: string array of model statistics
    """
    def __init__(self, args: dict) -> None:
        super().__init__(args)
        self.curr_aum = args["initial_aum"]
        self.n_top_tickers = self.find_n_top_tickers(args)
        self.cul_info_coef: pd.Series = None
        self.daily_aum_hist: pd.Series = None
        self.sk_ols = LinearRegression()
        self.x_train = np.empty((0, 2))
        self.y_train = np.empty((0, 1))
        self.model_stats = []

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

        # Specifying print message for clarity
        strat1 = "Reversal" if self.strat1 == "R" else "Momentum"
        strat2 = "Reversal" if self.strat2 == "R" else "Momentum"
        print(self.LINE_SEPARATOR)
        print("Executing Multiple Signal Strategy Consisting of:")
        print(f"Strategy 1: {strat1}, Period: {self.days1} days")
        print(f"Strategy 2: {strat2}, Period: {self.days2} days")

        # overall for-loop running regression and picking top n tickers
        for i in range(1, self.n_months):
            self.fit_model(i)
            top_tickers_hist.append(self.find_top_tickers(i))
            # Don't track AUM for the first prediction
            if i != 1:
                self.track_aum(top_tickers_hist, daily_aum, monthly_ic)

        print("Infomation coefficient and daily AUM change recorded.")
        print("Tidying up IC and AUM Data.")
        print(self.LINE_SEPARATOR)
        self.cul_info_coef = pd.Series(monthly_ic).cumsum()
        self.daily_aum_hist = pd.concat(daily_aum)
        self.daily_aum_hist = \
            pd.concat(daily_aum).drop_duplicates(keep = "first")

    def get_monthly_model_stats(self, date: datetime) -> None:
        """Gets coefficients and t-statistic for linear regression model

        Args:
            date: last day of the month in question
        """
        # Solution taken from stackoverflow to calculate t-statistic:
        # https://stackoverflow.com/questions/27928275/find-p-value-significance-in-scikit-learn-linearregression
        # Standard Square Errors
        sse = np.sum(
            (self.sk_ols.predict(self.x_train) - self.y_train) ** 2, axis = 0)\
            / float(self.x_train.shape[0] - self.x_train.shape[1])
        # Calculate standard errors
        se = np.array([
            np.sqrt(np.diagonal(sse[i] * np.linalg.inv(
                np.dot(self.x_train.T, self.x_train)))) \
                    for i in range(sse.shape[0])]
                )

        # Retrieve relevant params
        tstats = (self.sk_ols.coef_ / se)[0]
        params = self.sk_ols.coef_[0]
        strat1 = "Reversal" if self.strat1 == "R" else "Momentum"
        strat2 = "Reversal" if self.strat2 == "R" else "Momentum"

        # Generate in a list for easy reduction
        monthly_model_stats_list = [
            f"Date Generated: {date}",
            f"x1 ({strat1} Strat) Coefficient: {params[0]}",
            f"x1 ({strat1} Strat) t-value: {tstats[0]}",
            f"x2 ({strat2} Strat) Coefficient: {params[1]}",
            f"x2 ({strat2} Strat) t-value: {tstats[1]}",
        ]

        # reduce to form a nicely packed string of data
        monthly_model_stats_str = reduce(
            lambda a, b: f"{a}\n{b}", monthly_model_stats_list
        )
        self.model_stats.append(monthly_model_stats_str)


    def fit_model(self, mth_idx: int) -> None:
        """Fits linear regression model of the 2 signals with monthly returns

        More specifically, for a given month, this function fits
        the 2 strategy based coefficients using the signal-returns taken
        from the previous month and the monthly return of the current month.

        Args:
            mth_idx: index in the last dates of month array
        """
        for _, data in self.data.items():
            # retrieve relevant data
            prev_month = data["last_days"][mth_idx - 1]
            curr_month = data["last_days"][mth_idx]
            # Get relevant data
            prev_month_idx = data["df"].index.get_loc(prev_month)
            strat1_start_idx = prev_month_idx - self.days1
            strat1_start_window = data["df"].index[strat1_start_idx]
            strat2_start_idx = prev_month_idx - self.days2
            strat2_start_window = data["df"].index[strat2_start_idx]

            # retrieve price data
            strat1_start_px = data["df"].at[
                strat1_start_window, "Close_Adjusted"
            ]
            strat2_start_px = data["df"].at[
                strat2_start_window, "Close_Adjusted"
            ]
            prev_month_last_px = data["df"].at[
                prev_month, "Close_Adjusted"
            ]
            curr_month_last_px = data["df"].at[
                curr_month, "Close_Adjusted"
            ]

            # Calculate returns
            strat1_returns = (prev_month_last_px - strat1_start_px) \
                / strat1_start_px
            strat2_returns = (prev_month_last_px - strat2_start_px) \
                / strat2_start_px
            month_returns = (curr_month_last_px - prev_month_last_px) \
                / prev_month_last_px

            # Add data to array to prepare for linear regression
            # Multiply -1 if reversal strategy to favour lower signal returns
            x_data = np.array([
                -strat1_returns if self.strat1 == "R" else strat1_returns,
                -strat2_returns if self.strat2 == "R" else strat2_returns
            ])
            y_data = np.array([month_returns])
            self.x_train = np.vstack((self.x_train, x_data))
            self.y_train = np.vstack((self.y_train, y_data))

        # After data points for all tickers obtained, fit model
        self.sk_ols.fit(self.x_train, self.y_train)
        self.get_monthly_model_stats(curr_month)


    def find_top_tickers(self, month: int) -> "list[dict]":
        """Finds the top tickers based on strategy to allocate AUM to
        Params:
            month: the nth-time (in terms of month) for portfolio reallocation.
        Returns:
            List of dictionaries of tickers to invest with relevant data
        """
        monthly_returns = []
        for ticker, data in self.data.items():
            # Get end price first
            end_window = data["last_days"][month]
            end_idx = data["df"].index.get_loc(end_window)
            end_price = data["df"].at[end_window, "Close_Adjusted"]

            # Get signal based returns for strategy1
            strat1_start_idx = end_idx - self.days1
            strat1_start_window = data["df"].index[strat1_start_idx]
            strat1_start_price = data["df"].at[strat1_start_window, \
                "Close_Adjusted"]
            strat1_returns = (end_price - strat1_start_price) \
                / strat1_start_price

            # Get signal based returns for strategy2
            strat2_start_idx = end_idx - self.days2
            strat2_start_window = data["df"].index[strat2_start_idx]
            strat2_start_price = data["df"].at[strat2_start_window, \
                "Close_Adjusted"]
            strat2_returns = (end_price - strat2_start_price) \
                / strat2_start_price

            # Extract model score
            model_score = self.sk_ols.predict(
                np.array([[strat1_returns, strat2_returns]])
            )[0][0]

            monthly_returns.append({
                "ticker": ticker,
                "score": model_score,
                "end": end_window
            })

        sorted_returns = sorted(monthly_returns,
            key = lambda x: x["score"],
        )

        return sorted_returns[:self.n_top_tickers]

    def track_aum(self,
        top_tickers_hist: "list[list[dict]]",
        daily_aum: "list[pd.Series]",
        monthly_ic: dict) -> None:
        """Tracks the AUM change (and IC) of the selected top tickers

        Args:
            top_tickers_hist: History of top tickers chosen
            daily_aum: Daily AUM, as a list of pandas series
            monthly_ic: Monthly IC, as a dictionary
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

        However, IC is passed unto the parameter monthly_ic by reference,
        so this function is a void function (returns None)

        Args:
            aum_by_ticker: AUM of the ticker in the given month
            day: The last day of the month that maps to the IC
            monthly_ic: dictionary, with date as keys, IC as values
        """
        n_increase = 0
        for ticker_df in aum_by_ticker:
            n_increase += 1 if ticker_df[-1] > ticker_df[0] else 0

        ic = (n_increase / self.n_top_tickers * 2) - 1
        monthly_ic[day] = ic
