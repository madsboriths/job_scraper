import sqlite3
# db.py
import sqlite3
from pathlib import Path

DB_PATH = Path("jobs.db")

def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db() -> None:
    with get_connection() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS job (
            id TEXT PRIMARY KEY,
            title TEXT,
            company TEXT,
            description TEXT
        );
        """)

if __name__ == "__main__":
    get_connection.commit()