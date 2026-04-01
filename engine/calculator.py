# engine/calculator.py

def calculate_arb_opportunity(poly_price, sol_odds, gas_estimate=0.50):
    """
    poly_price: Harga YES di Polymarket (0.00 - 1.00)
    sol_odds: Odds BACK di BetDEX (misal 2.5)
    """
    # 1. Konversi Odds Solana ke Harga (1 / Odds)
    sol_price = 1 / sol_odds
    
    # 2. Rumus Arbitrase: Harga YES (Poly) + Harga NO (Sol)
    # Harga NO di Solana adalah (1 - sol_price)
    combined_cost = poly_price + (1 - sol_price)
    
    # 3. Cek Profit
    if combined_cost < 1.00:
        gross_profit_per_share = 1.00 - combined_cost
        return True, gross_profit_per_share
    
    return False, 0

def kelly_criterion(balance, price, win_rate=0.75):
    """
    Menghitung modal aman (Fractional Kelly)
    """
    b = (1 / price) - 1  # Odds ratio
    f_star = (win_rate * (b + 1) - 1) / b
    
    # Gunakan 25% dari Kelly (Super Aman)
    safe_f = max(0, f_star * 0.25)
    return balance * safe_f
