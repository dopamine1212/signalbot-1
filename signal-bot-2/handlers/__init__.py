from aiogram import Router
from . import start, admin
from .ban_middleware import BanMiddleware

router = Router()
router.include_router(start.router)
router.include_router(admin.router)
router.message.middleware(BanMiddleware())
router.callback_query.middleware(BanMiddleware())
