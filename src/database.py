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
        CREATE TABLE IF NOT EXISTS jobs (
            tid TEXT PRIMARY KEY,
            title TEXT,
            company TEXT,
            description TEXT
        );
        """)

def upsert_job(tid, title, company, description):
    query = """
        INSERT INTO jobs(tid, job, company, description)
        VALUES (?,?,?,?)
        ON CONLFICT(tid) DO UPDATE SET
            title = excluded.title
            company = excluded.company
            description = excluded.description
        """
    get_connection().execute(query, (tid,title,company,description))

if __name__ == "__main__":
    # init_db()
    # conn.commit()
    pass