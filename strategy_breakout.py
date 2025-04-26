from .base_strategy import BaseStrategy

class BreakoutMomentumStrategy(BaseStrategy):
    def decide(self, market_data, indicators):
        price = market_data['price']
        ema_fast = indicators['ema_fast']
        ema_slow = indicators['ema_slow']

        if price > ema_fast > ema_slow:
            return "BUY"
        elif price < ema_fast < ema_slow:
            return "SELL"
        else:
            return "HOLD"
