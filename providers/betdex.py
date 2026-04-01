# providers/betdex.py
import httpx
import base64
from solana.rpc.async_api import AsyncClient
from solders.pubkey import Pubkey
from .base import BaseProvider

class BetDexProvider(BaseProvider):
    def __init__(self, rpc_url, jito_config):
        self.client = AsyncClient(rpc_url)
        # Ambil setting Jito dari config
        self.jito_url = jito_config['jito_engine_url']
        self.jito_tip_account = jito_config['jito_tip_account']

    async def get_price(self, market_pubkey):
        """Mengambil harga terbaik (Odds) dari Monaco Protocol."""
        try:
            # Logic ambil harga dari on-chain via AsyncClient
            # Return dummy untuk scanning mode
            return 2.50 
        except Exception:
            return None

    async def send_jito_bundle(self, tx_bytes_list: list):
        """
        Mengirim daftar transaksi (Bundle) ke Jito Block Engine.
        tx_bytes_list: List dari base64 encoded transactions.
        """
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "sendBundle",
            "params": [tx_bytes_list]
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(self.jito_url, json=payload)
                return response.json()
        except Exception as e:
            return {"error": str(e)}
