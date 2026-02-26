"""
Телеграм-бот анализа графиков на aiogram.
Принимает скриншоты графиков, отправляет в GPT Vision и возвращает текстовый анализ.
"""
import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message

from config import (
    ALLOWED_DOCUMENT_EXTENSIONS,
    ALLOWED_DOCUMENT_MIMES,
    TELEGRAM_BOT_TOKEN,
)
from gpt_client import analyze_chart

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

# --- Сообщения по ТЗ ---
# 1. Запуск /start
MSG_START = """👋 Hi!

🤖 I analyze trading charts using AI.

📸 Send me a screenshot of a chart, and I will return a clear text analysis:
trend, key levels, and possible scenarios"""

# 2. Пользователь отправил не изображение
MSG_NOT_IMAGE = "❌ Please send a screenshot of a trading chart"

# 3. Получение изображения — сразу после отправки фото/файла
MSG_CHART_RECEIVED = """✅ Chart received.

🔎 Analyzing the chart now…
This may take a few seconds"""

# 6. График плохого качества / GPT не понимает
MSG_CANT_READ = """⚠️ I can't read the chart clearly.
Please send a clearer screenshot with:
– the asset name
– the timeframe
– visible candles (zoom in)"""

# 7. После ответа — можно отправить ещё график
MSG_ANOTHER_CHART = "📸 You can send another chart whenever you're ready."

# 8. Ошибка GPT API или другая ошибка
MSG_API_ERROR = """❌ Something went wrong while analyzing the chart.
Please try again in a moment."""

UNREADABLE_MARKER = "UNREADABLE_CHART"


async def get_image_bytes(message: Message) -> bytes | None:
    """Скачивает изображение из сообщения (фото или документ) и возвращает bytes."""
    downloadable = None
    if message.photo:
        downloadable = message.photo[-1]  # максимальное разрешение
    elif message.document:
        downloadable = message.document

    if not downloadable:
        return None

    bio = await bot.download(downloadable)
    if bio is None:
        return None
    return bio.read()


def is_allowed_document(message: Message) -> bool:
    """Проверяет, что документ — допустимое изображение (PNG/JPG)."""
    if not message.document:
        return False
    doc = message.document
    if doc.mime_type and doc.mime_type.lower() in ALLOWED_DOCUMENT_MIMES:
        return True
    if doc.file_name:
        ext = "." + doc.file_name.rsplit(".", 1)[-1].lower() if "." in doc.file_name else ""
        if ext in ALLOWED_DOCUMENT_EXTENSIONS:
            return True
    return False


def is_start_command(message: Message) -> bool:
    """Проверяет, что сообщение — команда /start (с параметрами или без)."""
    if not message.text:
        return False
    text = message.text.strip()
    return text == "/start" or text.startswith("/start ")


@dp.message(F.func(is_start_command))
async def cmd_start(message: Message) -> None:
    await message.answer(MSG_START)


@dp.message(F.photo)
async def on_photo(message: Message) -> None:
    await message.answer(MSG_CHART_RECEIVED)
    image_bytes = await get_image_bytes(message)
    if not image_bytes:
        await message.answer(MSG_API_ERROR)
        await message.answer(MSG_ANOTHER_CHART)
        return

    result = await analyze_chart(image_bytes)
    if result is None:
        await message.answer(MSG_API_ERROR)
    elif result.strip().upper() == UNREADABLE_MARKER.upper():
        await message.answer(MSG_CANT_READ)
    else:
        await message.answer(result)
    await message.answer(MSG_ANOTHER_CHART)


@dp.message(F.document)
async def on_document(message: Message) -> None:
    if not is_allowed_document(message):
        await message.answer(MSG_NOT_IMAGE)
        return

    await message.answer(MSG_CHART_RECEIVED)
    image_bytes = await get_image_bytes(message)
    if not image_bytes:
        await message.answer(MSG_API_ERROR)
        await message.answer(MSG_ANOTHER_CHART)
        return

    result = await analyze_chart(image_bytes)
    if result is None:
        await message.answer(MSG_API_ERROR)
    elif result.strip().upper() == UNREADABLE_MARKER.upper():
        await message.answer(MSG_CANT_READ)
    else:
        await message.answer(result)
    await message.answer(MSG_ANOTHER_CHART)


@dp.message()
async def on_other(message: Message) -> None:
    """Любое сообщение не фото/документ — просим отправить скриншот."""
    await message.answer(MSG_NOT_IMAGE)


async def main() -> None:
    if not TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN не задан. Создайте файл .env")
        return
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
