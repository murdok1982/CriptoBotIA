class BaseStrategy:
    def decide(self, market_data, indicators):
        raise NotImplementedError("La estrategia debe implementar el método decide()")

