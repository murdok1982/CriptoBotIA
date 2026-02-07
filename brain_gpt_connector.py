"""GPT Brain connector for strategy selection."""

import os
import logging
from openai import OpenAI
from typing import Dict, Optional

logger = logging.getLogger(__name__)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


class BrainGPT:
    """AI-powered strategy advisor using GPT."""
    
    STRATEGIES = [
        'EMA_CROSS',
        'RSI_MACD',
        'BOLLINGER_BREAKOUT',
        'BREAKOUT_MOMENTUM',
        'MEAN_REVERSION'
    ]
    
    def __init__(self, model: str = None):
        """Initialize GPT Brain.
        
        Args:
            model: GPT model to use (defaults to gpt-4)
        """
        self.model = model or os.getenv('GPT_MODEL', 'gpt-4')
        
        if not os.getenv('OPENAI_API_KEY'):
            raise ValueError(
                "OPENAI_API_KEY not found. Set it as environment variable."
            )
        
        logger.info(f"BrainGPT initialized with model: {self.model}")
    
    def suggest_strategy(self, market_data: Dict, indicators: Dict) -> str:
        """Suggest best trading strategy based on market data.
        
        Args:
            market_data: Dict with current market information
            indicators: Dict with technical indicators
            
        Returns:
            Strategy name (one of STRATEGIES)
        """
        try:
            prompt = self._create_analysis_prompt(market_data, indicators)
            
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an expert cryptocurrency trading advisor. "
                            "Analyze market data and technical indicators to suggest "
                            "the BEST trading strategy. Choose ONE from: "
                            f"{', '.join(self.STRATEGIES)}. "
                            "Respond with ONLY the strategy name."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=100
            )
            
            strategy_response = response.choices[0].message.content.strip()
            strategy = self._parse_strategy(strategy_response)
            
            logger.info(f"GPT suggested strategy: {strategy}")
            return strategy
            
        except Exception as e:
            logger.error(f"Error getting GPT suggestion: {e}")
            # Default fallback strategy
            return "EMA_CROSS"
    
    def _create_analysis_prompt(self, market_data: Dict, indicators: Dict) -> str:
        """Create analysis prompt from market data.
        
        Args:
            market_data: Market information
            indicators: Technical indicators
            
        Returns:
            Formatted prompt string
        """
        prompt = f"""
Market Analysis Request:

Current Price: {market_data.get('price', 'N/A')}
Volume: {market_data.get('volume', 'N/A')}
24h Change: {market_data.get('change_24h', 'N/A')}%

Technical Indicators:
- RSI: {indicators.get('rsi', 'N/A')}
- MACD: {indicators.get('macd', 'N/A')}
- EMA Fast (12): {indicators.get('ema_fast', 'N/A')}
- EMA Slow (26): {indicators.get('ema_slow', 'N/A')}
- Bollinger Upper: {indicators.get('bb_upper', 'N/A')}
- Bollinger Lower: {indicators.get('bb_lower', 'N/A')}

Available Strategies:
1. EMA_CROSS - Trend following with EMA crossovers
2. RSI_MACD - Momentum strategy combining RSI and MACD
3. BOLLINGER_BREAKOUT - Volatility breakout using Bollinger Bands
4. BREAKOUT_MOMENTUM - Price breakout with volume confirmation
5. MEAN_REVERSION - Statistical arbitrage mean reversion

Based on the market conditions and indicators, which strategy would be most effective?
Respond with ONLY the strategy name.
"""
        return prompt
    
    def _parse_strategy(self, response: str) -> str:
        """Parse GPT response to extract strategy name.
        
        Args:
            response: Raw GPT response
            
        Returns:
            Valid strategy name
        """
        response_upper = response.upper()
        
        # Try exact match first
        for strategy in self.STRATEGIES:
            if strategy in response_upper:
                return strategy
        
        # Try keyword matching
        if "EMA" in response_upper or "CROSS" in response_upper:
            return "EMA_CROSS"
        elif "RSI" in response_upper or "MACD" in response_upper:
            return "RSI_MACD"
        elif "BOLLINGER" in response_upper:
            return "BOLLINGER_BREAKOUT"
        elif "BREAKOUT" in response_upper or "MOMENTUM" in response_upper:
            return "BREAKOUT_MOMENTUM"
        elif "REVERSION" in response_upper or "MEAN" in response_upper:
            return "MEAN_REVERSION"
        
        # Default fallback
        logger.warning(f"Could not parse strategy from: {response}. Using default.")
        return "EMA_CROSS"
    
    def get_detailed_analysis(self, market_data: Dict, indicators: Dict) -> Dict:
        """Get detailed market analysis and strategy recommendation.
        
        Args:
            market_data: Market information
            indicators: Technical indicators
            
        Returns:
            Dict with strategy, reasoning, and confidence
        """
        try:
            prompt = f"{self._create_analysis_prompt(market_data, indicators)}\n\n"
            prompt += "Provide: 1) Best strategy, 2) Reasoning (1 sentence), 3) Confidence (0-100%)"
            
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert trading advisor. Provide concise analysis."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=200
            )
            
            analysis_text = response.choices[0].message.content
            strategy = self._parse_strategy(analysis_text)
            
            return {
                'strategy': strategy,
                'analysis': analysis_text,
                'model': self.model,
                'success': True
            }
            
        except Exception as e:
            logger.error(f"Error getting detailed analysis: {e}")
            return {
                'strategy': 'EMA_CROSS',
                'analysis': f'Error: {str(e)}',
                'model': self.model,
                'success': False
            }


if __name__ == "__main__":
    # Test the BrainGPT
    test_market_data = {
        'price': 45000,
        'volume': 1000000,
        'change_24h': 2.5
    }
    
    test_indicators = {
        'rsi': 65,
        'macd': 'bullish',
        'ema_fast': 44800,
        'ema_slow': 44500,
        'bb_upper': 46000,
        'bb_lower': 44000
    }
    
    brain = BrainGPT()
    strategy = brain.suggest_strategy(test_market_data, test_indicators)
    print(f"Suggested Strategy: {strategy}")
    
    detailed = brain.get_detailed_analysis(test_market_data, test_indicators)
    print(f"\nDetailed Analysis:\n{detailed['analysis']}")
