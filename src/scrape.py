import requests
from bs4 import BeautifulSoup

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