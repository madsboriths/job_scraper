from .scrape import fetch_html, random_sleep
from .data_processing import extract_stash_text, extract_jobs_from_stash
from .html_processing import strip_html
from .database import upsert, get_connection

import logging

logger = logging.getLogger(__name__)

SLEEP_MIN = 1.8
SLEEP_MAX = 5.4
LONG_PAUSE_EVERY = 14
LONG_PAUSE_MIN = 35.0
LONG_PAUSE_MAX = 60.0

def scrape_and_store(base_url, max_jobs=1, max_pages=1, starting_page=1):
    num_jobs = 0
    num_pages = 0

    conn = get_connection()
    for page in range(starting_page, starting_page + max_pages + 1):
        if num_pages < max_pages:
            url = base_url + f"&page={page}"
            logger.info(f"Fetching page {page} of {starting_page + max_pages}...")
            random_sleep(SLEEP_MIN, SLEEP_MAX)

            page_html = fetch_html(url)
            page_stash = extract_stash_text(page_html)
            jobs = extract_jobs_from_stash(page_stash)
            
            for job in jobs:
                if num_jobs < max_jobs:
                    logger.info(f"Processing job {job['tid']} from page {page}...")
                    random_sleep(SLEEP_MIN, SLEEP_MAX)
                    job_html = fetch_html(job["url"])
                    job_data = {
                        "tid": job["tid"],
                        "title": job["headline"],
                        "company": job["companytext"],
                        "description": strip_html(job_html)
                    }
                    upsert(conn, "jobs", "tid", job_data)
                    num_jobs += 1
                    if num_jobs % LONG_PAUSE_EVERY == 0:
                        logger.info(f"Pausing for a longer duration after {num_jobs} jobs...")
                        random_sleep(LONG_PAUSE_MIN, LONG_PAUSE_MAX)
                else:
                    break
            num_pages += 1
            logger.info(f"Stored {num_jobs} jobs from {num_pages} pages. Committing changes...")
            conn.commit()
        else:
            break
        logger.info(f"Finished scraping. Total jobs stored: {num_jobs}. Committing changes...")
        conn.commit()