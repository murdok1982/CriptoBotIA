from .base_strategy import BaseStrategy

class RSIMACDStrategy(BaseStrategy):
    def decide(self, market_data, indicators):
        rsi = indicators['rsi']
        macd = indicators['macd']

        if rsi < 30 and macd > 0:
            return "BUY"
        elif rsi > 70 and macd < 0:
            return "SELL"
        else:
            return "HOLD"
