"""
Админские команды (бот №1): только отправка уведомлений (рассылка), без сигналов и итогов по группам.
"""
import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, LinkPreviewOptions
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from database import get_db, PaymentStatus
from services import AdminService, UserService
from config import settings

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
👑 <b>Administrator Commands:</b>

📊 <b>Statistics:</b>
<code>/stats</code> - Bot statistics (users, payments)

👥 <b>Admin Management:</b>
<code>/admin_list</code> - List all admins
<code>/admin_add &lt;user_id&gt;</code> - Add admin
<code>/admin_remove &lt;user_id&gt;</code> - Remove admin

📢 <b>Notifications:</b>
<code>/send_message</code> - Send custom message to all users
<code>/send_notification</code> - Send prepared template to all users
<code>/send_notification_now</code> - Send prepared template to all users now

Send /cancel to cancel any operation.
"""
    await message.answer(admin_commands, parse_mode="HTML")


@router.message(Command("send_notification"))
async def cmd_send_notification(message: Message):
    """Отправка заготовленного уведомления всем пользователям (текст из config.NOTIFICATION_TEMPLATE)."""
    if not AdminService.is_admin(message.from_user.id):
        return
    text = (settings.NOTIFICATION_TEMPLATE or "").strip()
    if not text:
        await message.answer("❌ NOTIFICATION_TEMPLATE пустой. Заполните в config.py или .env")
        return
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
                parse_mode="HTML",
                link_preview_options=LinkPreviewOptions(is_disabled=True),
            )
            sent += 1
        except Exception as e:
            failed += 1
            logger.debug("Notification to %s: %s", uid, e)
    await message.answer(f"✅ Notification sent: {sent} delivered, {failed} errors.")


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

