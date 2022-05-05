# Data Science in Quantitative Finance

Coursework for YSC4228 Data Science in Quantitative Finance. Repository is organized by assignments, with code done by Zhao Yuan and Walter

## Assignment 1 - Kernel Regression

For this assignment, we are to implement Linear Regression using a Gaussian Kernel. The detailed implementation can be found in the `kernel_regression` directory.

## Assignment 2 - Scraping Market Data

For this assignment, we are to implement scraping market data. This was done using the `yfinance` module.

## Assignment 3 - Backtesting a Single Strategy

As an extension to assignment 2, we used our fetched data from the `yfinance` module to backtest either reversal or momentum strategy.

## Assignment 4 - Backtesting Multiple-Signal Strategy

As an extension to assignment 3, we instead did backtesting for multiple-signal strategies. We employed 2 strategies in parallel, created a linear regression model using `sklearn` and chose stocks based on the scores given from the regression model.