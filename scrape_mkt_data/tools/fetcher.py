from datetime import datetime, timedelta
import yfinance as yf

class Fetcher:
    def __init__(self, args):
        fetcher_args = self._check_fetcher_validity(args)
        self._ticker = fetcher_args["ticker"]
        self._start_date = fetcher_args["start_date"]
        self._end_date = fetcher_args["end_date"]
        self.data = None

    def _check_fetcher_validity(self, args: dict) -> dict:
        # Check for possible ticker errors
        ticker = args["ticker"]
        if len(ticker) != 4:
            raise ValueError("Ticker should have 4 Characters")
        if not ticker.isalpha():
            raise ValueError("Ticker should only consist of letters")

        # Datetime automatically checks for datetime argument errors
        # yfinance tracks 1 day before start, 1 day before end
        start_date = datetime.strptime(args["b"], "%Y%m%d") + timedelta(days = 1)
        end_date = datetime.strptime(args["e"], "%Y%m%d") + timedelta(days = 1) \
            if args["e"] is not None else datetime.now()

        if start_date > end_date:
            raise ValueError("End Date is earlier than Start Date")

        fetcher_args = {
            "ticker": ticker,
            "start_date": start_date,
            "end_date": end_date
        }
        return fetcher_args


    def get_data(self) -> None:
        tracker = yf.Ticker("MSFT")
        self.data = tracker.history(
            start = self._start_date,
            end = self._end_date
        )
        print(self.data)
