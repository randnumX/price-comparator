# backend/run_scrapers.py

import logging
from shopping_scrapper import ShoppingScraper
from airfare_scraper import AirfareScraper
from config import LOG_LEVEL, LOG_FORMAT


def setup_logging():
    logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)


def main():
    setup_logging()
    logger = logging.getLogger(__name__)

    # Run shopping scrapers
    shopping_scraper = ShoppingScraper()
    try:
        amazon_results = shopping_scraper.scrape_amazon("laptop")
        flipkart_results = shopping_scraper.scrape_flipkart("laptop")
        ebay_results = shopping_scraper.scrape_ebay("laptop")

        logger.info(f"Amazon results: {len(amazon_results)}")
        logger.info(f"Flipkart results: {len(flipkart_results)}")
        logger.info(f"eBay results: {len(ebay_results)}")
    finally:
        shopping_scraper.close()

    # Run airfare scraper
    airfare_scraper = AirfareScraper()
    try:
        weekly_flights = airfare_scraper.scrape_weekly_flights("SFO", "LAX", "2023-07-15")
        logger.info(f"Weekly flights scraped for 7 days")
    finally:
        airfare_scraper.close()


if __name__ == "__main__":
    main()