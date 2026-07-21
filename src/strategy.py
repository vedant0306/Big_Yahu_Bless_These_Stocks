# src/strategy.py
import pandas as pd

class MovingAverageCrossover:
    def __init__(self, fast_window: int = 20, slow_window: int = 50):
        self.fast_window = fast_window
        self.slow_window = slow_window

    def calculate_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Helper method: Adds Moving Average columns to the incoming DataFrame."""
        df = df.copy()
        df['fast_ma'] = df['close'].rolling(window=self.fast_window).mean()
        df['slow_ma'] = df['close'].rolling(window=self.slow_window).mean()
        return df

    def generate_signal(self, df: pd.DataFrame) -> str:
        """Generates trade signals based on MA crossover."""
        if len(df) < self.slow_window:
            return "HOLD"

        # Calculate MAs
        df = self.calculate_indicators(df)

        current_fast = df['fast_ma'].iloc[-1]
        current_slow = df['slow_ma'].iloc[-1]
        prev_fast = df['fast_ma'].iloc[-2]
        prev_slow = df['slow_ma'].iloc[-2]

        # Bullish Crossover (Fast crosses above Slow)
        if prev_fast <= prev_slow and current_fast > current_slow:
            return "BUY"
        # Bearish Crossover (Fast crosses below Slow)
        elif prev_fast >= prev_slow and current_fast < current_slow:
            return "SELL"

        return "HOLD"