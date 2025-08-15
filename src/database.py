import sqlite3
from pathlib import Path
from typing import Mapping

DATABASE_PATH = Path("jobs.db")

SQLITE_TYPE_MAP = {
    str: "TEXT",
    float: "REAL",
    int: "INTEGER",
    bool: "BOOLEAN",
}

def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def create_table_with_primary_key(conn:sqlite3.Connection, table: str, pk: str, data: Mapping[str, object])-> None:
    if pk not in data:
        raise ValueError(f"Primary key '{pk}' missing in data")
    
    cols = list(data.keys())
    types = [SQLITE_TYPE_MAP[type(data[col])] for col in cols]

    for name, col_type in zip(cols, types):
        print(name, col_type)

    col_defs = ", ".join(f"{name} {col_type}" for name, col_type in zip(cols, types))
    sql_query = f"""
        CREATE TABLE IF NOT EXISTS {table}
        ({pk} TEXT PRIMARY KEY, {col_defs}"""
    conn.execute(sql_query)

def upsert_job(conn:sqlite3.Connection, table: str, pk: str, data: Mapping[str, object])-> None:
    if pk not in data:
        raise ValueError(f"Primary key '{pk}' missing in data") 
    
    cols = list(data.keys())
    placeholders = ",".join(["?"] * len(cols))

    update_cols = [c for c in cols if c != pk]
    update_assign = ",".join([f"{c}=excluded.{c}" for c in update_cols])

    sql_query = f"""
        INSERT INTO {table} ({",".join(cols)})
        VALUES ({placeholders})
        ON CONFLICT ({pk}) DO UPDATE SET
            {update_assign}
    """ 
    conn.execute(sql_query)

if __name__ == "__main__":
    conn = get_connection()
    create_table_with_primary_key(conn, "jobs", "tid", {
        "tid": "12345",
        "title": "Software Engineer",
        "company": "Tech Company",
        "description": "Developing software solutions."
        })
    conn.commit()