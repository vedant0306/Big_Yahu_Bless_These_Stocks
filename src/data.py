import pandas as pd
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from src.config import Config

class MarketDataClient:
    def __init__(self, config: Config):
        self.client = StockHistoricalDataClient(config.API_KEY, config.SECRET_KEY)

    def get_recent_bars(self, symbol: str, limit: int = 100) -> pd.DataFrame:
        """Fetches recent minute bars and returns a pandas DataFrame with a DatetimeIndex."""
        request_params = StockBarsRequest(
            symbol_or_symbols=symbol,
            timeframe=TimeFrame.Minute,
            limit=limit
        )
        bars = self.client.get_stock_bars(request_params)
        df = bars.df
        
        if df.empty:
            raise ValueError(f"No market data returned for symbol: {symbol}")
            
        # ------------------------------------------------------------------
        # FIX: Remove the MultiIndex level ('symbol') so only 'timestamp' remains
        # ------------------------------------------------------------------
        if isinstance(df.index, pd.MultiIndex):
            # Drop the 'symbol' level from the row index
            df = df.droplevel('symbol')
            
        return df