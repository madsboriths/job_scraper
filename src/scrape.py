from typing import List
import requests
from bs4 import BeautifulSoup
import json
import re
from src.data_processing import extract_json_from_soup

headers = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET",
    "Access-Control-Allow-Headers": "Content-Type",
    "Accept-Encoding": "utf-8",
    "Access-Control-Max-Age": "3600"
}

def scrape_soup_from_url(url):
    print(f"Scraping from:{url}")
    req = requests.get(url, headers=headers)
    soup = BeautifulSoup(req.text, "html.parser")
    return soup