"""Bot 2 services: admin check only."""
from database import get_db


class AdminService:
    @staticmethod
    def is_admin(telegram_id: int) -> bool:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM admins WHERE telegram_id = ?", (telegram_id,))
        return cursor.fetchone() is not None


class BanService:
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
