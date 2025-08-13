from bs4 import BeautifulSoup
from typing import List
import json
import re

DEFAULT_PATH = "data/stash.json"

def extract_json_from_soup(soup: BeautifulSoup, save_to_file: bool = False) -> List[dict]:
    scripts = soup.find_all("script")
    for script in scripts:
        if script.string and "var Stash" in script.string:
            pattern = r"var\s+Stash\s*=\s*(\{.*?\});"
            match = re.search(pattern, script.string, flags=re.DOTALL)
            if match:
                raw_json = match.group(1)            
                parsed_json = json.loads(raw_json)

    if save_to_file:
        with open("data/stash.json", "w", encoding="utf-8") as f:
            json.dump(parsed_json, f, indent=2, ensure_ascii=False)

def get_jobs_list(path: str = None) -> List:
    if path is None:
        path = DEFAULT_PATH

    with open(path, "r", encoding="utf-8") as f:
        stash = json.load(f)
    return stash["jobsearch/result_app"]["storeData"]["searchResponse"]["results"]

if __name__ == "__main__":
    jobs = get_jobs_list()
    print(jobs[0].keys())