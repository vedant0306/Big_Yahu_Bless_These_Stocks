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

    def place_buy_order(self, symbol: str, qty: int = 1, stop_loss=None, take_profit=None):
        """Place a market buy order.

        stop_loss and take_profit are accepted for compatibility with the calling code,
        but are not applied directly to a simple market order request.
        """
        order_data = MarketOrderRequest(
            symbol=symbol,
            qty=qty,
            side=OrderSide.BUY,
            time_in_force=TimeInForce.GTC
        )
        order = self.client.submit_order(order_data)
        print(f"✅ BUY Order Executed for {symbol} | Order ID: {order.id}")
        if stop_loss is not None or take_profit is not None:
            print(f"   Note: stop_loss={stop_loss}, take_profit={take_profit} were received but not applied to the market order.")
        return order

    def place_sell_order(self, symbol: str, qty: int = 1, stop_loss=None, take_profit=None):
        """Place a market sell order.

        stop_loss and take_profit are accepted for compatibility with the calling code,
        but are not applied directly to a simple market order request.
        """
        order_data = MarketOrderRequest(
            symbol=symbol,
            qty=qty,
            side=OrderSide.SELL,
            time_in_force=TimeInForce.GTC
        )
        order = self.client.submit_order(order_data)
        print(f"🚨 SELL Order Executed for {symbol} | Order ID: {order.id}")
        if stop_loss is not None or take_profit is not None:
            print(f"   Note: stop_loss={stop_loss}, take_profit={take_profit} were received but not applied to the market order.")
        return order
    
    def Print_Data_to_Terminal(self):

        account = self.client.get_account()
        balance_change = float(account.equity) - float(account.last_equity)
        print(f'Today\'s portfolio balance change: ${balance_change}')