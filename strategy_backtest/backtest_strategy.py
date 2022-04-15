from datetime import datetime, timedelta
import argparse

from tools.Fetcher import Fetcher

def process_inputs() -> dict:
    '''Processes inputs from command line for further processing'''
    parser = argparse.ArgumentParser(
        prog = 'backtest_strategy',
        description = 'Test simple Momentum and Reversal monthly strategies'
    )
    parser.add_argument(
        '--tickers', '--list', nargs = '+',
        help = '<REQUIRED> List of Tickers to track',
        required = True
    )
    parser.add_argument("--b",
        required = True, type = str,
        help = "<REQUIRED> Start Date to track (YYYYMMDD)"
    )
    parser.add_argument("--e",
        required = False, type = str,
        help = "<OPTIONAL> Stop Date to Track (YYYYMMDD). Default: today's date"
    )
    parser.add_argument("--initial_aum",
        required = True, type = int,
        help = "Initial Assets Under Management, expressed in US dollars"
    )
    parser.add_argument("--strategy_type",
        required = True, type = str,
        help = "Investing Strategy to use. Input 'R' for Reversal and 'M' for Momentum."
    )
    parser.add_argument("--days",
        required = True, type = int,
        help = "Number of trading days used to compute strategy-related returns"
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
    """Check for validity of arguments"""
    if args["days"] > 250:
        raise ValueError("--days: Trading Days Exceed 250.")
    if args["days"] < 1:
        raise ValueError("--days: Trading days Param must be positive.")
    if args["top_pct"] < 1 or args["top_pct"] > 100:
        raise ValueError("--top_pct: Percentile must be between 1 and 100.")
    if args["strategy_type"] not in ["R", "M"]:
        raise ValueError("--strategy_type: Only 'R'(Reversal) or 'M'(Momentum)")
    if args["initial_aum"] <= 0:
        raise ValueError("Initial AUM must be positive")
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
        raise ValueError("Start Date is later than Start Date")

    # Update Args so that it is easier to initialize class
    args["b"] = start_date_DT
    args["e"] = end_date_DT
    return args


def execute():
    '''Overall function that executes backtest strategy.'''
    args = process_inputs()
    fetcher = Fetcher(args)

if __name__ == '__main__':
    execute()
