from datetime import datetime, timedelta
import argparse
from tools.Strategizer import Strategizer

def process_inputs() -> dict:
    parser = argparse.ArgumentParser(
        prog = "backtest_two_signal_strategy",
        description = "Test Strategy of linear combination of 2 signals"
    )
    parser.add_argument(
        "--tickers", "--list", nargs = "+",
        help = "<REQUIRED> List of Tickers to track",
        required = True
    )
    parser.add_argument("--b",
        required = True, type = str,
        help = "Start Date to track (YYYYMMDD)"
    )
    parser.add_argument("--e",
        required = False, type = str,
        help = "Stop Date to Track (YYYYMMDD). Default: today's date"
    )
    parser.add_argument("--initial_aum",
        required = True, type = int,
        help = "Initial Assets Under Management, expressed in US dollars"
    )
    parser.add_argument("--strategy1_type",
        required = True, type = str,
        help = "First Strategy: Input 'R' for Reversal and 'M' for Momentum."
    )
    parser.add_argument("--days1",
        required = True, type = int,
        help = "Number of trading days used to compute First Strategy returns"
    )
    parser.add_argument("--strategy2_type",
        required = True, type = str,
        help = "Second Strategy: Input 'R' for Reversal and 'M' for Momentum."
    )
    parser.add_argument("--days2",
        required = True, type = int,
        help = "Number of trading days used to compute Second Strategy returns"
    )
    parser.add_argument("--top_pct",
        required = True, type = int,
        help = "Indicates the percentage of stocks to go long (Rounded up)"
    )

    # Check for Argument Validity before returning
    dict_args = vars(parser.parse_args())
    try:
        valid_args = check_validity(dict_args)
        return valid_args
    except ValueError as e:
        raise e


def check_validity(args: dict) -> dict:
    # Check for Simpler arguments first before more complex ones
    if args["initial_aum"] <= 0:
        raise ValueError("--initial_aum: Initial AUM must be positive")
    if args["top_pct"] < 1 or args["top_pct"] > 100:
        raise ValueError("--top_pct: Percentile must be between 1 and 100.")

    # for-loop to make days checking more compact
    for days in ["days1", "days2"]:
        if args[days] > 250:
            raise ValueError(f"--{days}: Trading Days Exceed 250.")
        if args[days] < 1:
            raise ValueError(f"--{days}: Trading days Param must be positive.")

    # for-loop to make strategy checking more compact
    for strat in ["strategy1_type", "strategy2_type"]:
        if args[strat] not in ["R", "M"]:
            raise ValueError(f"--{strat}: Only 'R'(Reversal) or 'M'(Momentum)")

    # Check for DateTime validity
    start_date_DT = datetime.strptime(args["b"], "%Y%m%d")

    end_date_DT = datetime.strptime(args["e"], "%Y%m%d") \
        if args["e"] is not None else datetime.now()

    # Compensate for yfinance bug, where the given API
    # Tracks until 1 day before end
    end_date_DT += timedelta(days = 1)

    # Start date cannot be later than current date
    if start_date_DT > datetime.now():
        raise ValueError("Start date cannot be after current time")

    # Start date cannot be later than end date
    if start_date_DT > end_date_DT:
        raise ValueError("Start Date is later than End Date")

    # Start date cannot be at same month and year as end
    # this is because positions are taken at the end of month
    if start_date_DT.year == end_date_DT.year and \
        start_date_DT.month == end_date_DT.month:
        # pylint: disable=line-too-long
        raise ValueError("Position taken at last trading day of start date month. Please select end date at least 1 month after start date")

    # Update Args so that it is easier to initialize class
    args["b"] = start_date_DT
    args["e"] = end_date_DT
    return args

def execute():
    """Overall function that executes backtest strategy."""
    args = process_inputs()
    strategizer = Strategizer(args)

if __name__ == "__main__":
    execute()
