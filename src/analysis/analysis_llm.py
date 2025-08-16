from openai import OpenAI
import os

from pathlib import Path

API_KEY = os.environ["OPENAI_API_KEY"]
client = OpenAI(api_key=API_KEY)

def analyze_text(text: str) -> str:
    prompt_path = Path("prompts/analysis_prompt.txt")

    with open(prompt_path, "r", encoding="utf-8") as file:
        prompt = file.read().strip()
    
    try:
        response = client.responses.create(
            model="gpt-5-nano",
            input=prompt,
        )
    except Exception as e:
        raise RuntimeError(f"Failed to analyze text with OpenAI API: {e}") from e
    return response.output_text.strip()