class RiskManager:
    def __init__(self, max_cap):
        self.max_cap = max_cap

    def validate_execution(self, profit):
        if profit < 0.01: # Minimal profit 1%
            return False, "Profit margin too thin"
        return True, "Success"
