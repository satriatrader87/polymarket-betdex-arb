# core/orchestrator.py
import asyncio
import os
import json
import base64
from dotenv import load_dotenv

from core.logger import log_info, log_success, log_error
from engine.calculator import calculate_arb_opportunity, kelly_criterion
from engine.risk_manager import RiskManager
from engine.market_depth import MarketDepthAnalyzer
from providers.polymarket import PolymarketProvider
from providers.betdex import BetDexProvider

load_dotenv()

class ArbOrchestrator:
    def __init__(self):
        # 1. Load Config
        with open('config.json', 'r') as f:
            self.config = json.load(f)
        
        self.settings = self.config['bot_settings']
        self.jito_settings = self.config['jito_settings']
        
        # 2. Inisialisasi Provider dengan Config Jito
        self.poly = PolymarketProvider(os.getenv("POLY_RPC_URL"))
        self.betdex = BetDexProvider(os.getenv("SOL_RPC_URL"), self.jito_settings)
        
        # 3. Risk Management
        self.risk = RiskManager(self.settings['max_capital_usd'])

    async def scan_market(self, market):
        name = market['name']
        try:
            # 1. Ambil Data Parallel (Asynchronous)
            poly_book_task = self.poly.get_orderbook(market['poly_token_id'])
            sol_odds_task = self.betdex.get_price(market['betdex_market_pubkey'])
            
            poly_book, s_odds = await asyncio.gather(poly_book_task, sol_odds_task)

            if not poly_book or not s_odds: 
                return

            # 2. Cek Arbitrase Dasar (Top of Book)
            p_price = float(poly_book['asks'][0][0])
            is_arb, raw_profit = calculate_arb_opportunity(p_price, s_odds)

            if is_arb and raw_profit > self.settings['min_profit_threshold']:
                # 3. Analisis Kedalaman Pasar (Slippage Check)
                stake = kelly_criterion(self.settings['max_capital_usd'], p_price)
                effective_p = MarketDepthAnalyzer.calculate_effective_price(poly_book['asks'], stake)

                if effective_p:
                    _, final_profit = calculate_arb_opportunity(effective_p, s_odds)
                    
                    # 4. Validasi Akhir oleh Risk Manager
                    is_safe, msg = self.risk.validate_execution(final_profit)
                    if is_safe:
                        log_success(f"!!! PROFIT DITEMUKAN: {name} !!!")
                        log_success(f"Profit Bersih: {final_profit:.2%}")
                        log_success(f"Estimasi Stake: ${stake:.2f}")
                        
                        # 5. Eksekusi Jito Bundle
                        await self.execute_jito_trade(stake, market)
                    else:
                        log_info(f"[{name}] Peluang diabaikan: {msg}")

        except Exception as e:
            log_error(f"Error scanning {name}: {e}")

    async def execute_jito_trade(self, stake, market):
        """
        Menyiapkan transaksi dan mengirimkan bundle ke Jito Block Engine.
        """
        log_info(f"Menyiapkan Bundle Jito untuk {market['name']}...")
        
        # TIP yang akan dikirim (diambil dari config)
        tip_amount = self.jito_settings['default_tip_lamports']
        target_tip_account = self.jito_settings['jito_tip_account']
        
        log_info(f"Info Jito: Mengirim tip ke {target_tip_account} sebesar {tip_amount} lamports")

        # LOGIKA EKSEKUSI (SIMULASI):
        # b64_tx = self.build_transaction(stake, market) # Buat tx asli di sini
        # response = await self.betdex.send_jito_bundle([b64_tx])
        # log_success(f"Jito Bundle Sent: {response}")
        
        log_info("Eksekusi selesai (Mode Dry-Run Aktif).")

    async def start_scanning(self):
        log_info("Bot Arbitrase Jito-Ready Berjalan...")
        log_info(f"Konfigurasi Tip Account: {self.jito_settings['jito_tip_account']}")
        
        while True:
            tasks = [self.scan_market(m) for m in self.config['active_markets']]
            await asyncio.gather(*tasks)
            await asyncio.sleep(self.settings['check_interval_seconds'])
