import requests
from bs4 import BeautifulSoup
import random, time, logging

logger = logging.getLogger(__name__)

headers = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET",
    "Access-Control-Allow-Headers": "Content-Type",
    "Accept-Encoding": "utf-8",
    "Access-Control-Max-Age": "3600"
}

# TODO: Add capability of caching
def fetch_html(url: str) -> BeautifulSoup:
    req = requests.get(url, headers=headers)
    soup = BeautifulSoup(req.text, "html.parser")
    return soup

def random_sleep(min_s: float = 1.0, max_s: float = 3.0) -> float:
    t = random.uniform(min_s, max_s)
    logger.info("Sleeping %.2fs", t)
    time.sleep(t)
    return t