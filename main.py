import logging, re, sys, os
from src import dataParser, dataScraper

logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - [%(name)s] - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),               # Logging on console
            logging.FileHandler("logs/latest.log") # Loggin on file, uncomment if needed for debug 
        ]
    )
logger = logging.getLogger(__name__)



def main():

    url = "https://tabs.ultimate-guitar.com/tab/rkomi/il-ritmo-delle-cose-chords-5669451"

    scraper = dataScraper()
    parser = dataParser()
    blob = scraper.fetch_by_url(url)

    soup = parser.blob_to_clean(blob)

    title_dict = scraper.get_song_info(scraper.req_url)
    title = parser.regex(title_dict["title"], "^", "-[0-9]")
    
    parser.save_to_file_as_text(title, soup)
    print(soup)
   
if __name__ == "__main__":
    main()