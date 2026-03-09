"""
Обработчик команды /start (без обязательной подписки на канал).
"""
import asyncio
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from services import UserService
from config import settings

router = Router()
_LAST_MAIN_MENU_MESSAGES: dict[int, int] = {}
_LAST_SUBSCRIPTION_MESSAGES: dict[int, int] = {}
_LAST_BONUS_MESSAGES: dict[int, int] = {}


def get_main_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура под строкой ввода: Главное меню и подписка"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Main menu",icon_custom_emoji_id="5197269100878907942",style='primary')],
            [KeyboardButton(text="choose a subscription",icon_custom_emoji_id="5372980108493596586",style='primary')],
            [KeyboardButton(text="BONUS",icon_custom_emoji_id="5390823932376915757",style='primary')],
        ],
        resize_keyboard=True,
        input_field_placeholder="Choose an action..."
    )
    return keyboard


def get_main_menu_links_keyboard() -> InlineKeyboardMarkup:
    """Инлайн-кнопки под сообщением «Главное меню»: по 2 кнопки в ряд"""
    signal_link = (settings.SIGNAL_BOT_LINK or "https://t.me/signalpriv_bot").strip()
    if signal_link.startswith("@"):
        signal_link = "https://t.me/" + signal_link.lstrip("@")
    elif not signal_link.startswith("http"):
        signal_link = "https://t.me/" + signal_link.lstrip("@")
    landing_link = (settings.LANDING_URL or "http://89.169.2.206:4173/").strip()
    reviews_link = (settings.REVIEWS_CHANNEL or "https://t.me/futuresreviewsTom").strip()
    if not reviews_link.startswith("http"):
        reviews_link = "https://t.me/" + reviews_link.lstrip("@")
    support_username = (settings.OPERATOR_USERNAME or "ecoTomSawyer").strip().lstrip("@")
    support_link = f"https://t.me/{support_username}"
    # По 2 кнопки в ряд
    buttons = [
        [
            InlineKeyboardButton(text="Trading cabinet", callback_data="eco_system", icon_custom_emoji_id="5247066536551656212", style='primary'),
            InlineKeyboardButton(text="Why us", url=landing_link, icon_custom_emoji_id="5323745261997007354", style='primary'),
        ],
        [
            InlineKeyboardButton(text="Reviews", url=reviews_link, icon_custom_emoji_id="5377705435807619775", style='primary'),
            InlineKeyboardButton(text="Support", url=support_link, icon_custom_emoji_id="5819062970998590994", style='primary'),
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def _normalize_tg_link(raw: str) -> str:
    raw = (raw or "").strip()
    if not raw:
        return ""
    if raw.startswith("@"):
        return "https://t.me/" + raw.lstrip("@")
    if raw.startswith("http"):
        return raw
    return "https://t.me/" + raw.lstrip("@")


def get_ecosystem_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура экосистемы: пока 1 торговый бот + назад в меню."""
    trading_bot_link = _normalize_tg_link(settings.SIGNAL_BOT_LINK or "https://t.me/signalpriv_bot")
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Trading bot", url=trading_bot_link, style="danger", icon_custom_emoji_id="5300964257242829093")],
        [InlineKeyboardButton(text="Back to main menu", callback_data="back_main_menu", style="danger", icon_custom_emoji_id="5465368548702446780")],
    ])

MAIN_MENU_TEXT = """
📋 Main menu
"""


@router.message(Command("start"))
async def cmd_start(message: Message):
    """Обработчик /start: приветствие без проверки подписки на канал."""
    user_id = message.from_user.id

    user = UserService.get_or_create_user(
        telegram_id=user_id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
    )

    welcome_message_2 = (
    f"Our team and our bot don’t hand out free money that just falls into your hands\n\n"
    "<tg-emoji emoji-id=\"5474638166163988906\">🤖</tg-emoji> The bot is NOT a MONEY button\n\n"
    "It’s a shovel you can use to actually dig out that profit\n\n"
)

    welcome_message_1 = (
        f"👋 Hello, {message.from_user.first_name}!\n\n"
        "I’m an AI-based trading bot that works together with 15 top traders. They know what to do to make money on the market in 2026.\n\n"
    )
    await message.answer(welcome_message_1, parse_mode="HTML")
    await asyncio.sleep(1)

    await message.answer(welcome_message_2, parse_mode="HTML")
    await asyncio.sleep(1)

    welcome_message_3 = ( '<tg-emoji emoji-id="5285005584700025090">📈</tg-emoji> '
    'I analyze the market in real time, taking into account all the key parameters\n\n'
    'In 2026, we assume the market is heavily driven and manipulated by big players. '
    'Our bot tracks the activity of all major whales 🐳 in its database. '
    'As a result, you get instant, up-to-date signals with a high probability of playing out'
)

    await message.answer(welcome_message_3, parse_mode="HTML")
    await asyncio.sleep(1)
       
    welcome_message_4 = (f"Trading with TomSawyer is a journey you go through together with the rest of the community\n\n"
    "When you make money - we make money too\n\n")

    await message.answer(welcome_message_4, parse_mode="HTML", reply_markup=get_main_keyboard())



@router.message(lambda message: message.text == "Main menu")
async def main_menu(message: Message):
    """Главное меню: текст и инлайн-кнопки со ссылками (Trading cabinet, Why us, Reviews, Support)"""
    chat_id = message.chat.id

    # Удаляем предыдущее сообщение главного меню, чтобы не плодить дубликаты
    last_msg_id = _LAST_MAIN_MENU_MESSAGES.get(chat_id)
    if last_msg_id:
        try:
            await message.bot.delete_message(chat_id=chat_id, message_id=last_msg_id)
        except Exception:
            pass

    # По возможности удаляем служебное сообщение пользователя "Main menu"
    try:
        await message.delete()
    except Exception:
        pass

    sent = await message.bot.send_message(
        chat_id=chat_id,
        text=MAIN_MENU_TEXT,
        reply_markup=get_main_menu_links_keyboard(),
        parse_mode="HTML",
    )
    _LAST_MAIN_MENU_MESSAGES[chat_id] = sent.message_id


@router.callback_query(F.data == "eco_system")
async def cb_eco_system(callback: CallbackQuery):
    """Экосистема (Trading cabinet): текст + кнопки с торговыми ботами."""
    await callback.answer()
    # Удаляем предыдущее сообщение "Main menu" с инлайн-кнопками
    try:
        await callback.message.delete()
    except Exception:
        pass
    text = (
        "<tg-emoji emoji-id=\"5359594091296335780\">🤖</tg-emoji><b> Trading cabinet ecosystem</b>\n\n"
    )
    await callback.message.answer(text, reply_markup=get_ecosystem_keyboard(), parse_mode="HTML")


@router.callback_query(F.data == "back_main_menu")
async def cb_back_main_menu(callback: CallbackQuery):
    await callback.answer()
    # Удаляем сообщение экосистемы перед возвратом в главное меню
    try:
        await callback.message.delete()
    except Exception:
        pass
    await callback.message.answer(MAIN_MENU_TEXT, reply_markup=get_main_menu_links_keyboard(), parse_mode="HTML")


@router.message(lambda message: message.text == "choose a subscription")
async def buy_subscription(message: Message):
    """📈 choose a subscription — актуальный баланс и 3 тарифа: $24/мес, $100/6 мес, $200/год"""
    chat_id = message.chat.id

    # Удаляем предыдущее сообщение с тарифами в этом чате
    last_msg_id = _LAST_SUBSCRIPTION_MESSAGES.get(chat_id)
    if last_msg_id:
        try:
            await message.bot.delete_message(chat_id=chat_id, message_id=last_msg_id)
        except Exception:
            pass

    # Пытаемся удалить сообщение пользователя "choose a subscription"
    try:
        await message.delete()
    except Exception:
        pass

    user = UserService.get_user_by_telegram_id(message.from_user.id)
    balance = float(user["balance"]) if user else 0.0

    text = (
        f"📈 Choose a subscription\n\n"
        f"💰 Your balance: {balance:.2f} USD\n\n"
        f"Select a plan:"
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="$24 | month", callback_data="pay_24", style='danger')],
        [InlineKeyboardButton(text="$100 | 6 months", callback_data="pay_100", style='danger')],
        [InlineKeyboardButton(text="$200 | year", callback_data="pay_200", style='danger')],
    ])
    sent = await message.bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=keyboard,
        parse_mode="HTML",
    )
    _LAST_SUBSCRIPTION_MESSAGES[chat_id] = sent.message_id


GPT_BONUS_BOT_LINK = "https://t.me/GPTBonus_bot"


@router.message(lambda message: message.text == "BONUS")
async def bonus(message: Message):
    """Bonus: текст про AI Scanner + цветная кнопка в бонус-бота."""
    chat_id = message.chat.id

    # Стараемся не создавать «мусор»: удаляем предыдущее бонус-сообщение, если оно было
    last_msg_id = _LAST_BONUS_MESSAGES.get(chat_id)
    if last_msg_id:
        try:
            await message.bot.delete_message(chat_id=chat_id, message_id=last_msg_id)
        except Exception:
            pass

    # По возможности удаляем служебное сообщение пользователя с текстом BONUS
    try:
        await message.delete()
    except Exception:
        pass

    text = (
        "<b><tg-emoji emoji-id=\"5474638166163988906\">🤖</tg-emoji> TomSawyer AI Scanner</b>\n\n"
        "AI chart analysis tool for traders\n\n"
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(icon_custom_emoji_id="5206473031110631274", text="AI Chart Scanner", url=GPT_BONUS_BOT_LINK, style="primary")],
    ])
    sent = await message.bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard, parse_mode="HTML")
    _LAST_BONUS_MESSAGES[chat_id] = sent.message_id

