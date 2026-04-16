"""
Объединение всех обработчиков
"""
from aiogram import Router
from . import start, payment, admin
from .ban_middleware import BanMiddleware

# Создаем главный роутер
router = Router()

# Подключаем все роутеры
router.include_router(start.router)
router.include_router(payment.router)  # Только callback для платежей
router.include_router(admin.router)
router.message.middleware(BanMiddleware())
router.callback_query.middleware(BanMiddleware())

