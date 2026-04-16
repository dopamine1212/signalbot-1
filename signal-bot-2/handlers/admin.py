"""
Bot 2 admin: send signals and broadcast only. Shared Supabase DB with main bot.
"""
import html
import json
import logging
import asyncio
from aiogram import Router, F
from aiogram.types import Message, InputMediaPhoto, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, LinkPreviewOptions
from aiogram.filters import Command, StateFilter
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from database import get_db
from services import AdminService, BanService
from config import settings

logger = logging.getLogger(__name__)

router = Router()


def build_signal_body(signal_text: str) -> str:
    """Return only the signal text, no header."""
    return (signal_text or "").strip()


def _h(s: str) -> str:
    """Escape for HTML (Telegram parse_mode=HTML)."""
    return html.escape(str(s))


async def _delete_pin_system_notification(chat_id: int, pinned_message_id: int, bot) -> None:
    """
    Best-effort удаление системного уведомления о закрепе.

    Telegram API не возвращает message_id сервисного сообщения после pin.
    На практике оно обычно идёт следующим id, поэтому пробуем удалить несколько ближайших.
    """
    for candidate_id in (pinned_message_id + 1, pinned_message_id + 2):
        try:
            await bot.delete_message(chat_id=chat_id, message_id=candidate_id)
            return
        except Exception:
            pass


# Шаблоны сигналов SHORT/LONG. Переменные задаёт админ. Отправляются с parse_mode=HTML.
# В начале #SIGNAL (ПАРА). Строка про OKX и % депозита убрана.
def build_short_signal(
    pair: str,
    price_low: str, price_high: str, leverage: str,
    target1: str, target2: str, target3: str, target4: str, target5: str,
    stop_loss: str = "",
) -> str:
    header = f"#SIGNAL ({_h(pair)})\n\n"
    stop_loss_line = f"\n\n❗️ STOP LOSS: ${_h(stop_loss)}" if stop_loss and stop_loss.strip() else ""
    return (
        header
        + f"<tg-emoji emoji-id=\"5283224689395640696\">📉</tg-emoji> Open <b>SHORT</b> <tg-emoji emoji-id=\"5472265471610856247\">⛔️</tg-emoji> at price between\n"
        f"${_h(price_low)} – ${_h(price_high)} with X{_h(leverage)} leverage\n\n"
        f"Targets:\n\n"
        f"1️⃣ Close the order at the price ${_h(target1)}\n"
        f"2️⃣ Close the order at the price ${_h(target2)}\n"
        f"3️⃣ Close the order at the price ${_h(target3)}\n"
        f"4️⃣ Close the order at the price ${_h(target4)}\n"
        f"5️⃣ Close the order at the price ${_h(target5)}\n\n"
        + stop_loss_line
    )


def build_long_signal(
    pair: str,
    price_low: str, price_high: str, leverage: str,
    target1: str, target2: str, target3: str, target4: str, target5: str,
    stop_loss: str = "",
) -> str:
    header = f"#SIGNAL ({_h(pair)})\n\n"
    stop_loss_line = f"\n\n❗️ STOP LOSS: ${_h(stop_loss)}" if stop_loss and stop_loss.strip() else ""
    return (
        header
        + f"<tg-emoji emoji-id=\"5298952911173205130\">📈</tg-emoji> Open <b>LONG</b> <tg-emoji emoji-id=\"5449660186853648911\">🔠</tg-emoji> at price between\n"
        f"${_h(price_low)} – ${_h(price_high)} with X{_h(leverage)} leverage\n\n"
        f"Targets:\n\n"
        f"1️⃣ Close the order at the price ${_h(target1)}\n"
        f"2️⃣ Close the order at the price ${_h(target2)}\n"
        f"3️⃣ Close the order at the price ${_h(target3)}\n"
        f"4️⃣ Close the order at the price ${_h(target4)}\n"
        f"5️⃣ Close the order at the price ${_h(target5)}\n\n"
        + stop_loss_line
    )


class SignalStates(StatesGroup):
    waiting_for_photos = State()
    waiting_for_signal_type = State()   # SHORT или LONG
    waiting_for_signal_vars = State()   # переменные для шаблона
    waiting_for_text = State()         # для Edit (повторный ввод)
    waiting_for_confirm = State()


class BroadcastStates(StatesGroup):
    waiting_for_text = State()
    waiting_for_link = State()


class NotificationStates(StatesGroup):
    waiting_for_time = State()


media_groups_storage = {}


def _summarize_groups_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Group 1", callback_data="summarize_group_1"),
            InlineKeyboardButton(text="✅ Group 2", callback_data="summarize_group_2"),
        ],
    ])


@router.message(Command("admin"))
@router.message(Command("admine"))
async def cmd_admin(message: Message):
    """Admin command list. No response for non-admins."""
    if not AdminService.is_admin(message.from_user.id):
        return
    admin_commands = """
👑 *Administrator (Bot 2):*

📢 *Signals & messages:*
`/send_signal` - Send signal (1-2 photos + text, Group 1 or 2)
`/send_message` - Send custom message to all users
`/send_notification` - Уведомление о времени сигнала (только премиум; время вводит админ)
`/summarize` - Подвести итоги по группе
`/ban_user <@username>` - Забанить пользователя
`/unban_user <@username>` - Разбанить пользователя
`/ban_list` - Список банов

Send /cancel to cancel any operation.
"""
    admin_panel_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📋 Подвести итоги", callback_data="open_summarize")]
    ])
    await message.answer(admin_commands, reply_markup=admin_panel_kb)


def _extract_username_arg(message: Message) -> str:
    args = (message.text or "").split(maxsplit=1)
    if len(args) < 2:
        return ""
    return args[1].strip().lstrip("@")


@router.message(Command("ban_user"))
async def cmd_ban_user(message: Message):
    if not AdminService.is_admin(message.from_user.id):
        return
    username = _extract_username_arg(message)
    if not username:
        await message.answer("❌ Usage: /ban_user <@username>")
        return
    ok, reason = BanService.ban_by_username(username, added_by=message.from_user.id)
    if ok:
        await message.answer(f"✅ User @{username.lower()} has been banned.")
    elif reason == "already_banned":
        await message.answer(f"⚠️ User @{username.lower()} is already banned.")
    else:
        await message.answer("❌ Failed to ban user. Check username.")


@router.message(Command("unban_user"))
async def cmd_unban_user(message: Message):
    if not AdminService.is_admin(message.from_user.id):
        return
    username = _extract_username_arg(message)
    if not username:
        await message.answer("❌ Usage: /unban_user <@username>")
        return
    if BanService.unban_by_username(username):
        await message.answer(f"✅ User @{username.lower()} has been unbanned.")
    else:
        await message.answer(f"⚠️ User @{username.lower()} is not in ban list.")


@router.message(Command("ban_list"))
async def cmd_ban_list(message: Message):
    if not AdminService.is_admin(message.from_user.id):
        return
    bans = BanService.get_all_bans()
    if not bans:
        await message.answer("📋 Ban list is empty.")
        return
    lines = ["🚫 Banned users:\n"]
    for idx, row in enumerate(bans, 1):
        uname = row.get("username") or "unknown"
        tg_id = row.get("telegram_id")
        if tg_id:
            lines.append(f"{idx}. @{uname} (id: {tg_id})")
        else:
            lines.append(f"{idx}. @{uname}")
    await message.answer("\n".join(lines), parse_mode=None)


@router.message(Command("summarize"))
async def cmd_summarize(message: Message):
    """Подвести итоги: выбор группы, у которой прогноз зашёл."""
    if not AdminService.is_admin(message.from_user.id):
        return
    await message.answer(
        "📋 Подвести итоги\n\nВыберите группу, у которой прогноз сработал:",
        reply_markup=_summarize_groups_keyboard(),
        parse_mode=None,
    )


@router.callback_query(F.data == "open_summarize")
async def cb_open_summarize(callback: CallbackQuery):
    if not AdminService.is_admin(callback.from_user.id):
        return
    await callback.answer()
    await callback.message.answer(
        "📋 Подвести итоги\n\nВыберите группу, у которой прогноз сработал:",
        reply_markup=_summarize_groups_keyboard(),
        parse_mode=None,
    )


@router.callback_query(F.data.startswith("summarize_group_"))
async def cb_summarize_group(callback: CallbackQuery):
    """Показать список юзеров выбранной группы (прогноз зашёл)."""
    if not AdminService.is_admin(callback.from_user.id):
        return
    try:
        group = int(callback.data.replace("summarize_group_", ""))
    except ValueError:
        group = 1
    if group not in (1, 2):
        group = 1

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT telegram_id, username, first_name, last_name
        FROM users
        WHERE split_group = ? AND is_premium = 1 AND is_active = 1
        ORDER BY id
        """,
        (group,),
    )
    rows = cursor.fetchall()

    if not rows:
        text = f"📋 Группа {group} — прогноз зашёл\n\nСписок пуст (нет активных премиум-пользователей в этой группе)."
        try:
            await callback.message.edit_text(text, parse_mode=None)
        except Exception:
            await callback.message.answer(text, parse_mode=None)
        await callback.answer()
        return

    header = f"📋 Группа {group} — прогноз зашёл\n\nВсего: {len(rows)} чел.\n"
    chunks = [header]
    for i, row in enumerate(rows, 1):
        uid = row[0]
        username = row[1] or ""
        first_name = (row[2] or "").strip()
        last_name = (row[3] or "").strip()
        name = f"{first_name} {last_name}".strip() or "—"
        uname = f"@{username}" if username else ""
        line = f"{i}. ID: {uid} | {uname} | {name}"
        if len(chunks[-1]) + len(line) + 1 > 4000:
            chunks.append(line)
        else:
            chunks[-1] += "\n" + line

    for j, chunk in enumerate(chunks):
        try:
            if j == 0:
                await callback.message.edit_text(chunk, parse_mode=None)
            else:
                await callback.message.answer(chunk, parse_mode=None)
        except Exception:
            await callback.message.answer(chunk, parse_mode=None)
    await callback.answer()


@router.message(Command("send_notification"))
async def cmd_send_notification(message: Message, state: FSMContext):
    """Уведомление по шаблону NOTIFICATION_TEMPLATE; подставляется только {time}; получатели — активный премиум."""
    if not AdminService.is_admin(message.from_user.id):
        return
    template = (settings.NOTIFICATION_TEMPLATE or "").strip()
    if not template:
        await message.answer("❌ NOTIFICATION_TEMPLATE пустой. Заполните в config.py или .env")
        return
    if "{time}" not in template:
        await message.answer(
            "❌ В NOTIFICATION_TEMPLATE должен быть плейсхолдер <code>{time}</code> "
            "(время подставляется из ответа админа).",
            parse_mode="HTML",
        )
        return
    await message.answer(
        "⏰ *Уведомление о сигнале*\n\n"
        "Отправьте время для строки «Today's signal is at … GMT+2» — это единственная переменная.\n"
        "Например: `15:30` или `3:30 PM`\n\n"
        "Отправьте /cancel для отмены."
    )
    await state.set_state(NotificationStates.waiting_for_time)


@router.message(StateFilter(NotificationStates.waiting_for_time), F.text)
async def process_notification_time(message: Message, state: FSMContext):
    if not AdminService.is_admin(message.from_user.id):
        return
    raw = (message.text or "").strip()
    if raw == "/cancel":
        await state.clear()
        await message.answer("❌ Отменено")
        return
    if raw.startswith("/"):
        await message.answer("Сначала введите время или отправьте /cancel")
        return
    time_str = raw
    if not time_str:
        await message.answer("Пусто. Введите время или /cancel")
        return
    template = (settings.NOTIFICATION_TEMPLATE or "").strip()
    text = template.replace("{time}", _h(time_str))
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT telegram_id FROM users WHERE is_premium = 1 AND is_active = 1"
    )
    users = [row[0] for row in cursor.fetchall()]
    sent = 0
    failed = 0
    for uid in users:
        try:
            await message.bot.send_message(
                chat_id=uid,
                text=text,
                parse_mode="HTML",
                link_preview_options=LinkPreviewOptions(is_disabled=True),
            )
            sent += 1
        except Exception as e:
            failed += 1
            logger.debug("Notification to %s: %s", uid, e)
    await state.clear()
    await message.answer(
        f"✅ Уведомление отправлено активным премиум-пользователям: {sent} доставлено, {failed} ошибок."
    )


@router.message(Command("send_message"))
async def cmd_send_message(message: Message, state: FSMContext):
    """Broadcast a message to all users (admin only)."""
    if not AdminService.is_admin(message.from_user.id):
        return
    await message.answer(
        "📝 *Send message*\n\n"
        "Send the text of the message to be sent to all users.\n\n"
        "Send /cancel to cancel."
    )
    await state.set_state(BroadcastStates.waiting_for_text)


@router.message(StateFilter(BroadcastStates.waiting_for_text), F.text)
async def process_broadcast_text(message: Message, state: FSMContext):
    if message.text and message.text.strip() == "/cancel":
        await state.clear()
        await message.answer("❌ Cancelled")
        return
    await state.update_data(broadcast_text=message.text)
    await state.set_state(BroadcastStates.waiting_for_link)
    await message.answer(
        "📎 *Add link?*\n\n"
        "Send a URL (e.g. https://t.me/...) to add a button under the message.\n"
        "Or send /skip to send the message without a button."
    )


def _is_url(s: str) -> bool:
    s = (s or "").strip()
    return s.startswith("http://") or s.startswith("https://")


@router.message(StateFilter(BroadcastStates.waiting_for_link), F.text)
async def process_broadcast_link(message: Message, state: FSMContext):
    if message.text and message.text.strip() == "/cancel":
        await state.clear()
        await message.answer("❌ Cancelled")
        return
    data = await state.get_data()
    text = data.get("broadcast_text", "")
    reply_markup = None
    if message.text and message.text.strip().lower() != "/skip":
        raw = message.text.strip()
        if _is_url(raw):
            reply_markup = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🔗 Open link", url=raw)]
            ])
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT telegram_id FROM users")
    users = [row[0] for row in cursor.fetchall()]
    sent = 0
    failed = 0
    for uid in users:
        try:
            await message.bot.send_message(
                chat_id=uid,
                text=text,
                parse_mode=None,
                reply_markup=reply_markup,
            )
            sent += 1
        except Exception as e:
            failed += 1
            logger.debug(f"Broadcast to {uid}: {e}")
    await state.clear()
    await message.answer(f"✅ Message sent: {sent} delivered, {failed} errors.")


@router.message(Command("send_signal"))
async def cmd_send_signal(message: Message, state: FSMContext):
    if not AdminService.is_admin(message.from_user.id):
        return
    await message.answer(
        "📸 *Send Signal*\n\n"
        "Send 1 or 2 photos, then choose SHORT or LONG and enter the template variables (one line, 10 numbers).\n\n"
        "Send /cancel to cancel"
    )
    await state.set_state(SignalStates.waiting_for_photos)


@router.message(StateFilter(SignalStates.waiting_for_photos), F.photo)
async def process_signal_photos(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if message.media_group_id:
        if message.media_group_id not in media_groups_storage:
            media_groups_storage[message.media_group_id] = {
                'user_id': user_id,
                'photo_ids': [],
                'state': state,
                'processed': False
            }
        photo_id = message.photo[-1].file_id
        if photo_id not in media_groups_storage[message.media_group_id]['photo_ids']:
            media_groups_storage[message.media_group_id]['photo_ids'].append(photo_id)
        photo_ids = media_groups_storage[message.media_group_id]['photo_ids'][:2]
        media_groups_storage[message.media_group_id]['photo_ids'] = photo_ids
        await asyncio.sleep(1.0)
        group_data = media_groups_storage.get(message.media_group_id)
        if group_data and not group_data['processed']:
            await state.update_data(photo_ids=photo_ids)
            media_groups_storage[message.media_group_id]['processed'] = True
            if len(photo_ids) > 2:
                await message.answer("⚠️ Only 2 photos accepted (maximum)")
            await message.answer(
                f"✅ Photos received ({len(photo_ids)} pcs.)!\n\n"
                "Choose signal type:"
            )
            await state.set_state(SignalStates.waiting_for_signal_type)
            kb = InlineKeyboardBuilder()
            kb.button(text="📉 SHORT", callback_data="signal_type_short")
            kb.button(text="📈 LONG", callback_data="signal_type_long")
            await message.answer(
                "SHORT or LONG?",
                reply_markup=kb.as_markup()
            )
            await asyncio.sleep(0.5)
            if message.media_group_id in media_groups_storage:
                del media_groups_storage[message.media_group_id]
        return

    data = await state.get_data()
    photo_ids = data.get("photo_ids", [])
    photo_id = message.photo[-1].file_id
    if photo_id not in photo_ids:
        photo_ids.append(photo_id)
    if len(photo_ids) > 2:
        photo_ids = photo_ids[:2]
        await message.answer("⚠️ Only 2 photos accepted (maximum)")
    await state.update_data(photo_ids=photo_ids)
    if len(photo_ids) >= 2:
        await message.answer(
            "✅ Photos received!\n\n"
            "Choose signal type:"
        )
        kb = InlineKeyboardBuilder()
        kb.button(text="📉 SHORT", callback_data="signal_type_short")
        kb.button(text="📈 LONG", callback_data="signal_type_long")
        await message.answer("SHORT or LONG?", reply_markup=kb.as_markup())
        await state.set_state(SignalStates.waiting_for_signal_type)
    else:
        await message.answer(
            f"✅ Photo {len(photo_ids)}/2 received!\n\n"
            "Send another photo or choose signal type below."
        )
        kb = InlineKeyboardBuilder()
        kb.button(text="📉 SHORT", callback_data="signal_type_short")
        kb.button(text="📈 LONG", callback_data="signal_type_long")
        await message.answer("SHORT or LONG?", reply_markup=kb.as_markup())
        await state.set_state(SignalStates.waiting_for_signal_type)


@router.message(StateFilter(SignalStates.waiting_for_photos), F.text)
async def process_signal_text_after_photo(message: Message, state: FSMContext):
    if message.text and message.text.strip() == "/cancel":
        await state.clear()
        await message.answer("❌ Signal sending cancelled")
        return
    data = await state.get_data()
    if not data.get("photo_ids"):
        await message.answer("⚠️ Send photos first!")
        return
    await message.answer("Choose signal type:")
    kb = InlineKeyboardBuilder()
    kb.button(text="📉 SHORT", callback_data="signal_type_short")
    kb.button(text="📈 LONG", callback_data="signal_type_long")
    await message.answer("SHORT or LONG?", reply_markup=kb.as_markup())
    await state.set_state(SignalStates.waiting_for_signal_type)


@router.message(StateFilter(SignalStates.waiting_for_signal_type), F.text)
async def process_signal_type_text(message: Message, state: FSMContext):
    if message.text and message.text.strip() == "/cancel":
        await state.clear()
        await message.answer("❌ Signal sending cancelled")
        return
    await message.answer("Нажмите кнопку 📉 SHORT или 📈 LONG выше.")

@router.callback_query(
    F.data.in_(["signal_type_short", "signal_type_long"]),
    StateFilter(SignalStates.waiting_for_signal_type),
)
async def process_signal_type(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.answer()
    except Exception:
        pass
    signal_type = "short" if callback.data == "signal_type_short" else "long"
    await state.update_data(signal_type=signal_type)
    await state.set_state(SignalStates.waiting_for_signal_vars)
    await callback.message.answer(
        "Введите данные <b>с новой строки</b> (каждое значение — отдельная строка):\n\n"
        "1. Пара (например MKR/USDT)\n"
        "2. Цена мин\n"
        "3. Цена макс\n"
        "4. Плечо\n"
        "5. Цель 1\n"
        "6. Цель 2\n"
        "7. Цель 3\n"
        "8. Цель 4\n"
        "9. Цель 5\n"
        "10. Стоп-лосс (опционально, можно пропустить)",
        parse_mode="HTML",
    )


@router.message(StateFilter(SignalStates.waiting_for_signal_vars), F.text)
async def process_signal_vars(message: Message, state: FSMContext):
    if message.text and message.text.strip() == "/cancel":
        await state.clear()
        await message.answer("❌ Signal sending cancelled")
        return
    # Ввод с новой строки: каждое значение — отдельная строка
    parts = [line.strip() for line in message.text.strip().splitlines() if line.strip()]
    if len(parts) not in (9, 10):
        await message.answer(
            "⚠️ Нужно 9 или 10 строк (каждое значение с новой строки):\n"
            "пара, цена-мин, цена-макс, плечо, цель1, цель2, цель3, цель4, цель5, [стоп-лосс].\n"
            "Попробуйте снова.",
            parse_mode=None,
        )
        return
    (
        pair, price_low, price_high, leverage,
        target1, target2, target3, target4, target5, stop_loss
    ) = parts if len(parts) == 10 else (*parts, "")
    data = await state.get_data()
    signal_type = data.get("signal_type", "short")
    if signal_type == "long":
        text = build_long_signal(
            pair, price_low, price_high, leverage,
            target1, target2, target3, target4, target5, stop_loss,
        )
    else:
        text = build_short_signal(
            pair, price_low, price_high, leverage,
            target1, target2, target3, target4, target5, stop_loss,
        )
    await state.update_data(text=text)
    await show_signal_preview(message, state)


@router.message(StateFilter(SignalStates.waiting_for_text), F.text)
async def process_signal_text(message: Message, state: FSMContext):
    if message.text and message.text.strip() == "/cancel":
        await state.clear()
        await message.answer("❌ Signal sending cancelled")
        return
    await state.update_data(text=message.text)
    await show_signal_preview(message, state)


@router.message(StateFilter(SignalStates.waiting_for_text), F.photo)
async def process_additional_photo(message: Message, state: FSMContext):
    data = await state.get_data()
    photo_ids = data.get("photo_ids", [])
    if len(photo_ids) >= 2:
        await message.answer("⚠️ Maximum 2 photos. Send the signal text.")
        return
    photo_ids.append(message.photo[-1].file_id)
    await state.update_data(photo_ids=photo_ids)
    await message.answer(
        f"✅ Photo {len(photo_ids)}/2 received!\n\n"
        "Now send the signal text."
    )


async def show_signal_preview(message: Message, state: FSMContext):
    data = await state.get_data()
    photo_ids = data.get("photo_ids", [])
    text = data.get("text", "")
    if not photo_ids and not text:
        await message.answer("❌ Error: no data to send")
        await state.clear()
        return
    preview_text = "📋 Signal Preview:\n\n"
    if text:
        preview_text += f"Text:\n{text}\n\n"
    if photo_ids:
        preview_text += f"Photos: {len(photo_ids)}\n\n"
    preview_text += "Choose audience (Group 1 or Group 2):"
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="❌ Cancel", callback_data="signal_cancel"),
            InlineKeyboardButton(text="✏️ Edit", callback_data="signal_edit")
        ],
        [
            InlineKeyboardButton(text="✅ Group 1", callback_data="signal_send_1"),
            InlineKeyboardButton(text="✅ Group 2", callback_data="signal_send_2")
        ]
    ])
    if photo_ids:
        if len(photo_ids) == 1:
            await message.bot.send_photo(
                chat_id=message.chat.id,
                photo=photo_ids[0],
                caption=preview_text,
                reply_markup=keyboard,
                parse_mode="HTML"
            )
        else:
            media = [
                InputMediaPhoto(media=photo_ids[0]),
                InputMediaPhoto(media=photo_ids[1])
            ]
            await message.bot.send_media_group(chat_id=message.chat.id, media=media)
            await message.answer(preview_text, reply_markup=keyboard, parse_mode="HTML")
    else:
        await message.answer(preview_text, reply_markup=keyboard, parse_mode="HTML")
    await state.set_state(SignalStates.waiting_for_confirm)


@router.callback_query(F.data == "signal_cancel", StateFilter(SignalStates.waiting_for_confirm))
async def signal_cancel(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    try:
        await callback.message.edit_text("❌ Signal sending cancelled")
    except Exception:
        await callback.message.answer("❌ Signal sending cancelled")
    await callback.answer()


@router.callback_query(F.data == "signal_edit", StateFilter(SignalStates.waiting_for_confirm))
async def signal_edit(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.answer()
    except Exception:
        pass
    try:
        await callback.message.edit_text("✏️ Редактирование. Выберите тип сигнала:")
    except Exception:
        await callback.message.answer("✏️ Редактирование. Выберите тип сигнала:")
    kb = InlineKeyboardBuilder()
    kb.button(text="📉 SHORT", callback_data="signal_type_short")
    kb.button(text="📈 LONG", callback_data="signal_type_long")
    await callback.message.answer("SHORT or LONG?", reply_markup=kb.as_markup())
    await state.set_state(SignalStates.waiting_for_signal_type)


@router.callback_query(F.data.startswith("signal_send_"), StateFilter(SignalStates.waiting_for_confirm))
async def signal_send(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.message.edit_text("⏳ Sending signal...")
    except Exception:
        await callback.message.answer("⏳ Sending signal...")
    await callback.answer()
    suffix = callback.data.replace("signal_send_", "")
    try:
        target_group = int(suffix)
    except ValueError:
        target_group = 1
    if target_group not in (1, 2):
        target_group = 1
    data = await state.get_data()
    photo_ids = data.get("photo_ids", [])
    text = data.get("text", "")
    await process_final_signal(callback.message, state, photo_ids, text, target_group=target_group)


async def process_final_signal(message: Message, state: FSMContext, photo_ids=None, text=None, target_group=1):
    """Send signal. target_group: 1 or 2. Admins receive all signals."""
    if photo_ids is None or text is None:
        data = await state.get_data()
        photo_ids = photo_ids or data.get("photo_ids", [])
        text = text or data.get("text", "")
    if not photo_ids and not text:
        await message.answer("❌ Error: no data to send")
        await state.clear()
        return
    if target_group not in (1, 2):
        target_group = 1

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO signals (text, photo_ids, created_by, split_group)
        VALUES (?, ?, ?, ?)
        """,
        (text, json.dumps(photo_ids), message.from_user.id, target_group),
    )
    conn.commit()
    signal_id = cursor.lastrowid

    cursor.execute(
        "SELECT telegram_id FROM users WHERE is_premium = 1 AND is_active = 1 AND split_group = ?",
        (target_group,),
    )
    premium_users = [int(row[0]) for row in cursor.fetchall()]
    cursor.execute("SELECT telegram_id FROM admins")
    admin_ids = [int(row[0]) for row in cursor.fetchall()]
    recipients = set(premium_users) | set(admin_ids)

    sent_count = 0
    failed_count = 0
    body = build_signal_body(text)

    for user_telegram_id in recipients:
        try:
            msg_to_pin = None
            if photo_ids:
                if len(photo_ids) == 1:
                    msg_to_pin = await message.bot.send_photo(
                        chat_id=user_telegram_id,
                        photo=photo_ids[0],
                        caption=body,
                        parse_mode="HTML"
                    )
                else:
                    media = [
                        InputMediaPhoto(media=photo_ids[0], caption=body, parse_mode="HTML"),
                        InputMediaPhoto(media=photo_ids[1])
                    ]
                    sent_messages = await message.bot.send_media_group(
                        chat_id=user_telegram_id,
                        media=media
                    )
                    msg_to_pin = sent_messages[0] if sent_messages else None
            else:
                msg_to_pin = await message.bot.send_message(
                    chat_id=user_telegram_id,
                    text=body,
                    parse_mode="HTML"
                )
            if msg_to_pin:
                try:
                    await message.bot.pin_chat_message(
                        chat_id=user_telegram_id,
                        message_id=msg_to_pin.message_id,
                        disable_notification=True
                    )
                    await _delete_pin_system_notification(
                        chat_id=user_telegram_id,
                        pinned_message_id=msg_to_pin.message_id,
                        bot=message.bot,
                    )
                except Exception as pin_err:
                    logger.warning(f"Could not pin message for user {user_telegram_id}: {pin_err}")
            sent_count += 1
        except Exception as e:
            failed_count += 1
            logger.error(f"Error sending signal to user {user_telegram_id}: {e}")

    await message.answer(
        f"✅ *Signal sent!*\n\n"
        f"📊 Statistics:\n"
        f"   • Sent: {sent_count}\n"
        f"   • Errors: {failed_count}\n"
        f"   • Signal ID: {signal_id}"
    )
    await state.clear()


@router.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state:
        await state.clear()
        await message.answer("❌ Operation cancelled")
    else:
        await message.answer("❌ No active operations to cancel")
