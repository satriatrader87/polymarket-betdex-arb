# engine/market_depth.py

class MarketDepthAnalyzer:
    @staticmethod
    def calculate_effective_price(orderbook, target_amount):
        """
        Menghitung harga rata-rata jika kita membeli dalam jumlah 'target_amount'.
        Mencegah kerugian akibat likuiditas tipis (Slippage).
        """
        total_cost = 0
        amount_filled = 0
        
        # orderbook['asks'] berisi list [harga, jumlah]
        for price, size in orderbook:
            price = float(price)
            size = float(size)
            
            needed = target_amount - amount_filled
            if size >= needed:
                total_cost += needed * price
                amount_filled += needed
                break
            else:
                total_cost += size * price
                amount_filled += size
        
        if amount_filled < target_amount:
            return None # Likuiditas tidak cukup untuk modal kita
            
        return total_cost / target_amount # Harga rata-rata (Effective Price)
