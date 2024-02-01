import argparse
import logging

from currency_scraper import CurrencyScraper


def main():
    """Entry point of the script"""
    parser = argparse.ArgumentParser(
        description="Scrape currencies from https://www.xe.com/ and writes a CSV file."
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="scraped_currencies.csv",
        help="CSV file name",
    )
    parser.add_argument(
        "-l", "--log", type=str, default="main.log", help="LOG file name"
    )
    args = parser.parse_args()

    logging.basicConfig(
        filename=args.log,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    scraper = CurrencyScraper("https://www.xe.com/symbols/", csv_filename=args.output)
    scraper.scrape()


if __name__ == "__main__":
    main()
