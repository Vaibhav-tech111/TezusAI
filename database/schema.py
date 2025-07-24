# database/schema.py

import sqlite3

def initialize_db():
    conn = sqlite3.connect("Tezus.db")
    cursor = conn.cursor()

    # User memory
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_profile (
        key TEXT PRIMARY KEY,
        value TEXT
    )
    """)

    # Task history
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS task_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        intent TEXT,
        plugin TEXT,
        action TEXT,
        result TEXT
    )
    """)

    # Permissions
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS permissions (
        plugin_action TEXT PRIMARY KEY,
        decision TEXT
    )
    """)

    # Plugin usage
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS plugin_usage (
        plugin TEXT,
        action TEXT,
        count INTEGER DEFAULT 0,
        last_used TEXT
    )
    """)

    conn.commit()
    conn.close()
