# providers/polymarket.py
import httpx

class PolymarketProvider:
    def __init__(self):
        self.base_url = "https://clob.polymarket.com"

    async def get_market_data(self, token_id):
        async with httpx.AsyncClient() as client:
            # Mengambil Order Book untuk melihat kedalaman (Depth)
            resp = await client.get(f"{self.base_url}/book?token_id={token_id}")
            data = resp.json()
            
            # Kita ambil harga 'Ask' terbaik (harga termurah untuk kita beli YES)
            if data['asks']:
                return float(data['asks'][0]['price'])
            return None
