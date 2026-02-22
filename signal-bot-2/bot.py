"""
Bot 2: signals and broadcast. Shared Supabase DB with bot-1.
Run from signal-bot-2 folder. Requires .env with BOT_TOKEN and DATABASE_URL.
"""
import asyncio
import logging
import threading
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from config import settings
from database import init_db
import handlers

logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def _init_db_background():
    try:
        init_db()
        logger.info("Database initialized")
    except Exception as e:
        logger.exception("DB init failed: %s", e)


def _make_bot():
    try:
        from aiogram.client.default import DefaultBotProperties
        return Bot(
            token=settings.BOT_TOKEN,
            default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN),
        )
    except ImportError:
        return Bot(token=settings.BOT_TOKEN)


async def main():
    t = threading.Thread(target=_init_db_background, daemon=True)
    t.start()
    await asyncio.sleep(2)

    bot = _make_bot()
    dp = Dispatcher()
    dp.include_router(handlers.router)
    logger.info("Bot 2 started")
    await dp.start_polling(bot, request_timeout=60)


if __name__ == "__main__":
    asyncio.run(main())
