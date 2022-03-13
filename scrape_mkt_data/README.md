# Assignment 2 - Scraping Market Data

This repository code that is done by Walter and Zhao Yuan for the second assignment of Data Science in Quantitative Finance. In this task, we have decided to scrape market data using the yfinance package. In general,

```
get_prices.py --ticker <xxx> –-b <YYYYMMDD> –-e <YYYYMMDD> --initial_aum <xxxx>  --plot
```

There are a few things to take note here:
1. The ticker argument should be searchable in the total investable universe of equities on Yahoo finance
2. The beginning and end date should not be the same and both dates cannot be later than the present date

An example argument would be

```
get_prices.py --ticker MSFT –-b 20200312 –-e 20210311 --initial_aum 10000  --plot
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

If --plot is used, the daily AUM will be plotted through the entire chosen time period.