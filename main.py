from src.scrape import fetch_html
from src.data_processing import find_stash_json_string
from src.data_processing import get_jobs_list_from_path

if __name__ == "__main__":
    INITIAL_SEARCH_URL = "https://www.jobindex.dk/jobsoegning?geoareaid=1221&geoareaid=56&geoareaid=15182&geoareaid=15178&subid=1&subid=2&subid=3&subid=4&subid=6&subid=7&subid=93"
    try:
        html_soup = fetch_html(INITIAL_SEARCH_URL)
        stash_text = find_stash_json_string(html_soup)
        jobs = get_jobs_list_from_path(stash_text)
    except:
        print("Failed to retrieve jobs...")