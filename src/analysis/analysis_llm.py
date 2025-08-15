from openai import OpenAI
import os

API_KEY = os.environ["OPENAI_API_KEY"]
client = OpenAI(api_key=API_KEY)

def analyze_text(text: str) -> str:
    try:
        response = client.responses.create(
            model="gpt-5-nano",
            input=f"Analyze the following text:\n{text}",
        )
    except Exception as e:
        raise RuntimeError(f"Failed to analyze text with OpenAI API: {e}") from e
    return response.output_text.strip()