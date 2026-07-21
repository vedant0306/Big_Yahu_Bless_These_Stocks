from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from src.config import Config

class OrderExecutor:
    def __init__(self, config: Config):
        self.client = TradingClient(config.API_KEY, config.SECRET_KEY, paper=config.IS_PAPER)

    def get_account_info(self):
        account = self.client.get_account()
        print(f"Account Status: {account.status}")
        print(f"Buying Power: ${account.buying_power}")
        return account

    def place_buy_order(self, symbol: str, qty: int = 1):
        order_data = MarketOrderRequest(
            symbol=symbol,
            qty=qty,
            side=OrderSide.BUY,
            time_in_force=TimeInForce.GTC
        )
        order = self.client.submit_order(order_data)
        print(f"✅ BUY Order Executed for {symbol} | Order ID: {order.id}")
        return order

    def place_sell_order(self, symbol: str, qty: int = 1):
        order_data = MarketOrderRequest(
            symbol=symbol,
            qty=qty,
            side=OrderSide.SELL,
            time_in_force=TimeInForce.GTC
        )
        order = self.client.submit_order(order_data)
        print(f"🚨 SELL Order Executed for {symbol} | Order ID: {order.id}")
        return order