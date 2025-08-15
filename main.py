from src.pipeline import scrape_and_store

import typer

app = typer.Typer()
INITIAL_SEARCH_URL = "https://www.jobindex.dk/jobsoegning?geoareaid=1221&geoareaid=56&geoareaid=15182&geoareaid=15178&subid=1&subid=2&subid=3&subid=4&subid=6&subid=7&subid=93"

@app.command("extract-jobs")
def extract_jobs(num_jobs: int = typer.Option(None, "--num-jobs", "-n",
                                              help="Specify maximum number of jobs to scrape")):
    try:
        scrape_and_store()        
    except:
        print("Failed to retrieve jobs...")
    pass

if __name__ == "__main__":
    app()