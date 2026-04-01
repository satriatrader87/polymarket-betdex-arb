# core/orchestrator.py
import asyncio
import json
import os
from dotenv import load_dotenv
from engine.calculator import calculate_arb_opportunity
from providers.polymarket import PolymarketProvider
from providers.betdex import BetDexProvider

load_dotenv() # Mengambil data dari .env

class ArbOrchestrator:
    def __init__(self):
        self.config = self.load_config()
        self.poly = PolymarketProvider(os.getenv("POLY_RPC_URL"))
        self.betdex = BetDexProvider(os.getenv("SOL_RPC_URL"))

    def load_config(self):
        with open('config.json', 'r') as f:
            return json.load(f)

    async def start_scanning(self):
        print("🚀 Bot Started. Monitoring markets...")
        settings = self.config['bot_settings']
        
        while True:
            for market in self.config['active_markets']:
                # Ambil harga dari kedua provider secara paralel (Cepat!)
                poly_task = self.poly.get_price(market['poly_token_id'])
                sol_task = self.betdex.get_price(market['betdex_market_pubkey'])
                
                prices = await asyncio.gather(poly_task, sol_task)
                p_price, s_odds = prices

                if p_price and s_odds:
                    is_arb, profit = calculate_arb_opportunity(p_price, s_odds)
                    if is_arb and profit > settings['min_profit_threshold']:
                        print(f"🔥 Peluang di {market['name']}! Profit: {profit:.2%}")
                        # Lanjut ke logika eksekusi...
            
            await asyncio.sleep(settings['check_interval_seconds'])
