from math import ceil
import pandas as pd
from tools.Fetcher import Fetcher

class Strategizer(Fetcher):
    def __init__(self, args: dict) -> None:
        super().__init__(args)
        self.init_aum = args["initial_aum"]
        self.n_top_tickers = self.find_n_top_tickers(args)
        self.cul_info_coef = None
        self.aum_hist = None

    def find_n_top_tickers(self, args: dict) -> int:
        """Find number of top tickers to invest on"""
        return ceil(args["top_pct"] / 100 * len(args["tickers"]))

    def strategize(self):
        monthly_ic = pd.Series()
        daily_aum = []
        top_tickers = None
        for i in range(self.n_months):
            if i != 0:
                self.track_aum(top_tickers, daily_aum)
                self.evaluate_ic(top_tickers, monthly_ic)
            top_tickers = self.find_top_tickers(i)

    def find_top_tickers(self, month):
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

    def track_aum(self, top_tickers: "list", daily_aum: pd.Series) -> None:
        pass

    def evaluate_ic(self, top_tickers: "list", daily_aum: pd.Series) -> None:
        pass
