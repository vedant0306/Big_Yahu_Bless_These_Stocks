import os
from dotenv import load_dotenv
import stock_list

load_dotenv()

class Config:
    def __init__(self):
        self.API_KEY = os.getenv("ALPACA_API_KEY")
        self.SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")
        
        # Set IS_PAPER=False in .env only when ready for real money
        self.IS_PAPER = os.getenv("IS_PAPER", "true").lower() == "true"
        
        # Strategy Parameters
        self.SYMBOL = stock_list.get_tradable_universe(500)
        self.FAST_WINDOW = 20
        self.SLOW_WINDOW = 50
        
        # Safety Check
        if not self.API_KEY or not self.SECRET_KEY:
            raise ValueError("Missing ALPACA_API_KEY or ALPACA_SECRET_KEY in environment.")