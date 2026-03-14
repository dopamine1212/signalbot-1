"""
Обработчики платежей
"""
import html
import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from database import get_db, PaymentStatus
from services import UserService, CryptoPaymentService
from handlers.start import _PROTECTED_PAYMENT_MESSAGE, _LAST_BOT_MESSAGE

logger = logging.getLogger(__name__)

router = Router()
crypto_service = CryptoPaymentService()


# Команда /payment удалена - используется только через кнопки


@router.callback_query(F.data.startswith("pay_"))
async def process_payment(callback: CallbackQuery):
    """Payment amount selection handler"""
    # Сразу удаляем сообщение с выбором тарифа ($24 / $100 / $200)
    chat_id = callback.message.chat.id
    try:
        await callback.message.delete()
    except Exception:
        pass

    user = UserService.get_user_by_telegram_id(callback.from_user.id)
    if not user:
        await callback.answer("Error: user not found")
        return
    
    data = callback.data
    if data == "pay_custom":
        await callback.message.answer("Enter the amount to top up (in USD):")
        await callback.answer()
        return
    
    amount = float(data.split("_")[1])
    
    # Создаем инвойс через Crypto Bot
    invoice_data = crypto_service.create_invoice(
        amount=amount,
        currency="USD",
        description=f"Balance top-up for {amount} USD",
        user_id=callback.from_user.id
    )
    
    if not invoice_data:
        await callback.message.answer("❌ Error creating payment. Please try again later.")
        await callback.answer()
        return
    
    # Проверяем наличие обязательных полей
    invoice_id = invoice_data.get("invoice_id")
    bot_invoice_url = invoice_data.get("bot_invoice_url")  # Ссылка для оплаты из API
    
    if not invoice_id or not bot_invoice_url:
        logger.error(f"Error: incomplete invoice data. invoice_data: {invoice_data}")
        await callback.message.answer("❌ Error: failed to create invoice. Check Crypto Bot settings.")
        await callback.answer()
        return
    
    # НЕ записываем в БД сразу - только после успешной оплаты
    # Сначала показываем пользователю ссылку для оплаты
    
    # Отправляем сообщение с инструкцией и ссылкой (HTML)
    text = (
        f"💳 Payment for {amount} USD created!\n\n"
        f"<tg-emoji emoji-id=\"5258113901106580375\">⏰</tg-emoji> <b>Payment time: 5 minutes</b>\n\n"
        "Click the button below to pay:\n\n"
        f"<b>Invoice ID:</b> <code>{html.escape(str(invoice_id))}</code>"
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(icon_custom_emoji_id="5337082660164475701", text="Pay via Crypto bot", style="primary", url=bot_invoice_url),],
        [InlineKeyboardButton(icon_custom_emoji_id="5465368548702446780", text="Check status", style="primary", callback_data=f"check_invoice_{invoice_id}")]
    ])
    sent = await callback.message.answer(text, reply_markup=keyboard, parse_mode="HTML")
    # Сообщение с инвойсом не удаляем при переключении на Main menu / choose a subscription / BONUS
    _PROTECTED_PAYMENT_MESSAGE[chat_id] = sent.message_id
    _LAST_BOT_MESSAGE[chat_id] = sent.message_id

    await callback.answer()


@router.callback_query(F.data.startswith("check_invoice_"))
async def check_payment_status(callback: CallbackQuery):
    """Check payment status by invoice_id"""
    invoice_id = int(callback.data.split("_")[2])
    
    # Проверяем статус через Crypto Bot API
    invoice_data = crypto_service.check_payment_status(invoice_id)
    
    if not invoice_data:
        logger.warning(f"check_payment_status: no data for invoice_id={invoice_id}")
        await callback.message.answer("❌ Failed to check payment status.")
        await callback.answer()
        return
    
    status = invoice_data.get("status")
    logger.info(f"Invoice {invoice_id} status={status}, payload={invoice_data.get('payload')}")
    
    if status == "paid":
        # Платеж выполнен - записываем в БД
        conn = get_db()
        cursor = conn.cursor()
        
        # Проверяем, не записан ли уже этот платеж
        cursor.execute("SELECT * FROM payments WHERE payment_id = ?", (str(invoice_id),))
        existing_payment = cursor.fetchone()
        
        if existing_payment:
            # Платеж уже в БД. Раньше в user_id мог попасть telegram_id — тогда баланс не обновился.
            stored_user_id = existing_payment["user_id"]
            amount_stored = float(existing_payment["amount"])
            user = UserService.get_user_by_telegram_id(callback.from_user.id)
            # Самовосстановление: если по старому платежу не был выставлен срок подписки, применим сейчас.
            UserService.activate_subscription_by_amount(callback.from_user.id, amount_stored)
            if user and amount_stored > 0 and (stored_user_id != user["id"] or stored_user_id > 999999):
                UserService.update_balance(user["id"], amount_stored)
                await callback.message.answer("✅ Payment was already recorded. Balance has been updated.")
            else:
                await callback.message.answer("✅ Payment has already been processed.")
        else:
            # payload в инвойсе — это telegram_id (мы передали при createInvoice)
            payload = invoice_data.get("payload")
            telegram_id = None
            if payload:
                try:
                    telegram_id = int(payload)
                except (ValueError, TypeError):
                    pass
            if not telegram_id:
                telegram_id = callback.from_user.id

            user = UserService.get_user_by_telegram_id(telegram_id)
            if user:
                # В БД используем внутренний users.id, не telegram_id
                internal_user_id = user["id"]

                # Сумма по документации: paid_amount (оплачено) или amount (сумма инвойса), оба — строки
                paid_fiat = invoice_data.get("paid_fiat") or invoice_data.get("fiat") or "USD"
                raw_amount = invoice_data.get("paid_amount") or invoice_data.get("paid_fiat_amount") or invoice_data.get("amount")
                try:
                    paid_fiat_amount = float(raw_amount) if raw_amount is not None else 0.0
                except (TypeError, ValueError):
                    paid_fiat_amount = float(invoice_data.get("amount", 0) or 0)

                sub_ok, sub_months, premium_until = UserService.activate_subscription_by_amount(telegram_id, paid_fiat_amount)

                # Фиксируем платеж в БД в любом случае (даже если update_balance позже не сработает)
                cursor.execute("""
                    INSERT INTO payments (
                        user_id, amount, currency, crypto_currency, status, payment_id, payment_url,
                        subscription_months, subscription_until
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    internal_user_id,
                    paid_fiat_amount,
                    paid_fiat,
                    invoice_data.get("paid_asset", "USDT"),
                    PaymentStatus.COMPLETED,
                    str(invoice_id),
                    invoice_data.get("bot_invoice_url", ""),
                    sub_months if sub_ok else None,
                    premium_until if sub_ok else None,
                ))
                conn.commit()

                ok = UserService.update_balance(internal_user_id, paid_fiat_amount)
                if not ok:
                    logger.error("update_balance failed for user_id=%s", internal_user_id)
                    await callback.message.answer("✅ Payment recorded, but balance update failed. Please contact support.")
                elif sub_ok:
                    logger.info(
                        "Payment processed: user_id=%s, +%s %s, subscription=%s months until=%s",
                        internal_user_id, paid_fiat_amount, paid_fiat, sub_months, premium_until
                    )
                    await callback.message.answer(
                        f"✅ Payment completed successfully! Balance topped up by {paid_fiat_amount} {paid_fiat}.\n"
                        f"⭐ Premium activated for {sub_months} month(s)."
                    )
                else:
                    logger.info(
                        "Payment processed without subscription mapping: user_id=%s, amount=%s %s",
                        internal_user_id, paid_fiat_amount, paid_fiat
                    )
                    await callback.message.answer(
                        f"✅ Payment completed successfully! Balance topped up by {paid_fiat_amount} {paid_fiat}."
                    )
            else:
                await callback.message.answer("✅ Payment completed, but user not found in bot. Write /start and try again.")
    
    elif status == "active":
        await callback.message.answer("⏳ Payment is pending...\n\n⏰ You have 5 minutes to pay.")
    
    elif status == "expired":
        await callback.message.answer("❌ Payment expired. Create a new payment.")
    
    else:
        await callback.message.answer(f"⏳ Payment status: {status}")
    
    await callback.answer()

