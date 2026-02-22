"""
Админские команды (первый бот: только рассылка сообщений, без отправки сигналов).
"""
import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from database import get_db, PaymentStatus
from services import AdminService, UserService

logger = logging.getLogger(__name__)


router = Router()


class BroadcastStates(StatesGroup):
    """Состояния для рассылки сообщения"""
    waiting_for_text = State()
    waiting_for_link = State()  # опционально: ссылка кнопкой под сообщением


@router.message(Command("stats"))
async def cmd_stats(message: Message):
    """Bot statistics (admin only)"""
    if not AdminService.is_admin(message.from_user.id):
        await message.answer("❌ You don't have administrator rights")
        return
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Статистика
    cursor.execute("SELECT COUNT(*) as count FROM users")
    total_users = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(*) as count FROM users WHERE is_active = 1")
    active_users = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(*) as count FROM payments")
    total_payments = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(*) as count FROM payments WHERE status = ?", (PaymentStatus.COMPLETED,))
    completed_payments = cursor.fetchone()['count']
    
    cursor.execute("SELECT SUM(amount) as total FROM payments WHERE status = ?", (PaymentStatus.COMPLETED,))
    total_amount = cursor.fetchone()['total'] or 0
    
    cursor.execute("SELECT COUNT(*) as count FROM users WHERE split_group = 1")
    group1_count = cursor.fetchone()['count']
    cursor.execute("SELECT COUNT(*) as count FROM users WHERE split_group = 2")
    group2_count = cursor.fetchone()['count']
    
    stats_text = f"""
📊 Bot Statistics:

👥 Users:
   • Total: {total_users}
   • Active: {active_users}
   • Split 50/50: Group 1 = {group1_count}, Group 2 = {group2_count}

💳 Payments:
   • Total: {total_payments}
   • Successful: {completed_payments}
   • Total amount: {total_amount:.2f} USD
"""
    
    # У бота parse_mode=MARKDOWN по умолчанию; тут форматирование не нужно.
    await message.answer(stats_text, parse_mode=None)


@router.message(Command("admin_list"))
async def cmd_admin_list(message: Message):
    """Admin list (admin only)"""
    if not AdminService.is_admin(message.from_user.id):
        await message.answer("❌ You don't have administrator rights")
        return
    
    admins = AdminService.get_all_admins()
    
    if not admins:
        await message.answer("📋 Admin list is empty")
        return
    
    admin_text = "👑 Admin List:\n\n"
    for admin in admins:
        admin_text += f"🆔 ID: {admin['telegram_id']}\n"
        if admin['username']:
            admin_text += f"   @{admin['username']}\n"
        if admin['first_name']:
            admin_text += f"   {admin['first_name']}\n"
        admin_text += f"   Added: {admin['added_at']}\n\n"
    
    # У username часто есть '_' — в Markdown это ломает парсинг entities у Telegram.
    await message.answer(admin_text, parse_mode=None)


@router.message(Command("admin_add"))
async def cmd_admin_add(message: Message):
    """Add admin (admin only)"""
    if not AdminService.is_admin(message.from_user.id):
        await message.answer("❌ You don't have administrator rights")
        return
    
    # Получаем ID из команды или из ответа на сообщение
    try:
        if message.reply_to_message:
            new_admin_id = message.reply_to_message.from_user.id
        else:
            args = message.text.split()
            if len(args) < 2:
                await message.answer("❌ Usage: /admin_add &lt;user_id&gt; or reply to user's message")
                return
            new_admin_id = int(args[1])
        
        # Получаем информацию о пользователе
        user = UserService.get_user_by_telegram_id(new_admin_id)
        username = user.get('username') if user else None
        first_name = user.get('first_name') if user else None
        
        if AdminService.add_admin(new_admin_id, username, first_name, message.from_user.id):
            await message.answer(f"✅ User {new_admin_id} added to admins")
        else:
            await message.answer(f"❌ User {new_admin_id} is already an admin")
    except ValueError:
        await message.answer("❌ Invalid ID format. Use numeric ID")
    except Exception as e:
        await message.answer(f"❌ Error: {e}")


@router.message(Command("admin_remove"))
async def cmd_admin_remove(message: Message):
    """Remove admin (admin only)"""
    if not AdminService.is_admin(message.from_user.id):
        await message.answer("❌ You don't have administrator rights")
        return
    
    try:
        args = message.text.split()
        if len(args) < 2:
            await message.answer("❌ Usage: /admin_remove &lt;user_id&gt;")
            return
        
        admin_id = int(args[1])
        
        # Нельзя удалить самого себя
        if admin_id == message.from_user.id:
            await message.answer("❌ You cannot remove yourself")
            return
        
        if AdminService.remove_admin(admin_id):
            await message.answer(f"✅ User {admin_id} removed from admins")
        else:
            await message.answer(f"❌ User {admin_id} not found in admin list")
    except ValueError:
        await message.answer("❌ Invalid ID format. Use numeric ID")
    except Exception as e:
        await message.answer(f"❌ Error: {e}")


@router.message(Command("admin"))
@router.message(Command("admine"))
async def cmd_admin(message: Message):
    """Список команд админа. Для не-админов ничего не показываем."""
    if not AdminService.is_admin(message.from_user.id):
        return
    admin_commands = """
👑 *Administrator Commands:*

📊 *Statistics:*
`/stats` - Bot statistics (users, payments)

👥 *Admin Management:*
`/admin_list` - List all admins
`/admin_add <user_id>` - Add admin
`/admin_remove <user_id>` - Remove admin

📢 *Messages:*
`/send_message` - Send a simple message to all users

📋 *Results:*
`/summarize` - Подвести итоги (список юзеров, у которых прогноз зашёл)

Send /cancel to cancel any operation.
"""
    await message.answer(admin_commands)


@router.message(Command("summarize"))
async def cmd_summarize(message: Message):
    """Подвести итоги: выбор группы, у которой прогноз зашёл."""
    if not AdminService.is_admin(message.from_user.id):
        await message.answer("❌ You don't have administrator rights")
        return
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Group 1", callback_data="summarize_group_1"),
            InlineKeyboardButton(text="✅ Group 2", callback_data="summarize_group_2"),
        ],
    ])
    await message.answer(
        "📋 *Подвести итоги*\n\n"
        "Выберите группу, у которой прогноз сработал:",
        reply_markup=keyboard,
        parse_mode=None,
    )


@router.callback_query(F.data.startswith("summarize_group_"))
async def cb_summarize_group(callback: CallbackQuery):
    """Показать список юзеров выбранной группы (прогноз зашёл)."""
    if not AdminService.is_admin(callback.from_user.id):
        await callback.answer("❌ No access", show_alert=True)
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
    else:
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


@router.message(Command("send_message"))
async def cmd_send_message(message: Message, state: FSMContext):
    """Рассылка простого сообщения всем пользователям бота (только админ)."""
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
    """Приняли текст рассылки — спрашиваем про ссылку или сразу рассылаем."""
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
    """Добавить ссылку к рассылке или пропустить и отправить."""
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
        # если не URL и не /skip — считаем что хотели ссылку, но ошиблись; всё равно шлём без кнопки
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


@router.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext):
    """Cancel current operation"""
    current_state = await state.get_state()
    if current_state:
        await state.clear()
        await message.answer("❌ Operation cancelled")
    else:
        await message.answer("❌ No active operations to cancel")

