# Currencies Scraping Script

## Description

This repository contains a python script that scrape some currencies data from the website [xe.com](https://www.xe.com/).

## Features

The scraped data for each currencies are:
- Currency Name
- ISO Code
- Symbol
- Commonly Used Coins
- Commonly Used Banknotes
- Central Bank Name
- Central Bank Website
- Primary Users of the Currency

**Data Storage:** Organizes and stores the scraped data in a structured CSV file, facilitating easy access and analysis.

The file [scraped_currencies.csv](./scraped_currencies.csv) is an example of a generated CSV file.

**Logging:** Implements logging to track the script's operation and any issues encountered during the scraping process.

## Installation

To run this script, you need Python 3.x and the following packages:
- [requests](https://pypi.org/project/requests/): For making HTTP requests to the website.
- [BeautifulSoup](https://pypi.org/project/beautifulsoup4/): For parsing the HTML content and extracting data.

Install the required packages using `pip` and the provided `requirements.txt` file:
```sh
pip install -r requirements.txt
```
A python [virtualenv](https://docs.python.org/3/library/venv.html) may be used to install the dependencies.

## Usage
```sh
usage: main.py [-h] [-o OUTPUT] [-l LOG]

Scrape currencies from https://www.xe.com/ and writes a CSV file.

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        CSV file name
  -l LOG, --log LOG     LOG file name
```
## Contributing
Contributions to enhance the script or fix issues are welcome. Please feel free to fork the repository, make your changes, and submit a pull request.

## Ethical Considerations
Please ensure that your use of this script complies with XE.com's Terms of Service and respects the website's robots.txt file. Avoid making excessive requests that could impact the website's performance.

## License
This project is Open Source and is available under the [Apache License 2.0](./LICENSE).

## Disclaimer
This script is provided for educational purposes only. The author is not responsible for any misuse or damage resulting from the use of this script.