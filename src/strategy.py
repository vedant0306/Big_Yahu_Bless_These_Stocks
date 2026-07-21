# src/strategy.py
import pandas as pd
import numpy as np

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
    

class VolatilityMeanReversion:
    def __init__(self, rsi_period: int = 14, bb_period: int = 20, bb_std: float = 2.0):
        self.rsi_period = rsi_period
        self.bb_period = bb_period
        self.bb_std = bb_std

    def _compute_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        
        # 1. Bollinger Bands
        df['sma'] = df['close'].rolling(self.bb_period).mean()
        df['std'] = df['close'].rolling(self.bb_period).std()
        df['upper_band'] = df['sma'] + (df['std'] * self.bb_std)
        df['lower_band'] = df['sma'] - (df['std'] * self.bb_std)

        # 2. Relative Strength Index (RSI)
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(self.rsi_period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(self.rsi_period).mean()
        rs = gain / loss
        df['rsi'] = 100 - (100 / (1 + rs))

        # 3. ATR (Average True Range) for dynamic risk
        high_low = df['high'] - df['low']
        high_close = np.abs(df['high'] - df['close'].shift())
        low_close = np.abs(df['low'] - df['close'].shift())
        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = np.max(ranges, axis=1)
        df['atr'] = true_range.rolling(14).mean()

        return df

    def generate_signal(self, df: pd.DataFrame) -> dict:
        df = self._compute_indicators(df)
        latest = df.iloc[-1]

        if latest['close'] <= latest['lower_band'] and latest['rsi'] < 30:
            return {
                "signal": "BUY",
                "stop_loss": latest['close'] - (1.5 * latest['atr']),
                "take_profit": latest['close'] + (2.0 * latest['atr'])
            }
        elif latest['close'] >= latest['upper_band'] and latest['rsi'] > 70:
            return {
                "signal": "SELL",
                "stop_loss": latest['close'] + (1.5 * latest['atr']),
                "take_profit": latest['close'] - (2.0 * latest['atr'])
            }

        return {"signal": "HOLD", "stop_loss": None, "take_profit": None}
    
class MultiTimeframeMomentum:
    def __init__(self, fast_ema: int = 12, slow_ema: int = 26, signal_ema: int = 9):
        self.fast = fast_ema
        self.slow = slow_ema
        self.signal = signal_ema

    def _compute_macd(self, series: pd.Series):
        fast_series = series.ewm(span=self.fast, adjust=False).mean()
        slow_series = series.ewm(span=self.slow, adjust=False).mean()
        macd_line = fast_series - slow_series
        signal_line = macd_line.ewm(span=self.signal, adjust=False).mean()
        histogram = macd_line - signal_line
        return macd_line, signal_line, histogram

    def generate_signal(self, df_5min: pd.DataFrame, df_1hr: pd.DataFrame) -> str:
        # 1. Macro Trend Check (1-Hour 200 EMA)
        ema_200_macro = df_1hr['close'].ewm(span=200, adjust=False).mean().iloc[-1]
        current_macro_price = df_1hr['close'].iloc[-1]
        
        is_bullish_macro = current_macro_price > ema_200_macro

        # 2. Lower Timeframe MACD (5-Min)
        macd, signal, hist = self._compute_macd(df_5min['close'])
        
        current_macd, prev_macd = macd.iloc[-1], macd.iloc[-2]
        current_signal, prev_signal = signal.iloc[-1], signal.iloc[-2]

        # Bullish Entry: Bullish Macro Gate + MACD Crossover on Micro
        if is_bullish_macro:
            if prev_macd <= prev_signal and current_macd > current_signal:
                return "BUY"

        # Bearish Exit Signal
        if prev_macd >= prev_signal and current_macd < current_signal:
            return "SELL"

        return "HOLD"
    

class EnsembleStrategy:
    def __init__(self, min_votes: int = 2):
        """
        Combines multiple strategies into a single consensus decision.
        :param min_votes: Minimum number of matching signals required to trigger a trade (default: 2/3).
        """
        self.min_votes = min_votes
        
        # Instantiate child strategies
        self.ma_strategy = MovingAverageCrossover()
        self.vol_strategy = VolatilityMeanReversion()
        self.mtf_strategy = MultiTimeframeMomentum()

    def generate_signal(self, df_5min: pd.DataFrame, df_1hr: pd.DataFrame = None) -> dict:
        """
        Evaluates all strategies and aggregates signals.
        If df_1hr is not provided, it falls back to using df_5min for higher-timeframe resample.
        """
        # Auto-generate 1-hour bars if only 5-min bars are passed
        if df_1hr is None:
            df_1hr = df_5min.resample('1h').agg({
                'open': 'first',
                'high': 'max',
                'low': 'min',
                'close': 'last',
                'volume': 'sum'
            }).dropna()

        # 1. Fetch individual signals
        sig_ma = self.ma_strategy.generate_signal(df_5min)
        
        sig_vol_raw = self.vol_strategy.generate_signal(df_5min)
        sig_vol = sig_vol_raw["signal"]  # Extract string from dict
        
        sig_mtf = self.mtf_strategy.generate_signal(df_5min, df_1hr)

        signals = [sig_ma, sig_vol, sig_mtf]

        # 2. Count votes
        buy_votes = signals.count("BUY")
        sell_votes = signals.count("SELL")

        # Log individual strategy votes for transparency
        print(f"   [Votes] MA: {sig_ma} | Volatility: {sig_vol} | MTF: {sig_mtf}")

        # 3. Decision Logic
        if buy_votes >= self.min_votes:
            final_signal = "BUY"
        elif sell_votes >= self.min_votes:
            final_signal = "SELL"
        else:
            final_signal = "HOLD"

        # Pass along risk params if available from the volatility strategy
        return {
            "signal": final_signal,
            "votes": {"BUY": buy_votes, "SELL": sell_votes, "HOLD": signals.count("HOLD")},
            "stop_loss": sig_vol_raw.get("stop_loss"),
            "take_profit": sig_vol_raw.get("take_profit")
        }