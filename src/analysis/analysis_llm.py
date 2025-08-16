from pathlib import Path
import os, json, sqlite3
from src.database import get_connection, upsert, retrieve_row_from_table
from openai import OpenAI
import logging

API_KEY = os.environ["OPENAI_API_KEY"]
client = OpenAI(api_key=API_KEY)

def process_description(conn: sqlite3.Connection, job_id: str, description: str):
    gpt_response, _ = retrieve_text_insights(description)
    gpt_response_dict = json.loads(gpt_response)

    # dump for debugging
    with open(f"gpt_response.json", "w", encoding="utf-8") as f:
        json.dump(gpt_response_dict, f, indent=2, ensure_ascii=False)

    seen = set()
    for entity in gpt_response_dict["roles"]:

        if entity["canonical"] in seen:
            continue
        seen.add(entity["canonical"])

        previous_count = retrieve_row_from_table(conn, "nodes", "entity", entity["canonical"])
        previous_count = 0 if previous_count is None else previous_count["count"]

        data = {
            "entity": entity["canonical"],
            "type": "role",
            "count": previous_count + 1 
        }
        upsert(conn, "nodes", "entity", data)

    for entity in gpt_response_dict["skills"].items():
        for sub_entity in entity[1]:
            if sub_entity["canonical"] in seen:
                continue
            seen.add(sub_entity["canonical"])

            previous_count = retrieve_row_from_table(conn, "nodes", "entity", sub_entity["canonical"])
            previous_count = 0 if previous_count is None else previous_count["count"]
            data = {
                "entity": sub_entity["canonical"],
                "type": entity[0],
                "count": previous_count + 1 
            }
            upsert(conn, "nodes", "entity", data)

def retrieve_text_insights(description: str) -> str:
    sys_path = Path("prompts/analysis_prompt.txt")
    with open(sys_path, "r", encoding="utf-8") as file:
        system_prompt = file.read().strip()

    usr_path = Path("prompts/analysis_user_prompt.txt")
    with open(usr_path, "r", encoding="utf-8") as f:
        user_prompt_template = f.read().strip()
    user_prompt = user_prompt_template.replace("{{job_description_text}}", description)

    try:
        response = client.chat.completions.create(
            model="gpt-5-nano",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ]
        )
    except Exception as e:
        raise RuntimeError(f"Failed to analyze text with OpenAI API: {e}") from e
    return response.choices[0].message.content, "gpt-5-nano"

def was_processed(conn: sqlite3.Connection, job_id: str, version: str) -> bool:
    row = conn.execute(
        "SELECT 1 FROM processed_jobs WHERE job_id=? AND version=?",
        (job_id, version)
    ).fetchone()
    return row is not None

def mark_processed(conn: sqlite3.Connection, job_id: str, version: str) -> None:
    conn.execute(
        """
        INSERT INTO processed_jobs(job_id, version)
        VALUES (?, ?)
        ON CONFLICT(job_id, version) DO NOTHING
        """,
        (job_id, version)
    )

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    conn = get_connection()
    with open("schema.sql", "r", encoding="utf-8") as file:
        schema_sql = file.read()
        conn.executescript(schema_sql)
    cur = conn.execute("SELECT tid, title, description FROM jobs")
    
    n = cur.fetchall()
    logger.info(f"Found {len(n)} jobs in the database.")
    for row in n:
        if row:
            job_id, title, description = row["tid"], row["title"], row["description"]
            if not was_processed(conn, job_id, "v1"):
                logger.info(f"Processing job {job_id} with title '{title}...'")
                try:
                    process_description(conn, job_id=job_id, description=description)
                    mark_processed(conn, job_id, "v1")
                    conn.commit()
                except Exception as e:
                    logger.error(f"An error occurred while processing jobs: {e}")
            else:
                logger.info(f"Skipping {job_id} (already processed v1)")
        else:
            logger.info("No jobs found to process.")
