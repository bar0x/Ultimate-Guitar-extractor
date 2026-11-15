import logging, argparse
# import re, sys, os #already imported!
from src import dataParser, dataScraper, setup_logging


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="ug-extract",
        description="Fetch your favourites UG Tabs in .txt files, or use it to make your custom songbook using LaTeX or Typst template!",
    )

    #URLs
    parser.add_argument("urls",nargs="+",help="One or more Tab URLs from UG to download",)
    # Optional args
    parser.add_argument("-o", "--output", default="./songs/", help="Output folder to store .txt files (default: ./songs/)",)
    parser.add_argument("-n", "--name", default=None, help="Custom filename for your song file (only works if you pass 1 URL at time)",)
    parser.add_argument("-v", "--verbose", action="store_true", help="Shows detailed logs (for debugging purpose)",)

    return parser.parse_args()

def main() -> None:
    #setting up arg parser and logs
    args = parse_args()
    setup_logging(verbose=args.verbose)
    logger = logging.getLogger(__name__)

    if args.name and len(args.urls) > 1:
        logger.warning("Ignoring --name flag (multiple URLs sent)")
        args.name = None

    scraper, parser = dataScraper(), dataParser()
    parser.save_file_path = str(args.output)

    for url in args.urls:
        try:
            logger.info(f"Started looking for: {url}")
            blob = scraper.fetch_by_url(url)
            clean_text = parser.blob_to_clean(blob)

            if args.name:
                title = args.name
            else:
                title_dict = scraper.get_song_info(scraper.req_url)
                title = parser.regex(title_dict["title"], "^", "-[0-9]") or "untitled_song"

            parser.save_to_file_as_text(title, clean_text)

        except Exception as e:
            logger.error(f"Error trying to elaborate URL {url}: {e}")
   
if __name__ == "__main__":
    main()