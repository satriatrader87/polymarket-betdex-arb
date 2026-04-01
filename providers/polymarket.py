# providers/polymarket.py
import httpx
from .base import BaseProvider

class PolymarketProvider(BaseProvider):
    def __init__(self, rpc_url):
        self.rpc_url = rpc_url
        # Endpoint CLOB (Central Limit Order Book)
        self.api_url = "https://clob.polymarket.com/book"

    async def get_orderbook(self, token_id):
        """
        Mengambil seluruh buku perintah (Orderbook) untuk analisis kedalaman.
        Bukan hanya satu harga teratas.
        """
        try:
            async with httpx.AsyncClient() as client:
                # Memanggil API Polymarket untuk mendapatkan bid & ask
                params = {"token_id": token_id}
                resp = await client.get(self.api_url, params=params)
                
                if resp.status_code != 200:
                    return None
                
                data = resp.json()
                
                # Kita kembalikan format yang rapi untuk diolah MarketDepthAnalyzer
                return {
                    "asks": data.get('asks', []), # Format: [[price, size], [price, size]...]
                    "bids": data.get('bids', [])
                }
        except Exception as e:
            # Di mode produksi, sebaiknya log error ini ke file log
            return None

    async def get_price(self, token_id):
        """
        Fungsi simpel jika hanya butuh harga teratas (Legacy support)
        """
        book = await self.get_orderbook(token_id)
        if book and book['asks']:
            return float(book['asks'][0]['price'])
        return None
