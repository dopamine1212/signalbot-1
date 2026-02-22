"""
Основной файл бота. Бот запускается сразу, БД инициализируется в фоне — не «висит» при старте.
Совместимость со старым aiogram (без DefaultBotProperties) и увеличенный таймаут запросов к Telegram.
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
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def _init_db_background():
    try:
        init_db()
        logger.info("База данных инициализирована")
    except Exception as e:
        logger.exception("Ошибка инициализации БД: %s", e)


def _make_bot():
    """Бот: поддерживаются старый и новый aiogram (3.2+ с DefaultBotProperties)."""
    try:
        from aiogram.client.default import DefaultBotProperties
        return Bot(
            token=settings.BOT_TOKEN,
            default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
        )
    except ImportError:
        logger.warning(
            "Установите aiogram>=3.2 для Markdown по умолчанию: pip install -U 'aiogram>=3.2'"
        )
        return Bot(token=settings.BOT_TOKEN)


async def main():
    """Бот стартует сразу; БД в фоне; таймаут запросов к Telegram 60 сек."""
    t = threading.Thread(target=_init_db_background, daemon=True)
    t.start()
    await asyncio.sleep(2)

    bot = _make_bot()
    dp = Dispatcher()
    dp.include_router(handlers.router)
    logger.info("Бот запущен")
    await dp.start_polling(bot, request_timeout=60)


if __name__ == "__main__":
    asyncio.run(main())
