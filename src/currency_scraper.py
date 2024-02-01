import csv
import logging
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter, Retry


class CurrencyScraper:
    def __init__(self, base_url, csv_filename="results.csv"):
        self.base_url = base_url
        self.csv_filename = csv_filename
        self.session = self.create_session()

    def create_session(
        self, retries=3, backoff_factor=0.3, status_forcelist=(500, 502, 504)
    ):
        """Create a requests session with retries."""
        session = requests.Session()
        retry = Retry(
            total=retries,
            read=retries,
            connect=retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_forcelist,
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    def write_csv_file(self, data):
        """Write the list of dictionaries into a csv file."""
        if data:
            # Declare fieldnames list instead of the keys of the first dictionary:
            #   - for setting the columns order
            #   - in case the keys of the first dictionary does not contains all the fields
            fieldnames = [
                "currency",
                "code",
                "symbol",
                "coins",
                "bank_notes",
                "central_bank",
                "central_bank_url",
                "users",
            ]
            with open(self.csv_filename, "w") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            logging.info(f"CSV file '{self.csv_filename}' created successfully.")
        else:
            logging.info("No data to write to CSV.")

    def get_row_from_th_text(self, currency_details_table, th_text):
        """Return the tr tag that matches a text in th."""
        try:
            row_header = currency_details_table.find("th", string=th_text)
            return row_header.parent if row_header else None
        except Exception as e:
            logging.error(f"Error finding row for text '{th_text}': {e}")
            return None

    def extract_data_from_row_with_th_text(
        self, table, th_text, tag="td", post_process=None
    ):
        """Extract data from a table row based on the provided th_text."""
        row = self.get_row_from_th_text(table, th_text)
        if row:
            text = row.select_one(tag).text.strip()
            if post_process:
                return post_process(text)
            return text
        return None

    def parse_currency_details_page(self, url):
        """
        Parse a currency page.
        Example: https://www.xe.com/currency/all-albanian-lek/
        """
        try:
            logging.info(f"Requesting {url}.")
            response = self.session.get(url)
            response.raise_for_status()

            # Dictionary to store the parsed data
            currency_page_data = {}

            logging.info(f"Parsing {url}.")
            soup = BeautifulSoup(response.text, "html.parser")

            currency_details_tables = soup.select(
                "table.currency__InfoTable-sc-4472af-2"
            )

            post_process_coins_and_bank_notes = lambda text: text.replace(
                "Freq used: ", ""
            ).replace("Rarely used: ", ", ")

            # Define a mapping of th text to data keys, tags and optional post-processing
            label_key_map = {
                "Name": ("currency", "td", None),
                "Coins": ("coins", "td", post_process_coins_and_bank_notes),
                "Bank notes": ("bank_notes", "td", post_process_coins_and_bank_notes),
                "Central bank": ("central_bank", "td", None),
                "Users": ("users", "span", None),
            }

            for label, (key, tag, post_process) in label_key_map.items():
                # Use the first table for "Name", second table for the rest
                table_index = 0 if label == "Name" else 1
                value = self.extract_data_from_row_with_th_text(
                    currency_details_tables[table_index], label, tag, post_process
                )
                if value:
                    if label == "Central bank":
                        # Special handling for central bank to extract URL
                        central_bank_row = self.get_row_from_th_text(
                            currency_details_tables[table_index], label
                        )
                        currency_page_data[
                            "central_bank_url"
                        ] = central_bank_row.select_one("a", href=True)["href"]
                    currency_page_data[key] = value

            return currency_page_data
        except requests.HTTPError as e:
            logging.error(f"HTTP error: {e}")
        except Exception as e:
            logging.error(f"Error during scraping: {e}")
        return {}

    def parse_currency_basic_infos(self, currency_list_item):
        """Return basic infos for a currency"""
        return {
            "code": currency_list_item.select_one("div:nth-of-type(3)").text,
            "symbol": currency_list_item.select_one("div:nth-of-type(4)").text,
        }

    def scrape(self):
        """Scrape the base_url"""
        try:
            logging.info(f"Requesting {self.base_url}.")
            response = self.session.get(self.base_url)
            response.raise_for_status()

            # List of dicts to write to the csv
            currencies_data = []

            logging.info(f"Parsing {self.base_url}.")
            soup = BeautifulSoup(response.text, "html.parser")

            currency_list_ul = soup.select_one(
                "section.Container__Content-sc-1skoo0z-1 > ul"
            )

            # Skipping header row
            for currency_list_item in currency_list_ul.select("li")[1:]:
                currency_data = self.parse_currency_basic_infos(currency_list_item)
                currency_url = urljoin(
                    self.base_url, currency_list_item.select_one("a")["href"]
                )
                currency_page_data = self.parse_currency_details_page(currency_url)
                currency_data.update(currency_page_data)
                currencies_data.append(currency_data)

            self.write_csv_file(currencies_data)
        except requests.HTTPError as e:
            logging.error(f"HTTP error: {e}")
        except Exception as e:
            logging.error(f"Error during scraping: {e}")
