# engine/risk_manager.py

class RiskManager:
    def __init__(self, max_cap):
        self.max_capital = max_cap

    def validate_execution(self, profit_percent, orderbook_depth):
        """
        Memastikan profit cukup besar untuk menutup biaya gas 
        dan likuiditas cukup untuk modal kita.
        """
        # 1. Cek apakah profit > 1.5% (Setelan di config)
        if profit_percent < 0.015:
            return False, "Profit too low after slippage"

        # 2. Cek apakah di harga tersebut tersedia volume yang cukup
        # Misal kita mau pasang $50, tapi di orderbook cuma ada $10
        if orderbook_depth < self.max_capital:
            return False, "Insufficient liquidity (Slippage risk)"

        return True, "Safe to execute"
