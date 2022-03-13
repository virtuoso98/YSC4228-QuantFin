"""Sub-module storing the Processor Class that Does Data Crunching"""

import pandas as pd
from tools.fetcher import Fetcher

class Processor(Fetcher):
    """Class that post-processes data from the Fetcher class.

    More specifically, this class takes the DataFrame generated
    from the Fetcher class, processes the data and generates
    the statistics which are specified in the print_information
    function. If the --plot argument is given, then this class
    also handles the generation of the graph.

    Attributes:
        initial_aum: Initial Assets Under Management
        is_plot: Boolean of whether graph should be generated
        TRADING_DAYS_PER_YEAR: Assumed to be 250
    """

    def __init__(self, args: dict):
        super().__init__(args)
        # AUM must be positive to be relevant
        if args["initial_aum"] <= 0:
            raise ValueError("Initial AUM should be Positive")
        self._initial_aum = args["initial_aum"]
        self._is_plot = args["plot"]
        # Assumption given in the question
        self.TRADING_DAYS_PER_YEAR = 250

    def generate_statistics(self) -> None:
        """Overall Function that calculates the relevant statistics

        Returns:
            While it is a void function, it generates important statistics
            that is subsequently printed by the print_statistics function.
            Furthermore, it also handles whether the graph should be
            generated based on the boolean is_plot attribute
        """
        # Stocks adjusted for dividend added for easier processing
        df = self._add_dividend_to_stock(self.fetch_data())

        # Retrieve number of days + start, end dates
        start_date = self._get_start_date_adjusted(df)
        end_date = self._get_end_date_adjusted(df)
        n_days = self._get_number_of_days(df)

        # Retrieve the stock returns adjusted for dividends
        stock_hist = df["Stocks_Close_Adjusted"]
        n_stocks_bought = float(self._initial_aum / stock_hist[0])
        # Rest of the statistics retrieved with atomic functions
        # So that each function can be easily edited
        adjusted_stock_returns = self._get_stock_returns(stock_hist)
        total_aum_returns = self._get_aum_returns(stock_hist)
        annual_aum_returns = self._get_annual_aum_returns(
            total_aum_returns, n_days
        )
        initial_aum = self._initial_aum
        final_aum = self._get_final_aum(total_aum_returns)
        average_aum = self._get_average_aum(stock_hist)
        max_aum = self._get_max_aum(stock_hist)
        pnl_aum = self._get_aum_pnl(initial_aum, final_aum)
        avg_daily_return_aum = self._get_average_daily_return(stock_hist)
        avg_daily_aum_sd = self._get_daily_aum_sd()
        daily_sharpe_ratio = self._get_daily_aum_sharpe_ratio()
        print(df)
        # Dictionary that is used for pretty-printing later
        statistics = {
            "Start Date:": start_date,
            "End Date: ": end_date,
            "Number of Trading Days:": n_days,
            "Total stock return (With Dividends):": adjusted_stock_returns,
            "Total returns of AUM:": total_aum_returns,
            "Annualized AUM returns:": annual_aum_returns,
            "Initial AUM:": initial_aum,
            "Final AUM:": final_aum,
            "Average AUM:": average_aum,
            "Maximum AUM:": max_aum,
            "PnL of AUM:": pnl_aum,
            "Average daily returns:": avg_daily_return_aum,
            "Daily Standard Deviation:": avg_daily_aum_sd,
            "Daily Sharpe Ratio": daily_sharpe_ratio
        }

        self.print_statistics(statistics)

    def print_statistics(self, statistics: dict):
        """Function that handles the printing of statistics.

        This function was made as a standalone so that

        Args:
            statistics: a dictionary of information type mapped
            to the data value.
        """
        # Line Separator to make print messages clearer
        line_separator = "---------------------------------------------------"
        print(line_separator)
        print(f"Printing market data for the ticker {self._ticker}")
        print(line_separator)
        # As a dictionary, one simply needs to print the key-value pair.
        for info, value in statistics.items():
            print(info, value)
        print(line_separator)

    def _get_start_date_adjusted(self, df: pd.DataFrame) -> str:
        """Getter for start date (Adjusted for Public Holidays, etc).

        Args:
            df: Dataframe of retrieved financial data

        Returns:
            String of the adjusted start date
        """
        start_date_numpy = df.index.values[0]
        start_date_datetime = pd.to_datetime(str(start_date_numpy))
        return start_date_datetime.strftime("%Y-%m-%d")

    def _get_end_date_adjusted(self, df: pd.DataFrame) -> str:
        """Getter for end date (Adjusted for Public Holidays, etc).

        Args:
            df: Dataframe of retrieved financial data

        Returns:
            String of the adjusted end date
        """
        end_date_numpy = df.index.values[-1]
        end_date_datetime = pd.to_datetime(str(end_date_numpy))
        return end_date_datetime.strftime("%Y-%m-%d")

    def _get_number_of_days(self, df: pd.DataFrame) -> int:
        """Getter for number of trading days in dataframe

        Args:
            df: Dataframe of retrieved financial data

        Returns:
            Integer showing number of trading days recorded
        """
        return df.shape[0]

    def _add_dividend_to_stock(self, df: pd.DataFrame) -> pd.DataFrame:
        """Adds column for stock adjusted for dividends to DataFrame

        This post-processing is done so that future calculations of the stock
        become more managable. We have assumed that all dividends are indeed
        re-invested into the same stock.

        Args:
            df: Dataframe of retrieved financial data

        Returns:
            Same Dataframe but with added column
        """
        df["Stocks_Close_Adjusted"] = (
            df["Close"] + df["Dividends"].cumsum()
        )
        return df

    def _get_stock_returns(self, stock_hist: pd.Series) -> float:
        """Getter for stock returns
        """
        stock_initial = stock_hist[0]
        stock_final = stock_hist[-1]
        stock_returns = (stock_final - stock_initial) / stock_initial
        return stock_returns.astype(float)

    def _get_aum_returns(self, stock_hist: pd.Series) -> float:
        """Getter for AUM returns.

        Because we allow fractional shares in our calculation,
        this function works in exactly the same way as
        _get_stock_returns

        Args:
        """
        return self._get_stock_returns(stock_hist)

    def _get_annual_aum_returns(
            self,
            stock_returns: float,
            n_days_held: int
        ) -> float:
        annual_stock_returns = (1 + stock_returns) ** \
            (self.TRADING_DAYS_PER_YEAR / n_days_held) - 1
        return self._initial_aum * annual_stock_returns

    def _get_final_aum(self, aum_returns: float) -> float:
        """Getter for final AUM

        Args:
            aum_returns: float decimal representing AUM returns
            over the period stated

        Returns:
            Final AUM amount
        """
        return self._initial_aum * (1 + aum_returns)

    def _get_average_aum(self, stock_hist: pd.Series) -> float:
        # Normalize stock history relative to day 1
        stock_hist_normalized: pd.Series = stock_hist / stock_hist[0]
        return stock_hist_normalized.mean() * self._initial_aum

    def _get_max_aum(self, stock_hist: pd.Series) -> float:
        stock_hist_normalized: pd.Series = stock_hist / stock_hist[0]
        return stock_hist_normalized.max() * self._initial_aum

    def _get_aum_pnl(self, initial_aum: float, final_aum: float) -> float:
        return final_aum - initial_aum

    def _get_average_daily_return(self, stock_hist) -> float:
        stock_hist_normalized: pd.Series = stock_hist / stock_hist[0]
        return stock_hist_normalized.mean()

    def _get_daily_aum_sd(self) -> float:
        pass

    def _get_daily_aum_sharpe_ratio(self) -> float:
        pass

    def _plot_graph(self) -> None:
        pass