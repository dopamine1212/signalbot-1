"""
Настройки приложения
"""
import os
from dotenv import load_dotenv

# .env из папки бота (signal-bot-1), чтобы работало при запуске из любой директории
_bot_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(_bot_dir, ".env"))
load_dotenv()


class Settings:
    """Класс для хранения настроек приложения"""
    
    # Telegram Bot
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
    ADMIN_IDS: list[int] = [int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x]
    
    # Database (Supabase PostgreSQL) — общая БД для signal-bot-1 и signal-bot-2
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    
    # Crypto Pay API (Crypto Bot): https://help.send.tg/en/articles/10279948-crypto-pay-api
    CRYPTO_BOT_TOKEN: str = os.getenv("CRYPTO_BOT_TOKEN", "")
    # Testnet: @CryptoTestnetBot, URL https://testnet-pay.crypt.bot/api
    CRYPTO_PAY_TESTNET: bool = os.getenv("CRYPTO_PAY_TESTNET", "false").lower() == "true"
    
    # Channels and Links
    LANDING_URL: str = os.getenv("LANDING_URL", "http://sawyercrypto.com/").strip()
    # 📘 reviews (ссылка на канал/чат)
    REVIEWS_CHANNEL: str = os.getenv("REVIEWS_CHANNEL", "https://t.me/+zZdcOfpyTkc3OGMx")
    SIGNALS_CHANNEL: str = os.getenv("SIGNALS_CHANNEL", "")
    # 📦 BONUS
    PRODUCT_CHANNEL: str = os.getenv("PRODUCT_CHANNEL", "")
    # 👨 support (username без @)
    OPERATOR_USERNAME: str = os.getenv("OPERATOR_USERNAME", "ecoTomSawyer")
    # Ссылка на второго бота (сигналы VIP) — для кнопки Trading cabinet (@TomSawyerVIP_bot)
    SIGNAL_BOT_LINK: str = os.getenv("SIGNAL_BOT_LINK", "https://t.me/TomSawyerVIP_bot").strip()
    # Обязательный канал для подписки (без @) — https://t.me/SaawyerCrypto
    REQUIRED_CHANNEL: str = os.getenv("REQUIRED_CHANNEL", "SaawyerCrypto").strip().lstrip("@")

    # Текст уведомления по команде /send_notification (админ). Редактируйте под себя.
    NOTIFICATION_TEMPLATE: str = os.getenv(
        "NOTIFICATION_TEMPLATE",
        """<tg-emoji emoji-id=\"5316615057939897832\">🤖</tg-emoji> Today's signal is at ... GMT

<tg-emoji emoji-id=\"5265057377165531669\">🚀</tg-emoji> reminders

• 50% of profit will be sent to us after you receive profit

<a href="http://t.me/ecoTomSawyer"><b>Need some help?</b></a>""",
    ).strip()

    # Other
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")


settings = Settings()

