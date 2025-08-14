from bs4 import BeautifulSoup
from typing import Dict, List, Any
from pathlib import Path
import json
import re

from scrape import fetch_html

DATA_DIRECTORY = Path("data/")
STASH_RE = re.compile(r"var\s+Stash\s*=\s*(\{.*?\});", re.DOTALL)

class StashNotFound(Exception): ...
class JobsShapeError(Exception): ...

def find_stash_json_string(html_soup: BeautifulSoup) -> str:
    for script in html_soup.find_all("script"):
        text = script.string or script.get_text() or ""
        m = STASH_RE.search(text)
        if m:
            return m.group(1)
    raise StashNotFound("Could not find 'var Stash = { ... } in any <script> tag")

def json_string_to_dict(json_string: str) -> Dict[str, Any]:
    try:
        return json.loads(json_string)
    except json.JSONDecodeError as e:
        raise ValueError("Invalid JSON format in string") from e
    
def extract_jobs_from_stash_dict(stash_dict: Dict[str, Any]) -> List[Dict[str, Any]]:
    try:
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

if __name__ == "__main__":
    json_stash = load_json(DATA_DIRECTORY / "stash.json")
    jobs = extract_jobs_from_stash_dict(json_stash)
    for job in jobs[:2]:
        job_title = job["headline"]
        job_url = job["url"]

        stash_json_string = find_stash_json_string(fetch_html(job_url))
        stash_dict = json_string_to_dict(stash_json_string)
        save_json(stash_dict, DATA_DIRECTORY / f"{job_title}" / "stash.json")
