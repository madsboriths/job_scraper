from bs4 import BeautifulSoup
from typing import Dict, List, Any
from pathlib import Path
import json
import re

from openai import OpenAI
from pathlib import Path
import os

API_KEY = os.environ["OPENAI_API_KEY"]
client = OpenAI(api_key=API_KEY)

STASH_RE = re.compile(r"var\s+Stash\s*=\s*(\{.*?\});", re.DOTALL)

class StashNotFound(Exception): ...
class JobsShapeError(Exception): ...

def strip_html(html: str) -> str:
    prompt_path = Path("prompts/retrieval_prompt.txt")

    with open(prompt_path, "r", encoding="utf-8") as file:
        prompt = file.read().strip()
    try:
        response = client.responses.create(
            model="gpt-5-nano",
            input=f"{prompt}\n\nHTML:\n{html}",
        )
    except Exception as e:
        raise RuntimeError(f"Failed to process HTML with OpenAI API: {e}") from e
    return response.output_text.strip()

def extract_stash_text(html_soup: BeautifulSoup) -> str:
    try:
        for script in html_soup.find_all("script"):
            text = script.string or script.get_text() or ""
            m = STASH_RE.search(text)
            if m:
                return m.group(1)
    except Exception as e:
        raise StashNotFound("Could not find 'var Stash = { ... } in any <script> tag") from e
    
def convert_to_json(json_string: str) -> Dict[str, Any]:
    try:
        return json.loads(json_string)
    except json.JSONDecodeError as e:
        raise ValueError("Invalid JSON format in string") from e
    
def extract_jobs_from_stash(stash_text: str) -> List[Dict[str, Any]]:
    try:
        stash_dict = convert_to_json(stash_text)
        return stash_dict["jobsearch/result_app"]["storeData"]["searchResponse"]["results"]
    except Exception as e:
        raise JobsShapeError("Invalid format jobs in dict") from e

def save_json(object: Dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(object, f, indent=2, ensure_ascii=False)
    
def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)
    
