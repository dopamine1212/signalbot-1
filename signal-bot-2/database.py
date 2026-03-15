"""
База данных для бота 2: общая Supabase (PostgreSQL) с ботом 1.
Чтение подписки — новое подключение каждый раз (актуальные данные).
Для админки и рассылок — get_db() с переподключением при обрыве.
"""
import threading
import logging
from config import settings

logger = logging.getLogger(__name__)
local = threading.local()

_DATABASE_URL = (settings.DATABASE_URL or "").strip()
if not _DATABASE_URL or not _DATABASE_URL.lower().startswith("postgresql://"):
    raise ValueError(
        "Нужен DATABASE_URL Supabase (postgresql://...) в .env бота 2. "
        "Используйте ту же строку, что и для бота 1 (общая БД)."
    )


def _connect():
    """Одно новое подключение к PostgreSQL."""
    import psycopg2
    return psycopg2.connect(_DATABASE_URL, connect_timeout=15)


# --- Подписка: каждый раз новое подключение ---

def get_subscription_status(telegram_id: int) -> tuple[bool, bool]:
    """
    Статус подписки по telegram_id. Каждый вызов — новое подключение (актуальные данные).
    Возвращает (is_premium, is_active).
    """
    conn = _connect()
    try:
        cur = conn.cursor()
        try:
            # Если срок подписки истек — сразу деактивируем флаги.
            cur.execute(
                """
                UPDATE users
                SET is_premium = 0, is_active = 0, updated_at = CURRENT_TIMESTAMP
                WHERE telegram_id = %s
                  AND premium_until IS NOT NULL
                  AND premium_until <= CURRENT_TIMESTAMP
                  AND (is_premium = 1 OR is_active = 1)
                """,
                (telegram_id,),
            )
            conn.commit()

            cur.execute(
                """
                SELECT
                    CASE
                        WHEN premium_until IS NULL THEN is_premium
                        WHEN premium_until > CURRENT_TIMESTAMP THEN 1
                        ELSE 0
                    END AS effective_premium,
                    CASE
                        WHEN premium_until IS NULL THEN is_active
                        WHEN premium_until > CURRENT_TIMESTAMP THEN 1
                        ELSE 0
                    END AS effective_active
                FROM users
                WHERE telegram_id = %s
                """,
                (telegram_id,),
            )
            row = cur.fetchone()
        except Exception:
            # Совместимость до миграции: если premium_until еще не существует
            conn.rollback()
            cur.execute(
                "SELECT is_premium, is_active FROM users WHERE telegram_id = %s",
                (telegram_id,),
            )
            row = cur.fetchone()
        cur.close()
        if not row:
            return False, False
        return bool(row[0]), bool(row[1])
    finally:
        conn.close()

def init_db():
    """Проверка подключения к БД (таблицы создаёт бот 1)."""
    conn = _connect()
    try:
        cur = conn.cursor()
        cur.execute("SELECT 1")
        cur.close()
        logger.info("Database connection OK")
    finally:
        conn.close()


# --- get_db() для админки и рассылок (совместимо с bot-1 API) ---

import psycopg2
from psycopg2.extras import RealDictCursor


class _RowWithIndex:
    """Строка как dict + доступ по индексу row[0], row[1]."""
    def __init__(self, d, keys=None):
        self._d = d
        self._keys = keys or list(d.keys()) if d else []

    def __getitem__(self, key):
        if isinstance(key, int):
            return self._d[self._keys[key]]
        return self._d[key]

    def keys(self):
        return self._d.keys()

    def get(self, key, default=None):
        return self._d.get(key, default)

    def __contains__(self, key):
        return key in self._d


class _PGCursorWrapper:
    def __init__(self, conn):
        self._conn = conn
        self._cursor = conn.cursor(cursor_factory=RealDictCursor)
        self._lastrowid = None

    def execute(self, sql, params=None):
        sql = sql.replace("?", "%s")
        self._cursor.execute(sql, params or ())
        if sql.strip().upper().startswith("INSERT"):
            self._cursor.execute("SELECT lastval()")
            r = self._cursor.fetchone()
            self._lastrowid = list(r.values())[0] if r else None

    def _wrap(self, row):
        return _RowWithIndex(row, list(row.keys())) if row else None

    def fetchone(self):
        r = self._cursor.fetchone()
        return self._wrap(r)

    def fetchall(self):
        return [self._wrap(row) for row in self._cursor.fetchall()]

    @property
    def rowcount(self):
        return self._cursor.rowcount

    @property
    def lastrowid(self):
        return self._lastrowid


class _PGConnection:
    def __init__(self, conn):
        self._conn = conn

    def cursor(self):
        return _PGCursorWrapper(self._conn)

    def commit(self):
        self._conn.commit()

    def close(self):
        self._conn.close()


def get_db():
    """Возвращает живое подключение; при закрытом/мёртвом соединении создаёт новое."""
    if hasattr(local, "connection"):
        try:
            c = local.connection._conn
            if getattr(c, "closed", 1) != 0:
                raise psycopg2.InterfaceError("connection closed")
            cur = c.cursor()
            cur.execute("SELECT 1")
            cur.close()
            return local.connection
        except Exception:
            try:
                del local.connection
            except Exception:
                pass
    local.connection = _PGConnection(_connect())
    return local.connection
