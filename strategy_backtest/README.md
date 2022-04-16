# Assignment 3 - Testing Backtesting Strategies

This repository is done by Walter and Zhao Yuan for the second assignment for Data Science in Quantitative Finance. In this assignment, we are required to backtest reversal and momentum based strategies. Afterwards, we are to print the information coefficient and how our assets under management fared. To run this repository, you may run this command to start.

```python
python backtest_strategy.py --tickers MSFT APPL NVDA --b 20200414 --e 20200718 --initial_aum 5000 --strategy_type R --days 10 --top_pct 50
```

The parameters are explained below:

- **--tickers** : A list of space-separated tickers you'd like to track.
- **--b** : Beginning date of the period to start rebalancing the portfolio. Note that positions are always taken at the end of the month.
- **--e** : End date of the period. If this parameter is not provided, then it set set to today's date by default.
- **--initial_aum** : Initial assets under management, expressed in terms of USD
- **--strategy_type** : Strategy to execute. Input **R** for reversal and **M** for momentum.
- **--days** : Number of days to compute strategy-related returns. For the momentum strategy, an additional 20 trading-day gap is added to avoid the typical reversal effect.
- **--top_pct** : Top (1 to 100) percentile of the tickers under the strategy type to be selected for rebalancing. Note that the number of tickers selected is rounded up. If 10 tickers are being tracked and _55_ is the _top_pct_ parameter value, then the top 6 tickers will be selected.
