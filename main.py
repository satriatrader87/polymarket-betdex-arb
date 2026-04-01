import asyncio
from core.orchestrator import ArbOrchestrator

async def main():
    bot = ArbOrchestrator()
    try:
        await bot.start_scanning()
    except KeyboardInterrupt:
        print("\n[!] Bot stopped by user.")

if __name__ == "__main__":
    asyncio.run(main())
