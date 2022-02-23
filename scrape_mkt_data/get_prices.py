import argparse

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
        type = int,
        help = "Date to start tracking the ticker"
    )
    parser.add_argument("--e",
        required = True,
        type = int,
        help = "Date to stop tracking the ticker"
    )
    parser.add_argument("--initial_aum",
        required = True,
        type = int,
        help = "Initial Assets Under Management, expressed in dollars"
    )
    parser.add_argument("--plot",
        required = False,
        action = "store_true",
        help = "Optional Flag that decides whether to plot the graph or not"
    )

    return vars(parser.parse_args())

def execute():
    args = process_inputs()
    print(args)

if __name__ == '__main__':
    execute()
