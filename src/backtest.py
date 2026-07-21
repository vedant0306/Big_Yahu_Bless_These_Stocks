# src/backtest.py
import vectorbt as vbt
from src.config import Config
from src.data import MarketDataClient

def run_multi_stock_backtest(symbols: list):
    config = Config()
    data_client = MarketDataClient(config)
    
    # Fetch price data for multiple stocks (returns a multi-column DataFrame)
    # e.g., columns = ['AAPL', 'MSFT', 'NVDA', 'GOOGL']
    df = data_client.get_recent_bars_multi(symbols, limit=1000)
    price = df['close']

    # VectorBT runs all stocks in parallel automatically
    fast_ma = vbt.MA.run(price, window=config.FAST_WINDOW)
    slow_ma = vbt.MA.run(price, window=config.SLOW_WINDOW)

    entries = fast_ma.ma_crossed_above(slow_ma)
    exits = fast_ma.ma_crossed_below(slow_ma)

    # Portfolio metrics aggregated across all assets
    pf = vbt.Portfolio.from_signals(
        price, 
        entries=entries, 
        exits=exits, 
        init_cash=10000,
        fees=0.0005 # Include realistic transaction fees!
    )
    
    print("--- TOTAL PORTFOLIO STATS ---")
    print(pf.stats())
    
    # You can also see individual stock performance:
    print("\n--- SHARPE RATIO BY TICKER ---")
    print(pf.sharpe_ratio())

if __name__ == "__main__":
    test_universe = ["AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "META", "TSLA"]
    run_multi_stock_backtest(test_universe)