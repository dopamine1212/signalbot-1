"""Bot 2 services: admin check only."""
from database import get_db


class AdminService:
    @staticmethod
    def is_admin(telegram_id: int) -> bool:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM admins WHERE telegram_id = ?", (telegram_id,))
        return cursor.fetchone() is not None
