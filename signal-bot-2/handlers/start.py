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
from .admin import _delete_pin_system_notification

logger = logging.getLogger(__name__)

router = Router()

# Кнопка «Go to main menu» ведёт на основной бот @TomSawyerHub_bot — из config.MAIN_BOT_LINK


def is_user_premium(telegram_id: int) -> bool:
    """Проверка подписки: каждый раз новое подключение к БД — всегда актуальные данные (в т.ч. после правок в Supabase или оплаты в первом боте)."""
    is_premium, is_active = get_subscription_status(telegram_id)
    return is_premium and is_active


def get_welcome_text(premium: bool) -> str:
    """Welcome text with subscription status block (HTML)."""
    if premium:
        return (
            "<tg-emoji emoji-id=\"5890911279870119913\">❤️</tg-emoji> TOM SAWYER AI BOT - NOW LIVE\n\n"
            "The bot is active <tg-emoji emoji-id=\"5278628026416909103\">✅</tg-emoji>\n"
            "Turn on notifications and get ready for signals <tg-emoji emoji-id=\"5393389505321395092\">🔼</tg-emoji>\n\n"
            "<blockquote>We provide the entries - you take the profit</blockquote>\n\n"
            "<tg-emoji emoji-id=\"5471873663219284417\">💰</tg-emoji> <i>After each successful trade</i>, a 50% profit share is required\n\n"
            "For sending your share & support - contact us directly @ecoTomSawyer"
        )
    return (
        "<b>Welcome to Tom Sawyer signals bot</b>\n\n"
        "Access status: <tg-emoji emoji-id=\"5280950568636917742\">❎</tg-emoji> Inactive\n\n"
        "<b><tg-emoji emoji-id=\"5305772219727642933\">🔒</tg-emoji> Access is restricted</b>\n\n"
        "To activate signals, purchase a subscription in the main bot. After payment you will automatically receive full access to the signal system."
    )


def get_start_keyboard() -> InlineKeyboardMarkup:
    """Keyboard under the welcome message for non-premium users."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(icon_custom_emoji_id="5465226866321268133", text="Go to main menu", url=settings.MAIN_BOT_LINK, style="primary")]
        ]
    )


@router.message(Command("start"), F.text)
@router.message(Command("start"))
async def cmd_start(message: Message):
    """Welcome: subscription status block."""
    user_id = message.from_user.id if message.from_user else 0
    if not user_id:
        return

    premium = is_user_premium(user_id)
    text = get_welcome_text(premium)

    keyboard = None
    if not premium:
        keyboard = get_start_keyboard()

    sent = await message.answer(text, reply_markup=keyboard, parse_mode="HTML")
    try:
        await message.bot.pin_chat_message(
            chat_id=message.chat.id,
            message_id=sent.message_id,
            disable_notification=True,
        )
        await _delete_pin_system_notification(
            chat_id=message.chat.id,
            pinned_message_id=sent.message_id,
            bot=message.bot,
        )
    except TelegramBadRequest:
        logger.debug("pin or delete pin notification failed", exc_info=True)


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
    try:
        if premium:
            await callback.answer("✅ Subscription is active.", show_alert=True)
        else:
            await callback.answer("❌ Subscription is not active. Get a subscription in the main bot.", show_alert=True)
    except TelegramBadRequest:
        logger.debug("callback.answer failed (query expired or invalid)")
