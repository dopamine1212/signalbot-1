"""
Entry point for bot 2 (signals + broadcast).
Run: cd signal-bot-2 && python3 main.py
Ensure .env exists in signal-bot-2 with BOT_TOKEN and DATABASE_URL.
"""
import asyncio
from bot import main

if __name__ == "__main__":
    asyncio.run(main())
