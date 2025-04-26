from binance.client import Client
from config import API_KEY, API_SECRET

class BinanceFuturesClient:
    def __init__(self):
        self.client = Client(API_KEY, API_SECRET)
    
    def get_balance(self):
        balance = self.client.futures_account_balance()
        usdt_balance = next(item for item in balance if item["asset"] == "USDT")
        return float(usdt_balance['balance'])

    def get_price(self, symbol):
        ticker = self.client.futures_symbol_ticker(symbol=symbol)
        return float(ticker['price'])

    def place_market_order(self, symbol, side, quantity):
        side_binance = Client.SIDE_BUY if side == "BUY" else Client.SIDE_SELL
        order = self.client.futures_create_order(
            symbol=symbol,
            side=side_binance,
            type=Client.ORDER_TYPE_MARKET,
            quantity=quantity
        )
        return order
