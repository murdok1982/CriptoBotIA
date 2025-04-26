import openai

class BrainGPT:
    def __init__(self):
        openai.api_key = "TU_API_KEY_OPENAI"

    def suggest_strategy(self, market_data, indicators):
        try:
            prompt = (
                f"Precio actual: {market_data['price']}\n"
                f"RSI: {indicators['rsi']}\n"
                f"MACD: {indicators['macd']}\n"
                f"EMA 12: {indicators['ema_fast']}\n"
                f"EMA 26: {indicators['ema_slow']}\n"
                f"Basándote en estos datos, ¿qué estrategia recomendarías usar entre EMA_CROSS, RSI_MACD, BOLLINGER_BREAKOUT, BREAKOUT_MOMENTUM, MEAN_REVERSION?"
            )

            response = openai.ChatCompletion.create(
                model="gpt-4",#aqui no se si te funcionara con https://chatgpt.com/g/g-znPnqPziD-crypto-trader-automatizado   intentalo de varias maneras es que con el tema api de mi gpt no se si a ti te ira!!
                messages=[
                    {"role": "system", "content": "Eres un asesor de trading experto."},
                    {"role": "user", "content": prompt}
                ]
            )

            strategy = response['choices'][0]['message']['content']
            # Mapear respuesta a nombres de estrategia
            if "EMA" in strategy:
                return "EMA_CROSS"
            elif "RSI" in strategy:
                return "RSI_MACD"
            elif "Bollinger" in strategy:
                return "BOLLINGER_BREAKOUT"
            elif "Breakout" in strategy:
                return "BREAKOUT_MOMENTUM"
            elif "Reversion" in strategy:
                return "MEAN_REVERSION"
            else:
                return "EMA_CROSS"

        except Exception as e:
            print(f"[Error GPT]: {e}")
            return "EMA_CROSS"
