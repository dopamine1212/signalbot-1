"""
Телеграм-бот анализа графиков на aiogram.
Принимает скриншоты графиков, отправляет в GPT Vision и возвращает текстовый анализ.
Обязательная подписка на канал (если задан REQUIRED_CHANNEL в .env).
Все сообщения отправляются с parse_mode="HTML".
"""
import asyncio
import html
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ChatMemberStatus

from config import (
    ALLOWED_DOCUMENT_EXTENSIONS,
    ALLOWED_DOCUMENT_MIMES,
    TELEGRAM_BOT_TOKEN,
    REQUIRED_CHANNEL,
)
from gpt_client import analyze_chart

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

# --- Сообщения по ТЗ (HTML) ---
# 1. Запуск /start
MSG_START = """This <b><tg-emoji emoji-id=\"5474638166163988906\">🤖</tg-emoji></b> AI tool is built inside the Tom Sawyer trading system

<b><tg-emoji emoji-id="5258205968025525531">📸</tg-emoji></b> Drop a chart screenshot and get:

- instant technical breakdown
- key price zones
- possible market scenarios

<b>Fast  Clear  Useful</b>"""

# 2. Пользователь отправил не изображение
MSG_NOT_IMAGE = "<b><tg-emoji emoji-id=\"5017122105011995219\">❌</tg-emoji></b> Please send a screenshot of a trading chart"

# 3. Получение изображения — сразу после отправки фото/файла
MSG_CHART_RECEIVED = """<b><tg-emoji emoji-id=\"5328194414323980905\">✅</tg-emoji></b> Chart received.

<b><tg-emoji emoji-id=\"5874960879434338403\">🔎</tg-emoji></b> Analyzing the chart now…
This may take a few seconds"""

# 6. График плохого качества / GPT не понимает
MSG_CANT_READ = """<b><tg-emoji emoji-id=\"5017122105011995219\">⚠️</tg-emoji></b> I can't read the chart clearly.
Please send a clearer screenshot with:
– the asset name
– the timeframe
– visible candles (zoom in)"""

# 7. После ответа — можно отправить ещё график
MSG_ANOTHER_CHART = "<b><tg-emoji emoji-id=\"5375309569905938163\">📸</tg-emoji></b> You can send another chart whenever you're ready."

# 8. Ошибка GPT API или другая ошибка
MSG_API_ERROR = """<b><tg-emoji emoji-id=\"5017122105011995219\">❌</tg-emoji></b> Something went wrong while analyzing the chart.
Please try again in a moment."""

UNREADABLE_MARKER = "UNREADABLE_CHART"

# Сообщение и кнопки при отсутствии подписки на канал
MSG_SUBSCRIBE = """<tg-emoji emoji-id=\"5253878470647243654\">👋</tg-emoji><b> Welcome to TomSawyer AI Scanner</b>

<b>This bot is your AI trading assistant</b>
It scans chart screenshots and provides a quick analysis of the market

To continue using the bot, please subscribe to our official channel<tg-emoji emoji-id=\"5240147597640876449\">💎</tg-emoji>

<tg-emoji emoji-id=\"5370781982886220096\">🎁</tg-emoji> The bot is currently free for early users. In the future, access will become paid for new users

After subscribing, tap"""
CHANNEL_LINK = f"https://t.me/{REQUIRED_CHANNEL}" if REQUIRED_CHANNEL else ""


async def check_channel_subscription(bot: Bot, user_id: int) -> bool:
    """Проверяет, подписан ли пользователь на обязательный канал."""
    if not REQUIRED_CHANNEL:
        return True
    try:
        member = await bot.get_chat_member(chat_id=f"@{REQUIRED_CHANNEL}", user_id=user_id)
        return member.status in (ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR)
    except Exception:
        return False


def get_subscribe_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(icon_custom_emoji_id="5215344475039084599",text="Subscribe to channel", style="primary",url=CHANNEL_LINK)],
        [InlineKeyboardButton(icon_custom_emoji_id="5212932275376759608",text="Check subscription", style="primary", callback_data="bonus_check_subscription")],
    ])


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
    if not await check_channel_subscription(message.bot, message.from_user.id):
        await message.answer(MSG_SUBSCRIBE, reply_markup=get_subscribe_keyboard(), parse_mode="HTML")
        return
    msg = await message.answer(MSG_START, parse_mode="HTML")
    try:
        await message.bot.pin_chat_message(chat_id=message.chat.id, message_id=msg.message_id, disable_notification=True)
    except Exception:
        pass  # в личке закрепление недоступно


@dp.callback_query(F.data == "bonus_check_subscription")
async def cb_check_subscription(callback: CallbackQuery) -> None:
    if not await check_channel_subscription(callback.bot, callback.from_user.id):
        await callback.answer("❌ Please subscribe to the channel first, then tap again.", show_alert=True)
        return
    await callback.answer("✅ Subscription confirmed. Thank you!")
    msg = await callback.message.answer(MSG_START, parse_mode="HTML")
    try:
        await callback.bot.pin_chat_message(chat_id=callback.message.chat.id, message_id=msg.message_id, disable_notification=True)
    except Exception:
        pass


@dp.message(F.photo)
async def on_photo(message: Message) -> None:
    if not await check_channel_subscription(message.bot, message.from_user.id):
        await message.answer(MSG_SUBSCRIBE, reply_markup=get_subscribe_keyboard(), parse_mode="HTML")
        return
    await message.answer(MSG_CHART_RECEIVED, parse_mode="HTML")
    image_bytes = await get_image_bytes(message)
    if not image_bytes:
        await message.answer(MSG_API_ERROR, parse_mode="HTML")
        await message.answer(MSG_ANOTHER_CHART, parse_mode="HTML")
        return

    result = await analyze_chart(image_bytes)
    if result is None:
        await message.answer(MSG_API_ERROR, parse_mode="HTML")
    elif result.strip().upper() == UNREADABLE_MARKER.upper():
        await message.answer(MSG_CANT_READ, parse_mode="HTML")
    else:
        await message.answer(html.escape(result), parse_mode="HTML")
    await message.answer(MSG_ANOTHER_CHART, parse_mode="HTML")


@dp.message(F.document)
async def on_document(message: Message) -> None:
    if not await check_channel_subscription(message.bot, message.from_user.id):
        await message.answer(MSG_SUBSCRIBE, reply_markup=get_subscribe_keyboard(), parse_mode="HTML")
        return
    if not is_allowed_document(message):
        await message.answer(MSG_NOT_IMAGE, parse_mode="HTML")
        return

    await message.answer(MSG_CHART_RECEIVED, parse_mode="HTML")
    image_bytes = await get_image_bytes(message)
    if not image_bytes:
        await message.answer(MSG_API_ERROR, parse_mode="HTML")
        await message.answer(MSG_ANOTHER_CHART, parse_mode="HTML")
        return

    result = await analyze_chart(image_bytes)
    if result is None:
        await message.answer(MSG_API_ERROR, parse_mode="HTML")
    elif result.strip().upper() == UNREADABLE_MARKER.upper():
        await message.answer(MSG_CANT_READ, parse_mode="HTML")
    else:
        await message.answer(html.escape(result), parse_mode="HTML")
    await message.answer(MSG_ANOTHER_CHART, parse_mode="HTML")


@dp.message()
async def on_other(message: Message) -> None:
    """Любое сообщение не фото/документ — проверка подписки и просим скриншот."""
    # Не реагируем на системные сообщения без текста
    if not message.text:
        return

    # Не дублируем ответы для /start и BONUS – их уже обработали отдельные хендлеры
    if is_start_command(message):
        return
    if message.text.strip().upper() == "BONUS":
        return

    if not await check_channel_subscription(message.bot, message.from_user.id):
        await message.answer(MSG_SUBSCRIBE, reply_markup=get_subscribe_keyboard(), parse_mode="HTML")
        return
    await message.answer(MSG_NOT_IMAGE, parse_mode="HTML")


async def main() -> None:
    if not TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN не задан. Создайте файл .env")
        return
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
