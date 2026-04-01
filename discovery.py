import httpx
import json

async def discover():
    print("[*] Fetching trending markets from Polymarket...")
    resp = httpx.get("https://clob.polymarket.com/markets")
    markets = resp.json()
    # Logic untuk filter dan simpan ke config.json
    print("[+] Discovery finished.")

if __name__ == "__main__":
    import asyncio
    asyncio.run(discover())
