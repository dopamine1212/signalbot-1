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
    LANDING_URL: str = os.getenv("LANDING_URL", "http://89.169.2.206/").strip()
    # 📘 reviews (ссылка на канал/чат)
    REVIEWS_CHANNEL: str = os.getenv("REVIEWS_CHANNEL", "https://t.me/+zZdcOfpyTkc3OGMx")
    SIGNALS_CHANNEL: str = os.getenv("SIGNALS_CHANNEL", "")
    # 📦 BONUS
    PRODUCT_CHANNEL: str = os.getenv("PRODUCT_CHANNEL", "")
    # 👨 support (username без @)
    OPERATOR_USERNAME: str = os.getenv("OPERATOR_USERNAME", "ecoTomSawyer")
    # Ссылка на второго бота (сигналы) — для кнопки Trading cabinet (@signalpriv_bot)
    SIGNAL_BOT_LINK: str = os.getenv("SIGNAL_BOT_LINK", "https://t.me/signalpriv_bot").strip()
    # Обязательный канал для подписки (без @) — https://t.me/SaawyerCrypto
    REQUIRED_CHANNEL: str = os.getenv("REQUIRED_CHANNEL", "SaawyerCrypto").strip().lstrip("@")

    # Other
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")


settings = Settings()

