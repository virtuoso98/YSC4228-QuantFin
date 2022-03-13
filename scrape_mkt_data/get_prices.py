"""YSC4228 Data Science in Quantitative Finance

Authors: Koa Zhao Yuan, Walter Boo Keng Hua

This is the main file for the execution of the file to get prices.
"""

import argparse
from tools.processor import Processor

def process_inputs() -> dict:
    """Processes inputs from command line for further processing.

    Returns:
        Dictionary that maps parser command line arguments (key) to
        the parameters (values) inputted by the user.
    """
    # Relevant Command Line Arguments
    parser = argparse.ArgumentParser(
        prog = "get_prices",
        description= "Get Stocks Price data using yfinance API"
    )
    parser.add_argument("--ticker",
        type = str,
        required = True,
        help = "Ticker for Scraper to track"
    )
    parser.add_argument("--b",
        required = True,
        type = str,
        help = "Date to start tracking the ticker (YYYYMMDD)"
    )
    parser.add_argument("--e",
        required = False,
        type = str,
        help = "Date to stop tracking the ticker (YYYYMMDD)"
    )
    parser.add_argument("--initial_aum",
        required = True,
        type = int,
        help = "Initial Assets Under Management, expressed in dollars"
    )
    parser.add_argument("--plot",
        required = False,
        action = "store_true",
        help = "Optional Flag that decides whether to plot graph"
    )
    return vars(parser.parse_args())

def execute():
    """Overall function which runs the whole algorithm."""
    args = process_inputs()
    processor = Processor(args)
    processor.generate_statistics()

if __name__ == '__main__':
    execute()
