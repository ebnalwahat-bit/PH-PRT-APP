import sqlite3
import os

class LocalDB:
    def __init__(self):
        self.db_path = "inventory.db"
        self.init_db()

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def init_db(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS parts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    category TEXT,
                    quantity INTEGER DEFAULT 0,
                    price REAL DEFAULT 0.0,
                    description TEXT,
                    compatibility TEXT
                )
            ''')
            conn.commit()

    def add_part(self, name, category, quantity, price, description, compatibility):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO parts (name, category, quantity, price, description, compatibility)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (name, category, quantity, price, description, compatibility))
            conn.commit()

    def get_all_parts(self, search_query=None):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if search_query:
                cursor.execute("SELECT * FROM parts WHERE name LIKE ? OR category LIKE ?", (f'%{search_query}%', f'%{search_query}%'))
            else:
                cursor.execute("SELECT * FROM parts")
            return cursor.fetchall()

    def get_part_by_id(self, part_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM parts WHERE id = ?", (part_id,))
            return cursor.fetchone()

    def update_part(self, part_id, name, category, quantity, price, description, compatibility):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE parts 
                SET name=?, category=?, quantity=?, price=?, description=?, compatibility=?
                WHERE id=?
            ''', (name, category, quantity, price, description, compatibility, part_id))
            conn.commit()

    def delete_part(self, part_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM parts WHERE id = ?", (part_id,))
            conn.commit()
