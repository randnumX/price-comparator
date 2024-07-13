import logging
from shopping_scrapper import ShoppingScraper
from airfare_scraper import AirfareScraper
from backend.backend_f.config import LOG_LEVEL, LOG_FORMAT,LOG_FILE


def setup_logging():
    logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT, filename=LOG_FILE)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(LOG_LEVEL)
    console_formatter = logging.Formatter(LOG_FORMAT)
    console_handler.setFormatter(console_formatter)

    logging.getLogger().addHandler(console_handler)


def main():
    setup_logging()
    logger = logging.getLogger(__name__)

    shopping_scraper = ShoppingScraper()
    try:
        flipkart_results = shopping_scraper.scrape_flipkart("Laptop")

        logger.info(f"Flipkart results: {(flipkart_results)}")
    finally:
        shopping_scraper.close()

    airfare_scraper = AirfareScraper()
    try:
        weekly_flights = airfare_scraper.scrape_weekly_flights("SFO", "LAX", "2023-07-15")
        logger.info(f"Weekly flights scraped for 7 days")
    finally:
        airfare_scraper.close()


if __name__ == "__main__":
    main()