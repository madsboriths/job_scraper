from openai import OpenAI
from pathlib import Path
import os

API_KEY = os.environ["OPENAI_API_KEY"]
client = OpenAI(api_key=API_KEY)

def strip_html(html: str) -> str:
    with Path("prompt.txt").open("r", encoding="utf-8") as f:
        prompt = f.read()

    try:
        response = client.responses.create(
            model="gpt-5-nano",
            input=f"{prompt}\n\nHTML:\n{html}",
        )
    except Exception as e:
        raise RuntimeError(f"Failed to process HTML with OpenAI API: {e}") from e
    return response.output_text.strip()