from src.scrape import scrape_soup_from_url
from src.data_processing import extract_json_from_soup
from src.data_processing import get_jobs_list

if __name__ == "__main__":
    INITIAL_SEARCH_URL = "https://www.jobindex.dk/jobsoegning?geoareaid=1221&geoareaid=56&geoareaid=15182&geoareaid=15178&subid=1&subid=2&subid=3&subid=4&subid=6&subid=7&subid=93"
    try:
        soup = scrape_soup_from_url(INITIAL_SEARCH_URL)
        formatted_json = extract_json_from_soup(soup, save_to_file=True)
        jobs = get_jobs_list(formatted_json)
    except:
        print("Failed to retrieve jobs...")