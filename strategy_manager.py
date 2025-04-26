from strategies.strategy_ema_cross import EMACrossStrategy
from strategies.strategy_rsi_macd import RSIMACDStrategy
from strategies.strategy_bollinger import BollingerBreakoutStrategy
from strategies.strategy_breakout import BreakoutMomentumStrategy
from strategies.strategy_mean_reversion import MeanReversionStrategy

class StrategyManager:
    def __init__(self, client, executor, gpt_connector):
        self.client = client
        self.executor = executor
        self.gpt_connector = gpt_connector
        self.strategies = {
            "EMA_CROSS": EMACrossStrategy(),
            "RSI_MACD": RSIMACDStrategy(),
            "BOLLINGER_BREAKOUT": BollingerBreakoutStrategy(),
            "BREAKOUT_MOMENTUM": BreakoutMomentumStrategy(),
            "MEAN_REVERSION": MeanReversionStrategy()
        }

    def get_strategy(self, strategy_name):
        return self.strategies.get(strategy_name, EMACrossStrategy())  # Default
