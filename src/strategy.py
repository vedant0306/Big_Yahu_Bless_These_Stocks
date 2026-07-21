import pandas as pd

class MovingAverageCrossover:
    def __init__(self, fast_window: int = 20, slow_window: int = 50):
        self.fast_window = fast_window
        self.slow_window = slow_window

    def generate_signal(self, df: pd.DataFrame) -> str:
        """
        Calculates moving averages and returns 'BUY', 'SELL', or 'HOLD'.
        """
        if len(df) < self.slow_window:
            print("Not enough data to calculate indicators.")
            return "HOLD"

        closes = df['close']
        
        # Calculate Simple Moving Averages
        fast_sma = closes.rolling(window=self.fast_window).mean()
        slow_sma = closes.rolling(window=self.slow_window).mean()

        # Check current and previous indicators to detect crossovers
        current_fast = fast_sma.iloc[-1]
        current_slow = slow_sma.iloc[-1]
        prev_fast = fast_sma.iloc[-2]
        prev_slow = slow_sma.iloc[-2]

        # Bullish Crossover
        if prev_fast <= prev_slow and current_fast > current_slow:
            return "BUY"
        # Bearish Crossover
        elif prev_fast >= prev_slow and current_fast < current_slow:
            return "SELL"
        
        return "HOLD"