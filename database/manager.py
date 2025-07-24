# database/manager.py

import sqlite3
from datetime import datetime

DB_PATH = "Tezus.db"

class DatabaseManager:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()

    # USER PROFILE
    def fetch_user_profile(self) -> dict:
        self.cursor.execute("SELECT key, value FROM user_profile")
        return {k: v for k, v in self.cursor.fetchall()}

    def update_user_profile(self, key: str, value: str):
        self.cursor.execute("REPLACE INTO user_profile (key, value) VALUES (?, ?)", (key, value))
        self.conn.commit()

    # TASK HISTORY
    def log_task(self, intent: str, plugin: str, action: str, result: str):
        timestamp = datetime.now().isoformat()
        self.cursor.execute("""
            INSERT INTO task_history (timestamp, intent, plugin, action, result)
            VALUES (?, ?, ?, ?, ?)
        """, (timestamp, intent, plugin, action, result))
        self.conn.commit()

    # PERMISSIONS
    def get_permission(self, plugin_action: str) -> str:
        self.cursor.execute("SELECT decision FROM permissions WHERE plugin_action = ?", (plugin_action,))
        row = self.cursor.fetchone()
        return row[0] if row else None

    def set_permission(self, plugin_action: str, decision: str):
        self.cursor.execute("REPLACE INTO permissions (plugin_action, decision) VALUES (?, ?)", (plugin_action, decision))
        self.conn.commit()

    # PLUGIN USAGE
    def increment_plugin_usage(self, plugin: str, action: str):
        timestamp = datetime.now().isoformat()
        self.cursor.execute("""
            INSERT INTO plugin_usage (plugin, action, count, last_used)
            VALUES (?, ?, 1, ?)
            ON CONFLICT(plugin, action)
            DO UPDATE SET count = count + 1, last_used = excluded.last_used
        """, (plugin, action, timestamp))
        self.conn.commit()

    def close(self):
        self.conn.close()
