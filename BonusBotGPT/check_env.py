"""
Проверка окружения: запусти на Mac и на сервере и сравни вывод.
На сервере: cd /root/signalbot-1/BonusBotGPT && ./venv/bin/python check_env.py
Локально:   cd BonusBotGPT && python check_env.py  (или ./venv/bin/python check_env.py)
"""
import os
import sys
from pathlib import Path

def main():
    base = Path(__file__).resolve().parent
    print("=== Проверка окружения BonusBotGPT ===\n")
    print("1. Python:", sys.executable)
    print("2. Папка бота:", base)
    print("3. Текущая папка (cwd):", os.getcwd())

    env_file = base / ".env"
    print("4. Файл .env:", env_file, "— существует:", env_file.exists())

    # Загружаем .env так же, как config.py
    from dotenv import load_dotenv
    load_dotenv(env_file)
    token = os.getenv("TELEGRAM_BOT_TOKEN", "")
    openai_key = os.getenv("OPENAI_API_KEY", "")
    print("5. TELEGRAM_BOT_TOKEN задан:", bool(token and token.strip()))
    print("6. OPENAI_API_KEY задан:", bool(openai_key and openai_key.strip()))

    print("7. Импорт aiogram:", end=" ")
    try:
        from aiogram import Bot, Dispatcher
        print("OK")
    except Exception as e:
        print("ОШИБКА:", e)

    print("8. Импорт openai:", end=" ")
    try:
        from openai import AsyncOpenAI
        print("OK")
    except Exception as e:
        print("ОШИБКА:", e)

    print("\nЕсли всё OK выше — бот должен запускаться. Если нет — смотри, какой пункт FAIL.")

if __name__ == "__main__":
    main()
