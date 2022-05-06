# Assignment 4 - Backtesting Multiple-Signal Strategy

This repository is done by Walter and Zhao Yuan for the last assignment for Data Science in Quantitative Finance. In this assignment, we are required to backtest Multiple-Signal Strategies. In other words, we are to test a linear combination of reversal and momentum based strategies with their respective time periods. Afterwards, we are to print the information coefficient and how our assets under management fared. To run this repository, you may run this commnad on the root directory of this directory to start.

```python
python .\backtest_two_signal_strategy.py --tickers MSFT,AAPL,TSLA,FB,NFLX,IBM,PFE,GILD,MRNA,XOM,CVX,BAC,JPM,NOV,WMT,SE,MCD,DIS,WBD,NKE --b 20200402 --e 20201204 --initial_aum 20000 --strategy1_type M --days1 20 --strategy2_type R --days2 50 --top_pct 20
```

The parameters are explained below:

- **--tickers** : A list of comma-separated tickers you'd like to track.
- **--b** : Beginning date of the period to start rebalancing the portfolio. Note that positions are always taken at the end of the month.
- **--e** : End date of the period. If this parameter is not provided, then it set set to today's date by default.
- **--initial_aum** : Initial assets under management, expressed in terms of USD
- **--strategy1_type** : First Strategy to execute. Input **R** for reversal and **M** for momentum.
- **--days1** : Number of days to compute first strategy-related returns. For the momentum strategy, an additional 20 trading-day gap is added to avoid the typical reversal effect.
- **--strategy2_type** : Second Strategy to execute. Input **R** for reversal and **M** for momentum.
- **--days2** : Number of days to compute second strategy-related returns. For the momentum strategy, an additional 20 trading-day gap is added to avoid the typical reversal effect.
- **--top_pct** : Top (1 to 100) percentile of the tickers under the strategy type to be selected for rebalancing. Note that the number of tickers selected is rounded up. If 10 tickers are being tracked and _55_ is the _top_pct_ parameter value, then the top 6 tickers will be selected.

We have assumed the following while implementing this portfolio allocator:

1. When rebalancing portfolio, no transaction cost is incurred
2. AUM is evenly rebalanced to the tickers that we allocate to
3. Fractional stocks can be bought.

If you'd like to run all the tests, run `py.test` on the root directory of this repository.
