# src/backtest.py
import vectorbt as vbt
from src.config import Config
from src.data import MarketDataClient

def run_backtest():
    config = Config()
    data_client = MarketDataClient(config)
    df = data_client.get_recent_bars(config.SYMBOL, limit=1000)
    
    price = df['close']

    # ----------------------------------------------------
    # ADD MOVING AVERAGE FUNCTION HERE FOR VECTORBT
    # ----------------------------------------------------
    fast_ma = vbt.MA.run(price, window=config.FAST_WINDOW)
    slow_ma = vbt.MA.run(price, window=config.SLOW_WINDOW)

    # Crossover conditions
    entries = fast_ma.ma_crossed_above(slow_ma)
    exits = fast_ma.ma_crossed_below(slow_ma)

    # Run backtest
    pf = vbt.Portfolio.from_signals(price, entries=entries, exits=exits, init_cash=10000)
    print(pf.stats())

if __name__ == "__main__":
    run_backtest()