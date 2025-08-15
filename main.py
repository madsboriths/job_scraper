from src.pipeline import scrape_and_store

import typer

app = typer.Typer()

JOBINDEX_URL = "https://www.jobindex.dk/jobsoegning?geoareaid=1221&geoareaid=56&geoareaid=15182&geoareaid=15178&subid=1&subid=2&subid=3&subid=4&subid=6&subid=7&subid=93"

MAX_PAGES = 3
MAX_JOBS = 3

@app.command("extract-jobs")
def extract_jobs(url: str = typer.Option(JOBINDEX_URL, "--url", "-u",
                                         help="URL to extract jobs from"),
                 max_jobs: int = typer.Option(MAX_JOBS, "--max-jobs", "-n",
                                              help="Specify maximum number of jobs to scrape"),
                 max_pages: int = typer.Option(MAX_PAGES, "--max-pages", "-p",
                                              help="Specify maximum number of pages to scrape")):
    try:
        scrape_and_store(url, max_jobs=max_jobs, max_pages=max_pages)   
    except Exception as e:
        typer.echo(f"An error occurred: {e}")
    pass

if __name__ == "__main__":
    app()