



class Stock_List:
    TICKERS_500 = [
        "AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "META", "BRK.B", "TSLA", "AVGO", "PG",
        "JNJ", "COST", "HD", "UNH", "ABBV", "XOM", "MA", "V", "BAC", "JPM", "NFLX", "CRM",
        "AMD", "CVX", "LLY", "PEP", "KO", "MRK", "TU", "WMT", "ADBE", "ACN", "CSCO",
        "MCD", "DIS", "LIN", "ORCL", "ABT", "INTC", "QCOM", "INTU", "VZ", "TXN", "AMAT",
        "IBM", "GE", "AMGN", "CAT", "PFE", "NOW", "CMCSA", "GS", "MS", "SPGI", "RTX",
        "HON", "BKNG", "T", "LOW", "BLK", "ELV", "C", "AXP", "MDLZ", "NKE", "SCHW",
    ]

    @classmethod
    def get_tradable_universe(cls, limit: int = 500):
        """Returns the top N stocks from the universe."""
        return cls.TICKERS_500[:limit]
