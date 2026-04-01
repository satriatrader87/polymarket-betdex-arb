def calculate_arb_opportunity(poly_price, sol_odds):
    # Sol Price = 1 / Odds (Konversi ke format 0-1)
    sol_price = 1 / sol_odds
    
    # Combined = Beli YES di Poly + Beli NO (Lay) di BetDex
    # Harga NO di BetDex adalah (1 - sol_price)
    combined_cost = poly_price + (1 - sol_price)
    
    if combined_cost < 1.00:
        return True, (1.00 - combined_cost)
    return False, 0

def kelly_criterion(balance, price, win_rate=0.70):
    b = (1 / price) - 1
    f_star = (win_rate * (b + 1) - 1) / b
    return max(0, balance * f_star * 0.2) # 0.2 = Conservative Factor
