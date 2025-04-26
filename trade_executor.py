from config import TRADING_MODE
import time

class TradeExecutor:
    def __init__(self, client, risk_manager):
        self.client = client
        self.risk_manager = risk_manager

    def execute_trade(self, symbol, side):
        price = self.client.get_price(symbol)
        quantity = self.risk_manager.calculate_quantity(price)

        if TRADING_MODE == "PAPER":
            print(f"[SIMULACION] {side} {quantity} {symbol} a {price}")
        else:
            order = self.client.place_market_order(symbol, side, quantity)
            print(f"[ORDEN REAL] {side} ejecutado: {order}")

        # Simulación de trailing stop activado
        trailing_stop_price = self.risk_manager.get_trailing_stop_price(price, side)
        print(f"🛡️ Trailing Stop activado en: {trailing_stop_price}")

        time.sleep(2)  # Simular tiempo de orden ejecutándose
