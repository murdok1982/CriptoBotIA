from .base_strategy import BaseStrategy

class EMACrossStrategy(BaseStrategy):
    def decide(self, market_data, indicators):
        ema_fast = indicators['ema_fast']
        ema_slow = indicators['ema_slow']

        if ema_fast > ema_slow:
            return "BUY"
        elif ema_fast < ema_slow:
            return "SELL"
        else:
            return "HOLD"
