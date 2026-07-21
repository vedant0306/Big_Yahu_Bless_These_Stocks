import vectorbt as vbt
from src.config import Config
from src.data import MarketDataClient

def run_vectorbt_backtest():
    # 1. Fetch data using your existing data module
    config = Config()
    data_client = MarketDataClient(config)
    
    print(f"Fetching historical data for {config.SYMBOL} backtest...")
    df = data_client.get_recent_bars(config.SYMBOL, limit=1000)
    
    price = df['close']

    # 2. Define Moving Averages with vectorbt
    fast_ma = vbt.MA.run(price, config.FAST_WINDOW)
    slow_ma = vbt.MA.run(price, config.SLOW_WINDOW)

    # 3. Generate Crossover Signals
    entries = fast_ma.ma_crossed_above(slow_ma)
    exits = fast_ma.ma_crossed_below(slow_ma)

    # 4. Run Portfolio Backtest
    portfolio = vbt.Portfolio.from_signals(
        price, 
        entries=entries, 
        exits=exits, 
        init_cash=10000,
        fees=0.0  # 0.0 for commission-free brokers like Alpaca
    )

    # 5. Print Performance Analytics
    print("\n" + "="*40)
    print("      VECTORBT BACKTEST RESULTS      ")
    print("="*40)
    print(portfolio.stats())

    # 6. (Optional) Save interactive HTML chart
    # portfolio.plot().write_html("backtest_results.html")

if __name__ == "__main__":
    run_vectorbt_backtest()