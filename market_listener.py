from binance_connector import BinanceFuturesClient
import pandas as pd
import ta

class MarketListener:
    def __init__(self, client, symbol="BTCUSDT"):
        self.client = client
        self.symbol = symbol

    def get_latest_data(self):
        price = self.client.get_price(self.symbol)
        return {"price": price}

    def get_latest_indicators(self):
        # Simulamos indicadores usando últimos precios
        candles = self.client.client.futures_klines(symbol=self.symbol, interval="1m", limit=100)
        df = pd.DataFrame(candles, columns=['time','open','high','low','close','volume','close_time','qav','num_trades','taker_base_vol','taker_quote_vol','ignore'])
        df['close'] = df['close'].astype(float)

        rsi = ta.momentum.RSIIndicator(df['close'], window=14).rsi().iloc[-1]
        macd = ta.trend.MACD(df['close']).macd_diff().iloc[-1]
        ema_fast = ta.trend.EMAIndicator(df['close'], window=12).ema_indicator().iloc[-1]
        ema_slow = ta.trend.EMAIndicator(df['close'], window=26).ema_indicator().iloc[-1]

        return {
            "rsi": rsi,
            "macd": macd,
            "ema_fast": ema_fast,
            "ema_slow": ema_slow
        }

    def start_listening(self):
        print(f"🎧 Escuchando datos de mercado para {self.symbol}...")
