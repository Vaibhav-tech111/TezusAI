import sqlite3
from datetime import datetime
from contextlib import contextmanager
import os

DB_PATH = os.environ.get("TEZUS_DB_PATH", "Tezus.db")

class DatabaseManager:
    def __init__(self):
        self.conn = None
        self.cursor = None

    @contextmanager
    def manage_connection(self):
        try:
            self.conn = sqlite3.connect(DB_PATH)
            self.cursor = self.conn.cursor()
            yield
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            if self.conn:
                self.conn.rollback()
        finally:
            if self.conn:
                self.conn.close()
                self.conn = None
                self.cursor = None


    # USER PROFILE
    def fetch_user_profile(self, key=None) -> dict:
        with self.manage_connection():
            if key:
                self.cursor.execute("SELECT value FROM user_profile WHERE key = ?", (key,))
                row = self.cursor.fetchone()
                return row[0] if row else None
            else:
                self.cursor.execute("SELECT key, value FROM user_profile")
                return {k: v for k, v in self.cursor.fetchall()}

    def update_user_profile(self, key: str, value: str):
        key = key.replace("'", "''") #Simple sanitization
        value = value.replace("'", "''") #Simple sanitization
        with self.manage_connection():
            self.cursor.execute("REPLACE INTO user_profile (key, value) VALUES (?, ?)", (key, value))


    # TASK HISTORY
    def log_task(self, intent: str, plugin: str, action: str, result: str):
        timestamp = datetime.now().isoformat()
        with self.manage_connection():
            self.cursor.execute("""
                INSERT INTO task_history (timestamp, intent, plugin, action, result)
                VALUES (?, ?, ?, ?, ?)
            """, (timestamp, intent, plugin, action, result))

    # PERMISSIONS
    def get_permission(self, plugin_action: str) -> str:
        with self.manage_connection():
            self.cursor.execute("SELECT decision FROM permissions WHERE plugin_action = ?", (plugin_action,))
            row = self.cursor.fetchone()
            return row[0] if row else None

    def set_permission(self, plugin_action: str, decision: str):
        with self.manage_connection():
            self.cursor.execute("REPLACE INTO permissions (plugin_action, decision) VALUES (?, ?)", (plugin_action, decision))


    # PLUGIN USAGE
    def increment_plugin_usage(self, plugin: str, action: str):
        timestamp = datetime.now().isoformat()
        with self.manage_connection():
            self.cursor.execute("""
                INSERT INTO plugin_usage (plugin, action, count, last_used)
                VALUES (?, ?, 1, ?)
                ON CONFLICT(plugin, action)
                DO UPDATE SET count = count + 1, last_used = datetime(?)
            """, (plugin, action, timestamp, timestamp))