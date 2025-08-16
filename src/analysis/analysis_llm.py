from pathlib import Path
import os, json, sqlite3
from src.database import get_connection, upsert, retrieve_row_from_table, update_row_in_table
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

    for entity in gpt_response_dict["roles"]:
        previous_count = retrieve_row_from_table(conn, "nodes", "entity", entity["canonical"])
        if previous_count is None:
            previous_count = 0
        else:
            previous_count = previous_count["count"]
        data = {
            "entity": entity["canonical"],
            "type": "role",
            "count": previous_count + 1 
        }
        upsert(conn, "nodes", "entity", data)

    for entity in gpt_response_dict["skills"].items():
        for sub_entity in entity[1]:
            previous_count = retrieve_row_from_table(conn, "nodes", "entity", sub_entity["canonical"])
            if previous_count is None:
                previous_count = 0
            else:
                previous_count = previous_count["count"]
            data = {
                "entity": sub_entity["canonical"],
                "type": entity[0],
                "count": previous_count + 1 
            }
            upsert(conn, "nodes", "entity", data)

def retrieve_text_insights(text: str) -> str:
    prompt_path = Path("prompts/analysis_prompt.txt")
    with open(prompt_path, "r", encoding="utf-8") as file:
        prompt = file.read().strip()
        prompt = prompt.replace("{{job_description_text}}", text)
    try:
        response = client.responses.create(
            model="gpt-5-nano",
            input=prompt,
        )
    except Exception as e:
        raise RuntimeError(f"Failed to analyze text with OpenAI API: {e}") from e
    return response.output_text.strip(), "gpt-5-nano"

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    conn = get_connection()
    with open("schema.sql", "r", encoding="utf-8") as file:
        schema_sql = file.read()
        conn.executescript(schema_sql)
    cur = conn.execute("SELECT tid, title, description FROM jobs")
    logger.info(f"Starting to process {len(cur.fetchall())} jobs...")
    for row in cur.fetchall():
        if row:
            job_id, title, description = row["tid"], row["title"], row["description"]
            if description:
                logger.info(f"Processing job {job_id} with title '{title}...'")
                process_description(conn, job_id=job_id, description=description)
                conn.commit()
            else:
                print("No description found in the job.")
        else:
            print("No jobs found in the database.")