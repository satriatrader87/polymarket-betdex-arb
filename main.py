# main.py
import asyncio
from core.orchestrator import ArbOrchestrator

async def main():
    # Inisialisasi Orchestrator
    bot = ArbOrchestrator()
    
    # Jalankan proses scanning
    try:
        await bot.start_scanning()
    except KeyboardInterrupt:
        print("\n🛑 Bot dihentikan oleh pengguna.")

if __name__ == "__main__":
    asyncio.run(main())
