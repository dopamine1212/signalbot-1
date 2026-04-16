"""
Сервисы для работы с пользователями и платежами
"""
from typing import Optional, Dict, Tuple
import requests
from database import get_db, PaymentStatus
from config import settings
import logging

logger = logging.getLogger(__name__)


class AdminService:
    """Сервис для управления админами"""
    
    @staticmethod
    def is_admin(telegram_id: int) -> bool:
        """Проверить, является ли пользователь админом"""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM admins WHERE telegram_id = ?", (telegram_id,))
        return cursor.fetchone() is not None
    
    @staticmethod
    def add_admin(telegram_id: int, username: str = None, first_name: str = None, added_by: int = None) -> bool:
        """Добавить админа"""
        conn = get_db()
        cursor = conn.cursor()
        
        # Проверяем, не является ли уже админом
        cursor.execute("SELECT * FROM admins WHERE telegram_id = ?", (telegram_id,))
        if cursor.fetchone():
            return False  # Уже админ
        
        cursor.execute("""
            INSERT INTO admins (telegram_id, username, first_name, added_by)
            VALUES (?, ?, ?, ?)
        """, (telegram_id, username, first_name, added_by))
        conn.commit()
        return True
    
    @staticmethod
    def remove_admin(telegram_id: int) -> bool:
        """Удалить админа"""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM admins WHERE telegram_id = ?", (telegram_id,))
        conn.commit()
        return cursor.rowcount > 0
    
    @staticmethod
    def get_all_admins() -> list:
        """Получить список всех админов"""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM admins ORDER BY added_at DESC")
        admins = cursor.fetchall()
        return [dict(admin) for admin in admins]


class BanService:
    """Сервис для управления банами пользователей."""

    @staticmethod
    def _normalize_username(username: str) -> str:
        return (username or "").strip().lstrip("@").lower()

    @staticmethod
    def is_banned(telegram_id: int | None, username: str | None) -> bool:
        conn = get_db()
        cursor = conn.cursor()
        normalized = BanService._normalize_username(username)
        if telegram_id:
            cursor.execute(
                "SELECT 1 FROM banned_users WHERE telegram_id = ? OR username = ?",
                (telegram_id, normalized),
            )
        else:
            cursor.execute("SELECT 1 FROM banned_users WHERE username = ?", (normalized,))
        return cursor.fetchone() is not None

    @staticmethod
    def ban_by_username(username: str, added_by: int | None = None) -> tuple[bool, str]:
        normalized = BanService._normalize_username(username)
        if not normalized:
            return False, "empty_username"

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT telegram_id FROM users WHERE lower(username) = ? ORDER BY id DESC LIMIT 1",
            (normalized,),
        )
        user_row = cursor.fetchone()
        telegram_id = user_row[0] if user_row else None

        cursor.execute(
            "SELECT 1 FROM banned_users WHERE username = ? OR (telegram_id IS NOT NULL AND telegram_id = ?)",
            (normalized, telegram_id),
        )
        if cursor.fetchone():
            return False, "already_banned"

        cursor.execute(
            """
            INSERT INTO banned_users (telegram_id, username, added_by)
            VALUES (?, ?, ?)
            """,
            (telegram_id, normalized, added_by),
        )
        conn.commit()
        return True, "ok"

    @staticmethod
    def unban_by_username(username: str) -> bool:
        normalized = BanService._normalize_username(username)
        if not normalized:
            return False
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM banned_users WHERE username = ?", (normalized,))
        conn.commit()
        return cursor.rowcount > 0

    @staticmethod
    def get_all_bans() -> list:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT username, telegram_id, added_at FROM banned_users ORDER BY added_at DESC")
        return [dict(row) for row in cursor.fetchall()]


class UserService:
    """Сервис для управления пользователями"""
    
    @staticmethod
    def get_or_create_user(telegram_id: int, username: str = None, 
                          first_name: str = None, last_name: str = None) -> Dict:
        """Получить или создать пользователя"""
        conn = get_db()
        cursor = conn.cursor()
        
        # Проверяем существование пользователя
        cursor.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))
        user = cursor.fetchone()
        
        if not user:
            # Разделение 50/50: каждый следующий пользователь получает флаг 1 или 2
            cursor.execute("SELECT COUNT(*) as cnt FROM users")
            count = cursor.fetchone()['cnt']
            split_group = (count % 2) + 1  # 1, 2, 1, 2, ...
            cursor.execute("""
                INSERT INTO users (telegram_id, username, first_name, last_name, split_group)
                VALUES (?, ?, ?, ?, ?)
            """, (telegram_id, username, first_name, last_name, split_group))
            conn.commit()
            
            # Получаем созданного пользователя
            cursor.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))
            user = cursor.fetchone()
        else:
            # Обновляем данные пользователя
            updates = []
            params = []
            if username:
                updates.append("username = ?")
                params.append(username)
            if first_name:
                updates.append("first_name = ?")
                params.append(first_name)
            if last_name:
                updates.append("last_name = ?")
                params.append(last_name)
            
            if updates:
                params.append(telegram_id)
                cursor.execute(f"""
                    UPDATE users SET {', '.join(updates)}, updated_at = CURRENT_TIMESTAMP
                    WHERE telegram_id = ?
                """, params)
                conn.commit()
                
                cursor.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))
                user = cursor.fetchone()
        
        return dict(user) if user else None
    
    @staticmethod
    def get_user_by_telegram_id(telegram_id: int) -> Optional[Dict]:
        """Получить пользователя по Telegram ID"""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))
        user = cursor.fetchone()
        return dict(user) if user else None
    
    @staticmethod
    def update_balance(user_id: int, amount: float) -> bool:
        """Обновить баланс пользователя"""
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute("SELECT balance FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        if not user:
            return False
        
        new_balance = user['balance'] + amount
        cursor.execute("""
            UPDATE users SET balance = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (new_balance, user_id))
        conn.commit()
        return True

    @staticmethod
    def activate_subscription(telegram_id: int) -> bool:
        """Включить подписку (is_premium=1, is_active=1) — второй бот увидит после commit."""
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE users SET is_premium = 1, is_active = 1, updated_at = CURRENT_TIMESTAMP
            WHERE telegram_id = ?
        """, (telegram_id,))
        conn.commit()
        return cursor.rowcount > 0

    @staticmethod
    def subscription_months_for_amount(amount: float) -> int:
        """Тариф по сумме платежа: 24->1 мес, 100->6 мес, 200/190->12 мес."""
        rounded = round(float(amount), 2)
        if abs(rounded - 24.0) < 0.01:
            return 1
        if abs(rounded - 100.0) < 0.01:
            return 6
        # Поддерживаем оба варианта годового тарифа (исторически встречались 190 и 200)
        if abs(rounded - 200.0) < 0.01 or abs(rounded - 190.0) < 0.01:
            return 12
        return 0

    @staticmethod
    def activate_subscription_by_amount(telegram_id: int, amount: float) -> Tuple[bool, int, Optional[str]]:
        """
        Активировать/продлить подписку на срок по сумме платежа.
        Возвращает: (ok, months, premium_until_iso)
        """
        months = UserService.subscription_months_for_amount(amount)
        if months <= 0:
            return False, 0, None

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE users
            SET
                is_premium = 1,
                is_active = 1,
                subscription_months = ?,
                subscription_activated_at = CURRENT_TIMESTAMP,
                premium_until = CASE
                    WHEN premium_until IS NOT NULL AND premium_until > CURRENT_TIMESTAMP
                        THEN premium_until + (? || ' months')::interval
                    ELSE CURRENT_TIMESTAMP + (? || ' months')::interval
                END,
                updated_at = CURRENT_TIMESTAMP
            WHERE telegram_id = ?
            RETURNING premium_until
            """,
            (months, str(months), str(months), telegram_id),
        )
        row = cursor.fetchone()
        conn.commit()
        if not row:
            return False, months, None
        premium_until = row.get("premium_until") if hasattr(row, "get") else None
        return True, months, str(premium_until) if premium_until is not None else None


class CryptoPaymentService:
    """Сервис для обработки криптоплатежей через Crypto Bot (Telegram)"""
    
    def __init__(self):
        self.bot_token = settings.CRYPTO_BOT_TOKEN
        if getattr(settings, "CRYPTO_PAY_TESTNET", False):
            self.api_url = "https://testnet-pay.crypt.bot/api"  # Testnet: @CryptoTestnetBot
        else:
            self.api_url = "https://pay.crypt.bot/api"  # Mainnet: @CryptoBot
    
    def _make_request(self, method: str, params: Dict = None, use_post: bool = False) -> Optional[Dict]:
        """Выполнить запрос к Crypto Bot API"""
        url = f"{self.api_url}/{method}"
        headers = {
            "Crypto-Pay-API-Token": self.bot_token
        }
        
        try:
            # Для createInvoice используем POST, для остальных GET
            if use_post or method == "createInvoice":
                headers["Content-Type"] = "application/json"
                response = requests.post(url, headers=headers, json=params or {})
            else:
                response = requests.get(url, headers=headers, params=params or {})
            
            # Логируем для отладки
            logger.debug(f"Crypto Bot API Request: {url}")
            logger.debug(f"Method: {'POST' if (use_post or method == 'createInvoice') else 'GET'}")
            logger.debug(f"Params: {params}")
            logger.debug(f"Response status: {response.status_code}")
            logger.debug(f"Response text: {response.text}")
            
            response.raise_for_status()
            data = response.json()
            
            if data.get("ok"):
                return data.get("result")
            else:
                error_data = data.get("error", {})
                error_msg = error_data.get("name", error_data.get("code", "Unknown error"))
                error_description = error_data.get("message", "")
                logger.error(f"Ошибка Crypto Bot API: {error_msg} - {error_description}")
                return None
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP ошибка Crypto Bot: {e}")
            if hasattr(e.response, 'text'):
                logger.error(f"Ответ сервера: {e.response.text}")
            return None
        except Exception as e:
            logger.error(f"Ошибка запроса к Crypto Bot: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def create_invoice(
        self,
        amount: float,
        currency: str = "USD",
        description: str = "Пополнение баланса",
        user_id: int = None
    ) -> Optional[Dict]:
        """
        Создание инвойса через Crypto Bot
        
        Args:
            amount: Сумма в USD
            currency: Валюта (USD, EUR, RUB и т.д.)
            description: Описание платежа
            user_id: ID пользователя Telegram
            
        Returns:
            Данные инвойса или None
        """
        # Crypto Bot API - создание инвойса
        # Проверяем, что токен установлен
        if not self.bot_token:
            logger.error("Ошибка: CRYPTO_BOT_TOKEN не установлен в .env")
            return None
        
        # Crypto Bot API - создание инвойса
        # Используем фиатную валюту для указания суммы в USD
        params = {
            "currency_type": "fiat",  # Тип валюты - фиат
            "fiat": currency,  # Фиатная валюта (USD, EUR и т.д.)
            "amount": str(amount),  # Сумма в фиатной валюте
            "description": description,
            "expires_in": 300,  # Инвойс истекает через 5 минут (300 секунд)
            "accepted_assets": "USDT,TON,BTC,ETH",  # Какие криптовалюты можно использовать для оплаты
        }
        
        # Опциональные параметры
        if user_id:
            params["payload"] = str(user_id)  # Передаем user_id в payload для идентификации
        
        # hidden_message - сообщение после оплаты (максимум 1024 символа)
        hidden_msg = f"Пополнение баланса на {amount} {currency}"
        if len(hidden_msg) > 1024:
            hidden_msg = hidden_msg[:1021] + "..."
        params["hidden_message"] = hidden_msg
        
        # Используем POST для createInvoice
        result = self._make_request("createInvoice", params, use_post=True)
        
        # Дополнительная проверка результата
        if result:
            logger.info(f"Инвойс создан успешно: invoice_id={result.get('invoice_id')}")
        else:
            logger.error("Не удалось создать инвойс через Crypto Bot API")
        
        return result
    
    def get_invoice(self, invoice_id: int) -> Optional[Dict]:
        """
        Получить информацию об инвойсе.
        Crypto Pay API: getInvoices — параметр invoice_ids (строка, ID через запятую).
        """
        params = {"invoice_ids": str(invoice_id)}
        result = self._make_request("getInvoices", params)
        
        if not result:
            logger.warning(f"getInvoices returned empty for invoice_id={invoice_id}")
            return None
        if isinstance(result, list) and len(result) > 0:
            return result[0]
        if isinstance(result, dict):
            # Один инвойс как dict (поля status, amount и т.д. в корне)
            if "status" in result:
                return result
            if result.get("invoice_id") is not None or result.get("id") is not None:
                return result
            # Вариант: {"items": [invoice, ...], "count": N}
            items = result.get("items") or result.get("invoices")
            if items and len(items) > 0:
                return items[0]
        logger.warning(f"getInvoices unexpected result: type={type(result)}, keys={list(result.keys()) if isinstance(result, dict) else 'n/a'}")
        return None
    
    def check_payment_status(self, invoice_id: int) -> Optional[Dict]:
        """
        Проверка статуса платежа
        
        Args:
            invoice_id: ID инвойса
            
        Returns:
            Данные инвойса со статусом или None
        """
        return self.get_invoice(invoice_id)
