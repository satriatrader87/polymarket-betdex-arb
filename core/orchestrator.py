import asyncio
import json
import os
from dotenv import load_dotenv
from core.logger import log_info, log_success, log_error
from engine.calculator import calculate_arb_opportunity, kelly_criterion
from engine.risk_manager import RiskManager
from providers.polymarket import PolymarketProvider
from providers.betdex import BetDexProvider

load_dotenv()

class ArbOrchestrator:
    def __init__(self):
        with open('config.json', 'r') as f:
            self.config = json.load(f)
        
        self.poly = PolymarketProvider(os.getenv("POLY_RPC_URL"))
        self.betdex = BetDexProvider(os.getenv("SOL_RPC_URL"))
        self.risk = RiskManager(self.config['bot_settings']['max_capital_usd'])

    async def start_scanning(self):
        log_info("Initializing Arb Bot Orchestrator...")
        settings = self.config['bot_settings']
        
        while True:
            for market in self.config['active_markets']:
                p_price = await self.poly.get_price(market['poly_token_id'])
                s_odds = await self.betdex.get_price(market['betdex_market_pubkey'])

                if p_price and s_odds:
                    is_arb, profit = calculate_arb_opportunity(p_price, s_odds)
                    
                    if is_arb and profit > settings['min_profit_threshold']:
                        # Validasi Risiko & Kedalaman
                        is_safe, msg = self.risk.validate_execution(profit)
                        if is_safe:
                            stake = kelly_criterion(settings['max_capital_usd'], p_price)
                            log_success(f"ARB FOUND: {market['name']} | Profit: {profit:.2%} | Stake: ${stake:.2f}")
                            # TODO: await self.execute_trades(stake)
                        else:
                            log_info(f"Arb found but risk check failed: {msg}")
                
            await asyncio.sleep(settings['check_interval_seconds'])
