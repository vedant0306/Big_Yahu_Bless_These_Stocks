#  Big Yahu Bless These Stocks

An automated quantitative trading engine built in Python that executes multi-strategy technical signals on **Alpaca API**. The bot uses an ensemble consensus voting framework (Combining Moving Average Crossovers, Volatility-Filtered Mean Reversion, and Multi-Timeframe Momentum) to scan stocks and execute trades automatically via **GitHub Actions**.

---

##  Key Features

* **Consensus Signal Framework:** Combines 3 distinct quantitative strategies (MA Crossover, RSI/Bollinger Mean Reversion, and Multi-Timeframe MACD) and requires a 2/3 consensus vote before opening trades.
* **Algorithmic Risk Management:** Dynamic Stop-Loss and Take-Profit values generated via Average True Range (ATR).
* **Automated Cloud Execution:** Powered by GitHub Actions to run on a set schedule during market open (9:30 AM EST) with zero server infrastructure overhead.
* **Paper & Live Ready:** Seamlessly toggle between Alpaca Paper Trading and Live Trading through environment variables.
* **Rate-Limit Aware:** Safe API throttling designed for free-tier broker limitations.

---

## 🏗️ Repository Architecture

```text
Big_Yahu_Bless_These_Stocks/
├── .github/
│   └── workflows/
│       └── trading_bot.yml      # Automated CRON runner for GitHub Actions
├── src/
│   ├── __init__.py
│   ├── config.py                # Environment configuration loader
│   ├── data.py                  # Alpaca Market Data fetcher
│   ├── execution.py             # Order execution & risk management
│   ├── stock_list.py            # Universe selection & ticker loader
│   └── strategy.py             # Quantitative strategies & Ensemble model
├── tests/
│   └── test_strategy.py        # PyTest unit testing
├── .gitignore
├── main.py                      # Core execution loop
├── README.md
└── requirements.txt             # Locked project dependencies