import sqlite3
from pathlib import Path

from typing import Mapping

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
        conn.commit()

def upsert_job(conn:sqlite3.Connection, table: str, pk: str, data: Mapping[str, object])-> None:
    if pk not in data:
        raise ValueError(f"Primary key '{pk}' missing in data") 
    
    cols = list(data.keys())
    placeholders = ",".join(["?"] * len(cols))

    update_cols = [c for c in cols if c != pk]
    update_assign = ",".join([f"{c}=excluded.{c}" for c in update_cols])

    sql = f"""
        INSERT INTO {table} ({",".join(cols)})
        VALUES ({placeholders})
        ON CONFLICT ({pk}) DO UPDATE SET
            {update_assign}
    """ 
    print(sql)

if __name__ == "__main__":
    conn = get_connection()
    # upsert_job(conn, "jobs", "tid", {
    #     "tid": "12345",
    #     "title": "Software Engineer",
    #     "company": "Tech Company",
    #     "description": "Developing software solutions.",
    #     "status": "interested"
    # })
    conn.commit()