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

def get_connection(path: Path = DATABASE_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(path)
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
    
def retrieve_row_from_table(conn: sqlite3.Connection, table: str, pk: str, tid: str):
    sql_query = f"SELECT * FROM {table} WHERE {pk} = ?"
    return conn.execute(sql_query, (tid,)).fetchone()

def delete_row_from_table(conn:sqlite3.Connection, table: str, pk:str, tid: str) -> None:
    sql_query = f"DELETE FROM {table} WHERE {pk} = ?"
    conn.execute(sql_query, (tid,))

def update_row_in_table(conn:sqlite3.Connection, table: str, pk: str, tid: str, data: Mapping[str, object]) -> None:
    if pk not in data.keys():
        raise ValueError(f"Primary key '{pk}' missing in data")
    
    cols = list(data.keys())
    placeholders = ",".join([f"{col}=?" for col in cols])
    
    sql_query = f"UPDATE {table} SET {placeholders} WHERE {pk} = ?"
    conn.execute(sql_query, tuple(data.values()) + (tid,))

def delete_table_if_exists(conn:sqlite3.Connection, table: str) -> None:
    sql_query = f"DROP TABLE IF EXISTS {table}"
    conn.execute(sql_query)

def mark_processed():
    pass

def processed_exists(conn, job_id, version):
    pass