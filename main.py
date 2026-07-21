import sys
from src.config import Config
from src.data import MarketDataClient
from src.strategy import MovingAverageCrossover
from src.execution import OrderExecutor

def main():
    try:
        # 1. Load Configurations
        config = Config()
        mode_label = "PAPER TRADING" if config.IS_PAPER else " LIVE REAL MONEY "
        print(f"Starting Quant Engine in [{mode_label}] mode for {config.SYMBOL}...")

        # 2. Instantiate Modules
        data_client = MarketDataClient(config)
        strategy = MovingAverageCrossover(config.FAST_WINDOW, config.SLOW_WINDOW)
        executor = OrderExecutor(config)

        # Print balance details
        executor.get_account_info()

        # 3. Fetch Data
        print(f"Fetching market data for {config.SYMBOL}...")
        bars = data_client.get_recent_bars(config.SYMBOL, limit=config.SLOW_WINDOW + 10)

        # 4. Generate Signal
        signal = strategy.generate_signal(bars)
        print(f"Generated Signal: {signal}")

        # 5. Execute
        if signal == "BUY":
            executor.place_buy_order(config.SYMBOL, qty=1)
        elif signal == "SELL":
            executor.place_sell_order(config.SYMBOL, qty=1)
        else:
            print("No action required. Holding current position.")

    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()