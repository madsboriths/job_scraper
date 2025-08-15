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

def create_table_with_primary_key(conn:sqlite3.Connection, table: str, pk: str, data: list[str])-> None:
    if pk not in data.keys():
        raise ValueError(f"Primary key '{pk}' missing in data")
    
    data = [col for col in data if col != pk]

    types = [SQLITE_TYPE_MAP[type(col)] for col in data]

    col_defs = ", ".join(f"{name} {col_type}" for name, col_type in zip(data, types))
    sql_query = f"""
        CREATE TABLE IF NOT EXISTS {table}
        ({pk} TEXT PRIMARY KEY, {col_defs})"""
    conn.execute(sql_query)

def upsert(conn:sqlite3.Connection, table: str, pk: str, data: Mapping[str, object])-> None:
    if pk not in data.keys():
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
    conn.execute(sql_query, tuple(data.values()))
    
def remove_element(conn:sqlite3.Connection, table: str, tid: str) -> None:
    sql_query = f"DELETE FROM {table} WHERE tid = ?"
    conn.execute(sql_query, (tid,))

def delete_table_if_exists(conn:sqlite3.Connection, table: str) -> None:
    sql_query = f"DROP TABLE IF EXISTS {table}"
    conn.execute(sql_query)