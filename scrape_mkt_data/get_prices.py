"""Authors: Zhao Yuan, Walter"""

import argparse
from tools.processor import Processor

def process_inputs():
    parser = argparse.ArgumentParser(
        prog = "get_prices",
        description= "Get Stocks Price data using yfinance API"
    )
    parser.add_argument("--ticker",
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
    args = process_inputs()
    processor = Processor(args)
    processor.get_data()

if __name__ == '__main__':
    execute()
