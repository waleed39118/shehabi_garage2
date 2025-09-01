"""
database.py - إدارة قاعدة بيانات المشروع (SQLite)
"""

import sqlite3
from pathlib import Path
from typing import List, Tuple, Optional, Union

DB_PATH = Path(__file__).resolve().parent.parent / "shihabi2.db"


class DatabaseManager:
    """
    إدارة قاعدة بيانات SQLite لجميع عمليات المخزون والمستخدمين.
    """

    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        """إنشاء الجداول الأساسية إذا لم تكن موجودة."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS inventory (
                name TEXT NOT NULL,
                part TEXT NOT NULL UNIQUE,
                quantity INTEGER NOT NULL,
                location TEXT,
                condition TEXT,
                last_updated TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT NOT NULL,
                role TEXT NOT NULL,
                can_add INTEGER DEFAULT 0,
                can_edit INTEGER DEFAULT 0,
                can_delete INTEGER DEFAULT 0
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS archive (
                name TEXT,
                part TEXT,
                quantity INTEGER,
                location TEXT,
                condition TEXT,
                date_removed TEXT
            )
        """)
        self.conn.commit()

    # ================= Inventory Operations ================= #

    def get_inventory(self) -> List[dict]:
        """استرجاع جميع الأصناف من المخزون كقائمة قواميس."""
        self.cursor.execute("""
            SELECT name, part AS part_number, quantity, location, condition, last_updated
            FROM inventory
        """)
        return [dict(row) for row in self.cursor.fetchall()]

    def get_item_by_name(self, name: str) -> Optional[Tuple]:
        """استرجاع صنف محدد حسب الاسم."""
        self.cursor.execute("""
            SELECT name, part, quantity, location, condition
            FROM inventory WHERE name = ?
        """, (name,))
        row = self.cursor.fetchone()
        return tuple(row) if row else None

    def get_item_by_part(self, part_number: str) -> Optional[dict]:
        """استرجاع صنف محدد حسب رقم القطعة."""
        self.cursor.execute("""
            SELECT name, part AS part_number, quantity, location, condition, last_updated
            FROM inventory WHERE part = ?
        """, (part_number,))
        row = self.cursor.fetchone()
        return dict(row) if row else None

    def add_item(self, data: dict):
        """إضافة صنف جديد (الاسم القديم للدالة)."""
        self.cursor.execute("""
            INSERT INTO inventory (name, part, quantity, location, condition)
            VALUES (?, ?, ?, ?, ?)
        """, (
            data["name"],
            data.get("part") or data.get("part_number"),
            data["quantity"],
            data.get("location", ""),
            data.get("condition", "New")
        ))
        self.conn.commit()

    def add_inventory_item(self, data: dict):
        """إضافة صنف جديد (الاسم الجديد للدالة)."""
        self.add_item(data)

    def update_item(self, name: str, data: dict):
        """تعديل بيانات صنف موجود (الاسم القديم للدالة)."""
        self.cursor.execute("""
            UPDATE inventory
            SET name = ?, part = ?, quantity = ?, location = ?, condition = ?, last_updated = CURRENT_TIMESTAMP
            WHERE name = ?
        """, (
            data["name"],
            data.get("part") or data.get("part_number"),
            data["quantity"],
            data.get("location", ""),
            data.get("condition", "New"),
            name
        ))
        self.conn.commit()

    def update_inventory_item(self, part_number: str, data: dict):
        """تعديل بيانات صنف موجود (الاسم الجديد للدالة)."""
        self.cursor.execute("""
            UPDATE inventory
            SET name = ?, part = ?, quantity = ?, location = ?, condition = ?, last_updated = CURRENT_TIMESTAMP
            WHERE part = ?
        """, (
            data["name"],
            data.get("part") or data.get("part_number"),
            data["quantity"],
            data.get("location", ""),
            data.get("condition", "New"),
            part_number
        ))
        self.conn.commit()

    def delete_item(self, name: str):
        """حذف صنف ونقله إلى الأرشيف (الاسم القديم للدالة)."""
        item = self.get_item_by_name(name)
        if item:
            self.cursor.execute("""
                INSERT INTO archive (name, part, quantity, location, condition, date_removed)
                VALUES (?, ?, ?, ?, ?, DATE('now'))
            """, item)
            self.cursor.execute("DELETE FROM inventory WHERE name = ?", (name,))
            self.conn.commit()

    def delete_inventory_item(self, part_number: str):
        """حذف صنف ونقله إلى الأرشيف (الاسم الجديد للدالة)."""
        item = self.get_item_by_part(part_number)
        if item:
            self.cursor.execute("""
                INSERT INTO archive (name, part, quantity, location, condition, date_removed)
                VALUES (?, ?, ?, ?, ?, DATE('now'))
            """, (
                item["name"], item["part_number"], item["quantity"],
                item["location"], item["condition"]
            ))
            self.cursor.execute("DELETE FROM inventory WHERE part = ?", (part_number,))
            self.conn.commit()

    def record_outgoing(self, part: str, quantity: int, condition: str):
        """تسجيل خروج صنف (الاسم القديم للدالة)."""
        self._record_outgoing_internal(part, quantity, condition)

    def record_outgoing_item(self, part_number: str, quantity: int, condition: str):
        """تسجيل خروج صنف (الاسم الجديد للدالة)."""
        self._record_outgoing_internal(part_number, quantity, condition)

    def _record_outgoing_internal(self, part: str, quantity: int, condition: str):
        """منطق تسجيل الخروج المشترك."""
        self.cursor.execute("SELECT quantity FROM inventory WHERE part = ?", (part,))
        row = self.cursor.fetchone()
        if not row:
            raise ValueError("Part not found in inventory.")
        current_qty = row["quantity"]
        if quantity > current_qty:
            raise ValueError("Quantity exceeds current stock.")
        new_qty = current_qty - quantity
        self.cursor.execute("""
            UPDATE inventory
            SET quantity = ?, condition = ?, last_updated = CURRENT_TIMESTAMP
            WHERE part = ?
        """, (new_qty, condition, part))
        self.conn.commit()

    # ================= User Operations ================= #

    def create_user(self, username: str, password: str, role: str,
                    can_add: bool, can_edit: bool, can_delete: bool):
        """إنشاء مستخدم جديد."""
        self.cursor.execute("""
            INSERT INTO users (username, password, role, can_add, can_edit, can_delete)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (username, password, role, int(can_add), int(can_edit), int(can_delete)))
        self.conn.commit()

    def get_user(self, username: str) -> Optional[dict]:
        """استرجاع بيانات مستخدم حسب الاسم."""
        self.cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = self.cursor.fetchone()
        if row:
            return {
                "username": row["username"],
                "password": row["password"],
                "role": row["role"],
                "can_add": bool(row["can_add"]),
                "can_edit": bool(row["can_edit"]),
                "can_delete": bool(row["can_delete"])
            }
        return None

    def get_all_users(self) -> List[dict]:
        """استرجاع جميع المستخدمين."""
        self.cursor.execute("SELECT * FROM users")
        return [
            {
                "username": row["username"],
                "role": row["role"],
                "can_add": bool(row["can_add"]),
                "can_edit": bool(row["can_edit"]),
                "can_delete": bool(row["can_delete"])
            }
            for row in self.cursor.fetchall()
        ]

    def update_user(self, username: str, data: dict):
        """تعديل بيانات مستخدم."""
        self.cursor.execute("""
            UPDATE users
            SET password = ?, role = ?, can_add = ?, can_edit = ?, can_delete = ?
            WHERE username = ?
        """, (
            data["password"], data["role"],
            int(data["can_add"]),             int(data["can_delete"]),
            username
        ))
        self.conn.commit()

    def delete_user(self, username: str):
        """حذف مستخدم."""
        self.cursor.execute("DELETE FROM users WHERE username = ?", (username,))
        self.conn.commit()

    def authenticate_user(self, username: str, password: str) -> Optional[dict]:
        """
        التحقق من بيانات تسجيل الدخول.
        تعيد بيانات المستخدم إذا كانت صحيحة، أو None إذا كانت خاطئة.
        """
        self.cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        row = self.cursor.fetchone()
        if row:
            return {
                "username": row["username"],
                "password": row["password"],
                "role": row["role"],
                "can_add": bool(row["can_add"]),
                "can_edit": bool(row["can_edit"]),
                "can_delete": bool(row["can_delete"])
            }
        return None