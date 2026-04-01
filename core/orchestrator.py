# core/orchestrator.py

import asyncio
import json
import os
from dotenv import load_dotenv

# Import internal modules
from core.logger import log_info, log_success, log_error
from engine.calculator import calculate_arb_opportunity, kelly_criterion
from engine.risk_manager import RiskManager
from engine.market_depth import MarketDepthAnalyzer
from providers.polymarket import PolymarketProvider
from providers.betdex import BetDexProvider

load_dotenv()

class ArbOrchestrator:
    def __init__(self):
        # 1. Load Konfigurasi dari config.json
        self.config = self._load_config()
        self.settings = self.config['bot_settings']
        
        # 2. Inisialisasi Provider
        self.poly = PolymarketProvider(os.getenv("POLY_RPC_URL"))
        self.betdex = BetDexProvider(os.getenv("SOL_RPC_URL"))
        
        # 3. Inisialisasi Risk Manager
        self.risk = RiskManager(self.settings['max_capital_usd'])
        
        # 4. Status saldo simulasi/asli
        self.current_balance = self.settings['max_capital_usd']

    def _load_config(self):
        try:
            with open('config.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            log_error("config.json tidak ditemukan! Jalankan discovery.py terlebih dahulu.")
            exit(1)

    async def scan_market(self, market):
        """Fungsi tunggal untuk memproses satu market"""
        name = market['name']
        poly_id = market['poly_token_id']
        sol_pubkey = market['betdex_market_pubkey']

        try:
            # Ambil data Orderbook/Price secara paralel untuk kecepatan
            # Polymarket return Orderbook, BetDEX return Best Odds
            poly_data_task = self.poly.get_orderbook(poly_id) 
            sol_odds_task = self.betdex.get_price(sol_pubkey)
            
            poly_book, s_odds = await asyncio.gather(poly_data_task, sol_odds_task)

            if not poly_book or not s_odds:
                return

            # Ambil harga terbaik dari top of the book Polymarket
            p_price = float(poly_book['asks'][0][0]) 

            # 1. Hitung Peluang Arbitrase Dasar
            is_arb, raw_profit = calculate_arb_opportunity(p_price, s_odds)

            if is_arb and raw_profit > self.settings['min_profit_threshold']:
                # 2. Hitung Modal Aman (Kelly Criterion)
                stake = kelly_criterion(self.current_balance, p_price)
                
                # 3. Analisis Kedalaman Pasar (Slippage Check)
                # Menghitung harga rata-rata jika kita membeli sebesar 'stake'
                effective_p = MarketDepthAnalyzer.calculate_effective_price(poly_book['asks'], stake)
                
                if not effective_p:
                    log_info(f"[{name}] Arb ditemukan tapi likuiditas Polymarket terlalu tipis.")
                    return

                # Re-kalkulasi profit dengan harga efektif (setelah slippage)
                _, final_profit = calculate_arb_opportunity(effective_p, s_odds)

                # 4. Validasi Akhir oleh Risk Manager
                is_safe, msg = self.risk.validate_execution(final_profit)
                
                if is_safe:
                    log_success(f"!!! ARB DETECTED !!!")
                    log_success(f"Match: {name}")
                    log_success(f"Profit Bersih: {final_profit:.2%}")
                    log_success(f"Eksekusi: Beli YES di Poly @{effective_p:.3f} | Beli NO di Solana")
                    log_success(f"Estimasi Stake: ${stake:.2f}")
                    
                    # TODO: await self.execute_atomic_trade(stake, market)
                else:
                    log_info(f"[{name}] Peluang diabaikan: {msg}")

        except Exception as e:
            log_error(f"Kesalahan saat scan {name}: {e}")

    async def start_scanning(self):
        log_info("Bot Started. Menggunakan struktur Profesional & Aman.")
        log_info(f"Target Profit: >{self.settings['min_profit_threshold']*100}%")
        
        while True:
            # Menjalankan scan untuk semua market di config secara bersamaan
            tasks = [self.scan_market(m) for m in self.config['active_markets']]
            await asyncio.gather(*tasks)
            
            # Delay antar scan sesuai config
            await asyncio.sleep(self.settings['check_interval_seconds'])

    async def execute_atomic_trade(self, stake, market):
        """
        Fungsi masa depan untuk eksekusi real (Polygon & Solana Jito Bundle)
        """
        log_info("Mengirim transaksi atomik ke Polygon dan Solana...")
        # Implementasi integrasi Wallet & Jito di sini
        pass
