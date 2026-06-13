import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "taskmanager.db"

conn = sqlite3.connect(DB_PATH, check_same_thread=False)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()


def init_db() -> None:
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT NOT NULL,
        password TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        title TEXT NOT NULL,
        description TEXT DEFAULT '',
        priority TEXT DEFAULT 'Medium',
        due_date TEXT,
        completed INTEGER DEFAULT 0,
        category TEXT DEFAULT 'General',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(username) REFERENCES users(username)
    )
    """)

    # Add category column safely for old databases.
    cursor.execute("PRAGMA table_info(tasks)")
    columns = [row[1] for row in cursor.fetchall()]
    if "category" not in columns:
        cursor.execute("ALTER TABLE tasks ADD COLUMN category TEXT DEFAULT 'General'")
    if "created_at" not in columns:
        cursor.execute("ALTER TABLE tasks ADD COLUMN created_at TEXT DEFAULT CURRENT_TIMESTAMP")

    conn.commit()


def row_to_dict(row):
    if row is None:
        return None
    data = dict(row)
    if "completed" in data:
        data["completed"] = bool(data["completed"])
    return data


init_db()
