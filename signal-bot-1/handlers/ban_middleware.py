from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery, TelegramObject
from services import AdminService, BanService


class BanMiddleware(BaseMiddleware):
    """Глобально блокирует действия забаненных пользователей."""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        user = getattr(event, "from_user", None)
        if not user:
            return await handler(event, data)

        if AdminService.is_admin(user.id):
            return await handler(event, data)

        if not BanService.is_banned(user.id, user.username):
            return await handler(event, data)

        if isinstance(event, Message):
            await event.answer("⛔️ Доступ к боту ограничен администратором.")
        elif isinstance(event, CallbackQuery):
            await event.answer("⛔️ Доступ ограничен.", show_alert=True)
        return None
