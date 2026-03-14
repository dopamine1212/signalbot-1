"""
База данных: только Supabase (PostgreSQL).
Оба бота (signal-bot-1 и signal-bot-2) используют одну БД — укажите DATABASE_URL в .env.
"""
import threading
import logging
from typing import Optional, Dict, List
from config import settings

logger = logging.getLogger(__name__)
local = threading.local()

_DATABASE_URL = (settings.DATABASE_URL or "").strip()
if not _DATABASE_URL or not _DATABASE_URL.lower().startswith("postgresql://"):
    raise ValueError(
        "Нужен DATABASE_URL Supabase (postgresql://...). "
        "См. signal-bot-1/SUPABASE_SETUP.md и укажите строку из Settings → Database → Connection string (URI) в .env"
    )
if "[REGION]" in _DATABASE_URL or "[YOUR-PASSWORD]" in _DATABASE_URL or "[PROJECT-REF]" in _DATABASE_URL:
    raise ValueError(
        "DATABASE_URL содержит плейсхолдеры. Замените [PROJECT-REF], [YOUR-PASSWORD], [REGION] на реальные данные из Supabase."
    )
# Хост db.xxx.supabase.co (Direct) часто даёт "No route to host" — нужен pooler с хостом pooler.supabase.com
if "db." in _DATABASE_URL and "supabase.co" in _DATABASE_URL:
    raise ValueError(
        "В DATABASE_URL указан хост db....supabase.co (прямое подключение). Он часто даёт 'No route to host'. "
        "Нужна строка с Pooler: в Supabase нажмите Connect → вкладка Connection String → в Method выберите "
        "'Session pooler' или 'Transaction pooler'. Скопируйте **целиком** новую строку (хост будет pooler.supabase.com, порт 6543), "
        "подставьте пароль и вставьте в .env. Не меняйте только порт в старой строке — нужен именно другой хост."
    )

USE_SUPABASE = True

if USE_SUPABASE:
    import psycopg2
    from psycopg2.extras import RealDictCursor

    class _RowWithIndex:
        """Строка как dict + доступ по индексу row[0], row[1] для совместимости с sqlite3.Row."""
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

    def _set_statement_timeout(conn, seconds=60):
        """Увеличивает таймаут запросов (Supabase по умолчанию обрывает через 3–8 сек)."""
        try:
            with conn.cursor() as cur:
                cur.execute("SET statement_timeout = %s", (f"{seconds}s",))
        except Exception:
            pass

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
                _set_statement_timeout(c)
                return local.connection
            except Exception:
                try:
                    del local.connection
                except Exception:
                    pass
        conn = psycopg2.connect(settings.DATABASE_URL, connect_timeout=15)
        _set_statement_timeout(conn, 60)
        local.connection = _PGConnection(conn)
        return local.connection

    def init_db():
        conn = get_db()._conn
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id BIGSERIAL PRIMARY KEY,
                telegram_id BIGINT UNIQUE NOT NULL,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                is_active INTEGER DEFAULT 1,
                is_premium INTEGER DEFAULT 0,
                balance DOUBLE PRECISION DEFAULT 0.0,
                split_group INTEGER DEFAULT 1,
                premium_until TIMESTAMPTZ,
                subscription_months INTEGER,
                subscription_activated_at TIMESTAMPTZ,
                created_at TIMESTAMPTZ DEFAULT NOW(),
                updated_at TIMESTAMPTZ
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS payments (
                id BIGSERIAL PRIMARY KEY,
                user_id BIGINT NOT NULL REFERENCES users(id),
                amount DOUBLE PRECISION NOT NULL,
                currency TEXT DEFAULT 'USD',
                crypto_currency TEXT,
                status TEXT DEFAULT 'pending',
                transaction_hash TEXT,
                payment_id TEXT UNIQUE,
                payment_url TEXT,
                subscription_months INTEGER,
                subscription_until TIMESTAMPTZ,
                created_at TIMESTAMPTZ DEFAULT NOW(),
                updated_at TIMESTAMPTZ
            )
        """)
        # Миграция для уже существующих таблиц
        cur.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS premium_until TIMESTAMPTZ")
        cur.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS subscription_months INTEGER")
        cur.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS subscription_activated_at TIMESTAMPTZ")
        cur.execute("ALTER TABLE payments ADD COLUMN IF NOT EXISTS subscription_months INTEGER")
        cur.execute("ALTER TABLE payments ADD COLUMN IF NOT EXISTS subscription_until TIMESTAMPTZ")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS signals (
                id BIGSERIAL PRIMARY KEY,
                text TEXT,
                photo_ids TEXT,
                is_active INTEGER DEFAULT 1,
                split_group INTEGER DEFAULT 0,
                created_at TIMESTAMPTZ DEFAULT NOW(),
                created_by BIGINT
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS admins (
                id BIGSERIAL PRIMARY KEY,
                telegram_id BIGINT UNIQUE NOT NULL,
                username TEXT,
                first_name TEXT,
                added_at TIMESTAMPTZ DEFAULT NOW(),
                added_by BIGINT
            )
        """)
        conn.commit()
        cur.close()
        if settings.ADMIN_IDS:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            for admin_id in settings.ADMIN_IDS:
                cur.execute("SELECT 1 FROM admins WHERE telegram_id = %s", (admin_id,))
                if not cur.fetchone():
                    cur.execute("INSERT INTO admins (telegram_id) VALUES (%s) ON CONFLICT (telegram_id) DO NOTHING", (admin_id,))
            conn.commit()
            cur.close()
        logger.info("Supabase (PostgreSQL) DB initialized")


# Статусы платежей
class PaymentStatus:
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
