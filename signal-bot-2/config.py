"""
Settings for bot 2 (signals and broadcast only). Uses same Supabase as main bot.
"""
import os
from dotenv import load_dotenv

# Загружаем .env из папки, где лежит config.py (signal-bot-2), чтобы работало при запуске из любой директории
_bot_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(_bot_dir, ".env"))
load_dotenv()


class Settings:
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
    ADMIN_IDS: list[int] = [int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x]
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    # Main menu link — Бот 1 @TomSawyerScanner_bot (button "Go to main menu")
    MAIN_BOT_LINK: str = os.getenv("MAIN_BOT_LINK", "https://t.me/TomSawyerScanner_bot").strip() or "https://t.me/TomSawyerScanner_bot"
    # Текст уведомления по команде /send_notification (админ). Редактируйте под себя.
    NOTIFICATION_TEMPLATE: str = os.getenv(
        "NOTIFICATION_TEMPLATE",
        """<tg-emoji emoji-id=\"5316615057939897832\">🤖</tg-emoji> Today's signal is at ... GMT

<tg-emoji emoji-id=\"5265057377165531669\">🚀</tg-emoji> reminders

• 50% of profit will be sent to us after you receive profit

<a href="http://t.me/ecoTomSawyer"><b>Need some help?</b></a>""",
    ).strip()
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")


settings = Settings()
