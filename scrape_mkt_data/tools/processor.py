"""Sub-module storing the Processor Class that Does Data Crunching"""

import pandas as pd
import matplotlib.pyplot as plt
from tools.fetcher import Fetcher

class Processor(Fetcher):

    def __init__(self, args: dict):
        super().__init__(args)
        # Verify if initial aum is positive
        if args["initial_aum"] <= 0:
            raise ValueError("Initial AUM should be Positive")
        self._initial_aum = args["initial_aum"]
        self._is_plot = args["plot"]

    def process_dataframe(self, raw_df: pd.DataFrame):
        
        pass

    def compute_statistics(self):
        df = self.fetch_data()
        start_date = self._start_date
        end_date = self._end_date
        n_days = df.shape[0]
        print(df)


    def print_statistics(self):
        print(f"Statistics for the ticker {self._ticker}")

    def plot_graph(self):
        pass
