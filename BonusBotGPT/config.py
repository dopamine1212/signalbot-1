"""Конфигурация бота из переменных окружения."""
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Обязательный канал для подписки (без @). Пусто = проверка отключена
REQUIRED_CHANNEL = (os.getenv("REQUIRED_CHANNEL", "") or "").strip().lstrip("@")

# Допустимые MIME-типы для изображений (документ)
ALLOWED_DOCUMENT_MIMES = {"image/png", "image/jpeg", "image/jpg"}
ALLOWED_DOCUMENT_EXTENSIONS = {".png", ".jpg", ".jpeg"}
