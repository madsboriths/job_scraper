from pathlib import Path
from .scrape import fetch_html
from .data_processing import extract_stash_text, extract_jobs_from_stash, strip_html
from .database import upsert, get_connection

def scrape_and_store(base_url, max_jobs, max_pages):
    num_jobs = 0
    num_pages = 0
    
    conn = get_connection()
    for page in range(1, max_pages + 1):
        if num_pages < max_pages:
            url = base_url + f"&page={page}"
            page_html = fetch_html(url)
            page_stash = extract_stash_text(page_html)
            jobs = extract_jobs_from_stash(page_stash)
            
            for job in jobs:
                if num_jobs < max_jobs:
                    job_tid = job["tid"]
                    job_title = job["headline"]
                    job_company = job["companytext"]
                    job_description = strip_html()
                    print(f"Job ID: {job_tid}, Title: {job_title}, Company: {job_company}, Description: {job_description}")
                    
                    # job_post_html = fetch_html(job["share_url"])
                    # job_post_stash = extract_stash_text(job_post_html)

                    #TODO: Add to database
                    num_jobs += 1
                else:
                    break
            num_pages += 1
        else:
            break
        conn.commit()