from .base_strategy import BaseStrategy

class BollingerBreakoutStrategy(BaseStrategy):
    def decide(self, market_data, indicators):
        # Esta estrategia sería más completa con desviaciones estándar, pero haremos algo básico
        rsi = indicators['rsi']

        if rsi < 20:
            return "BUY"
        elif rsi > 80:
            return "SELL"
        else:
            return "HOLD"
