from .base_strategy import BaseStrategy

class MeanReversionStrategy(BaseStrategy):
    def decide(self, market_data, indicators):
        rsi = indicators['rsi']

        if rsi > 70:
            return "SELL"
        elif rsi < 30:
            return "BUY"
        else:
            return "HOLD"
