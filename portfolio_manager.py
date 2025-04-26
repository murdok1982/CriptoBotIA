class PortfolioManager:
    def __init__(self, client):
        self.client = client
        self.last_balance = 0

    def update(self):
        try:
            balance = self.client.get_balance()
            if balance != self.last_balance:
                print(f"💰 Balance actualizado: {balance} USDT")
                self.last_balance = balance
        except Exception as e:
            print(f"[Error Portfolio]: {e}")
