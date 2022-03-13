"""Sub-module storing the Processor Class that Does Data Crunching"""

import pandas as pd
from tools.fetcher import Fetcher

class Processor(Fetcher):

    def __init__(self, args: dict):
        super().__init__(args)
        # Verify if initial aum is positive
        if args["initial_aum"] <= 0:
            raise ValueError("Initial AUM should be Positive")
        self._initial_aum = args["initial_aum"]
        self._is_plot = args["plot"]
        self.TRADING_DAYS_PER_YEAR = 250

    def compute_statistics(self):
        df = self._add_dividend_to_stock(self.fetch_data())
        start_date = self._get_start_date_adjusted(df)
        end_date = self._get_end_date_adjusted(df)
        n_days = self._get_number_of_days(df)

        # Retrieve the Stock History
        stock_hist = df["Stocks_Close_Adjusted"]
        adjusted_stock_returns = self._get_stock_returns(stock_hist)
        aum_returns = self._get_aum_returns(
            adjusted_stock_returns
        )
        annual_aum_returns = self._get_annual_aum_returns(
            adjusted_stock_returns, n_days
        )

        initial_aum = self._initial_aum
        final_aum = self._get_final_aum(aum_returns)
        average_aum = self._get_average_aum()

        return {
            "Start Date: ": start_date,
            "End Date: ": end_date,
            "Number of Trading Days: ": n_days,
            "Total stock return (With Dividends): ": adjusted_stock_returns,
            "Total AUM returns: ": aum_returns
        }

    def print_information(self):
        pass

    def _get_start_date_adjusted(self, df: pd.DataFrame) -> str:
        start_date_numpy = df.index.values[0]
        start_date_datetime = pd.to_datetime(str(start_date_numpy))
        return start_date_datetime.strftime("%Y-%m-%d")

    def _get_end_date_adjusted(self, df: pd.DataFrame) -> str:
        end_date_numpy = df.index.values[-1]
        end_date_datetime = pd.to_datetime(str(end_date_numpy))
        return end_date_datetime.strftime("%Y-%m-%d")

    def _get_number_of_days(self, df: pd.DataFrame) -> int:
        return df.shape[0]

    def _add_dividend_to_stock(self, df: pd.DataFrame) -> pd.DataFrame:
        df["Stocks_Close_Adjusted"] = (
            df["Close"] + df["Dividends"].cumsum()
        )
        return df

    def _get_stock_returns(self, stock_hist: pd.Series) -> float:
        stock_initial = stock_hist[0]
        stock_final = stock_hist[-1]
        stock_returns = (stock_final - stock_initial) / stock_initial
        return stock_returns.astype(float)

    def _get_aum_returns(self, stock_returns: float) -> float:
        return self._initial_aum * stock_returns

    def _get_annual_aum_returns(
            self,
            stock_returns: float,
            n_days_held: int
        ) -> float:
        annual_stock_returns = (1 + stock_returns) ** (250 / n_days_held) - 1
        return self._initial_aum * annual_stock_returns

    def _get_final_aum(self, aum_returns: float) -> float:
        return self._initial_aum * aum_returns

    def _get_average_aum(self, stock_hist: pd.Series) -> float:
        pass

    def _get_max_aum(self, stock_hist: pd.Series) -> float:
        pass