import argparse
from multiprocessing.sharedctypes import Value

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
        check_validity(dict_args)
        return dict_args
    except ValueError as e:
        raise e


def check_validity(args: dict) -> None:
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




def execute():
    '''Overall function that executes backtest strategy.'''
    args = process_inputs()
    print(args)

if __name__ == '__main__':
    execute()
