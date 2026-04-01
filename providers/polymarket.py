import httpx
from .base import BaseProvider

class PolymarketProvider(BaseProvider):
    def __init__(self, rpc_url):
        self.rpc_url = rpc_url
        self.api_url = "https://clob.polymarket.com/book"

    async def get_price(self, token_id):
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(f"{self.api_url}?token_id={token_id}")
                data = resp.json()
                if data.get('asks'):
                    return float(data['asks'][0]['price'])
            return None
        except Exception:
            return None
