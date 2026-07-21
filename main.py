import sys
import time
import datetime
from zoneinfo import ZoneInfo
from src.config import Config
from src.data import MarketDataClient
from src.strategy import EnsembleStrategy
from src.execution import OrderExecutor
from src.stock_list import Stock_List

def is_market_hours() -> bool:
    ny_tz = ZoneInfo("America/New_York")
    now = datetime.datetime.now(tz=ny_tz)

    if now.weekday() >= 5:  # Saturday=5, Sunday=6
        return False

    market_open = datetime.time(hour=9, minute=30, tzinfo=ny_tz)
    market_close = datetime.time(hour=16, minute=0, tzinfo=ny_tz)
    return market_open <= now.timetz() <= market_close

def main():
    try:
        if not is_market_hours():
            print("Market is currently closed. Exiting without trading.")
            return
        # 1. Load Configurations
        config = Config()
        mode_label = "PAPER TRADING" if config.IS_PAPER else " LIVE REAL MONEY "
        print(f"Starting Quant Engine in [{mode_label}] mode for {config.SYMBOL}...")

        # 2. Instantiate Modules
        data_client = MarketDataClient(config)
        strategy = EnsembleStrategy(min_votes=2)
        executor = OrderExecutor(config)

        # Print balance details
        executor.Print_Data_to_Terminal()
        executor.get_account_info()

        symbols = Stock_List.get_tradable_universe(limit=500)
        print(f"Loaded {len(symbols)} tickers for execution.\n" + "-"*40)

        # 3. Process Stocks in Loop
        for index, symbol in enumerate(symbols, start=1):
            try:
                print(f"[{index}/{len(symbols)}] Analyzing {symbol}...")
                
                # Fetch data
                bars = data_client.get_recent_bars(symbol, limit=250)
                
                if bars is None or len(bars) < 50:
                    print(f"⚠️ Insufficient data for {symbol}, skipping...")
                    continue
                # Generate signal
                result = strategy.generate_signal(bars)
                signal = result["signal"]
                stop_loss = result.get("stop_loss")
                take_profit = result.get("take_profit")

                # Execute Trade based on signal
                if signal == "BUY":
                    print(f"🚀 BUY Signal detected for {symbol}!")
                    executor.place_buy_order(symbol=symbol, qty=1, stop_loss=stop_loss, take_profit=take_profit)                
                elif signal == "SELL":
                    print(f"🔻 SELL Signal detected for {symbol}!")
                    executor.place_sell_order(symbol=symbol, qty=1, stop_loss=stop_loss, take_profit=take_profit)
                else:
                    print(f"HOLDing {symbol}.")

            except Exception as e:
                # Keep loop alive even if one symbol fails (e.g. invalid ticker or missing data)
                print(f"⚠️ Skipped {symbol}: {e}")
                continue
            #sleep so that the API does not get overloaded
            time.sleep(0.3)

    except Exception as e:
        print(f"An error occured {e}", file=sys.stderr)
        

if __name__ == "__main__":
    main()