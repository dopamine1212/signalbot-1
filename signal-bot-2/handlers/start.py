"""
Welcome and subscription check from shared DB.
"""
import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.exceptions import TelegramBadRequest
from database import get_subscription_status
from config import settings

logger = logging.getLogger(__name__)

router = Router()

# Кнопка «Go to main menu» всегда ведёт на этого бота (не на signalcryptobot)
MAIN_MENU_BOT_URL = "https://t.me/futures_signalfast_bot"


def is_user_premium(telegram_id: int) -> bool:
    """Проверка подписки: каждый раз новое подключение к БД — всегда актуальные данные (в т.ч. после правок в Supabase или оплаты в первом боте)."""
    is_premium, is_active = get_subscription_status(telegram_id)
    return is_premium and is_active


def get_welcome_text(premium: bool) -> str:
    """Welcome text with subscription status block (HTML)."""
    if premium:
        return (
            "<b>Welcome to Tom Sawyer signals bot</b>\n\n"
            "Access status: <tg-emoji emoji-id=\"5212932275376759608\">✅</tg-emoji> Active\n\n"
            "You will receive trading signals here with pinned messages.\n\n"
            "No commands needed — just wait for the updates."
        )
    return (
        "<b>Welcome to Tom Sawyer signals bot</b>\n\n"
        "Access status: <tg-emoji emoji-id=\"5280950568636917742\">❎</tg-emoji> Inactive\n\n"
        "<b><tg-emoji emoji-id=\"5305772219727642933\">🔒</tg-emoji> Access is restricted</b>\n\n"
        "To activate signals, purchase a subscription in the main bot. After payment you will automatically receive full access to the signal system."
    )


def get_start_keyboard() -> InlineKeyboardMarkup:
    """«Check subscription» button under the welcome message."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔄 Check subscription", callback_data="check_subscription")]
        ]
    )


@router.message(Command("start"), F.text)
@router.message(Command("start"))
async def cmd_start(message: Message):
    """Welcome: subscription status block and check subscription button."""
    user_id = message.from_user.id if message.from_user else 0
    if not user_id:
        return

    premium = is_user_premium(user_id)
    text = get_welcome_text(premium)

    keyboard = get_start_keyboard()
    if not premium:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🔄 Check subscription", callback_data="check_subscription")],
                [InlineKeyboardButton(text="📲 Go to main menu", url=MAIN_MENU_BOT_URL)],
            ]
        )

    await message.answer(text, reply_markup=keyboard, parse_mode="HTML")


@router.callback_query(F.data == "check_subscription")
async def cb_check_subscription(callback: CallbackQuery):
    """On «Check subscription» press — re-check DB and answer."""
    user_id = callback.from_user.id if callback.from_user else 0
    if not user_id:
        try:
            await callback.answer()
        except TelegramBadRequest:
            pass
        return

    premium = is_user_premium(user_id)
    text = "✅ Subscription is active." if premium else "❌ Subscription is not active. Get a subscription in the main bot."
    try:
        await callback.answer(text, show_alert=True)
    except TelegramBadRequest:
        # Query too old or invalid — answer expired, do not re-raise
        logger.debug("callback.answer failed (query expired or invalid)")
        pass
