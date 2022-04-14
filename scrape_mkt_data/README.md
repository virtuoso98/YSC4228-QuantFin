# Assignment 2 - Scraping Market Data

This repository code is done by Walter and Zhao Yuan for the second assignment of Data Science in Quantitative Finance. In this task, we have decided to scrape market data using the yfinance package. This file was ran in python 3.10.2. In general,

```python
python get_prices.py --ticker <xxx> –-b <YYYYMMDD> –-e <YYYYMMDD> --initial_aum <xxxx>  --plot
```

There are a few things to take note here:

1. The ticker argument should be searchable in the total investable universe of equities on Yahoo finance
2. The start and end date should not be the same, start date should be earlier than end date, and both dates must be earlier than the present date
3. --initial_aum takes in a positive value with unit in USD
4. --e is an optional parameter. If there is no input for --e, then the present date at the time of running the program will be selected
5. --plot is an optional parameter. If --plot is used, the daily AUM will be plotted through the entire chosen time period.

An example argument would be

```python
python get_prices.py --ticker MSFT –-b 20200312 –-e 20210311 --initial_aum 10000 --plot
```

We expect to display the following:

1. Begin date (after adjusting for holidays, etc.)
2. End date (after adjusting for holidays, etc.)
3. Number of calendar days between
4. Total stock return (adjusted for dividends)
5. Total return (of the AUM invested)
6. Annualized rate of return (of the AUM invested) - Assume 250 trading days in a year
7. Initial AUM
8. Final AUM
9. Average AUM
10. Maximum AUM
11. PnL (of the AUM invested)
12. Average daily return of the portfolio (i.e., of the AUM invested)
13. Daily Standard deviation of the return of the portfolio
14. Daily Sharpe Ratio of the portfolio (assume a daily risk-free rate of 0.01%)

To run the unit tests, run `py.test` on the main directory.
