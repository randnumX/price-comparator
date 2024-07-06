import time
import logging
from datetime import datetime, timedelta
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_scraper import BaseScraper
from selenium.webdriver.common.by import By
from config import SCRAPER_DELAY, WEEKLY_SCRAPER_DELAY

class AirfareScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)

    def scrape_google_flights(self, from_location, to_location, date):
        """
        Scrape flight information from Google Flights.

        Args:
            from_location (str): Departure airport code.
            to_location (str): Arrival airport code.
            date (str): Flight date in YYYY-MM-DD format.

        Returns:
            list: A list of dictionaries containing flight information.
        """
        base_url = "https://www.google.com/flights"
        url = f"{base_url}?f=0&hl=en#flt={from_location}.{to_location}.{date}*"
        self.get_page(url)

        results = []
        try:
            # Wait for the results to load
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@class, 'gws-flights-results__result-item')]")))

            items = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'gws-flights-results__result-item')]")
            for item in items:
                try:
                    flight_info = item.find_element(By.XPATH,
                                                    ".//div[contains(@class, 'gws-flights-results__leg')]").text
                    price = item.find_element(By.XPATH, ".//div[contains(@class, 'gws-flights-results__price')]").text
                    results.append({
                        "flight_info": flight_info,
                        "price": price
                    })
                except NoSuchElementException as e:
                    self.logger.warning(f"Element not found: {e}")
                except Exception as e:
                    self.logger.error(f"Unexpected error: {e}")

                time.sleep(0.5)  # Rate limiting

        except TimeoutException:
            self.logger.error("Timeout waiting for flight results to load")
        except Exception as e:
            self.logger.error(f"Unexpected error during scraping: {e}")

        return results

    def scrape_skyscanner(self, from_location, to_location, date):
        """
        Scrape flight information from Skyscanner.

        Args:
            from_location (str): Departure airport code.
            to_location (str): Arrival airport code.
            date (str): Flight date in YYYY-MM-DD format.

        Returns:
            list: A list of dictionaries containing flight information.
        """
        url = f"https://www.skyscanner.com/transport/flights/{from_location}/{to_location}/{date}/"
        self.get_page(url)

        results = []
        try:
            wait = WebDriverWait(self.driver, 10)
            wait.until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'FlightsResults_dayViewItem__')]")))

            items = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'FlightsResults_dayViewItem__')]")
            for item in items:
                try:
                    airline = item.find_element(By.XPATH,
                                                ".//div[contains(@class, 'LogoImage_container__')]").get_attribute(
                        "aria-label")
                    price = item.find_element(By.XPATH, ".//span[contains(@class, 'Price_mainPriceText__')]").text
                    departure_time = item.find_element(By.XPATH,
                                                       ".//span[contains(@class, 'LegInfo_routePartialTime__')]").text
                    results.append({
                        "airline": airline,
                        "price": price,
                        "departure_time": departure_time
                    })
                except NoSuchElementException:
                    continue

                time.sleep(SCRAPER_DELAY)

        except TimeoutException:
            self.logger.error("Timeout waiting for Skyscanner results to load")
        except Exception as e:
            self.logger.error(f"Unexpected error during Skyscanner scraping: {e}")

        return results

    def scrape_makemytrip(self, from_location, to_location, date):
        """
        Scrape flight information from MakeMyTrip (Indian site).

        Args:
            from_location (str): Departure airport code.
            to_location (str): Arrival airport code.
            date (str): Flight date in YYYY-MM-DD format.

        Returns:
            list: A list of dictionaries containing flight information.
        """
        url = f"https://www.makemytrip.com/flight/search?itinerary={from_location}-{to_location}-{date}"
        self.get_page(url)

        results = []
        try:
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'listingCard')]")))

            items = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'listingCard')]")
            for item in items:
                try:
                    airline = item.find_element(By.XPATH, ".//p[contains(@class, 'airlineName')]").text
                    price = item.find_element(By.XPATH, ".//p[contains(@class, 'blackText fontSize18')]").text
                    departure_time = item.find_element(By.XPATH,
                                                       ".//p[contains(@class, 'appendBottom2 flightTimeInfo')]").text
                    results.append({
                        "airline": airline,
                        "price": price,
                        "departure_time": departure_time
                    })
                except NoSuchElementException:
                    continue

                time.sleep(SCRAPER_DELAY)

        except TimeoutException:
            self.logger.error("Timeout waiting for MakeMyTrip results to load")
        except Exception as e:
            self.logger.error(f"Unexpected error during MakeMyTrip scraping: {e}")

        return results

    def scrape_weekly_flights(self, from_location, to_location, start_date):
        # Implementation remains the same as in the previous response, but you can add the new scrapers here
        # For example:
        results = {}
        date_format = "%Y-%m-%d"
        start_date = datetime.strptime(start_date, date_format)
        for i in range(7):
            date = (start_date + timedelta(days=i)).strftime(date_format)
            self.logger.info(f"Scraping flights for {date}")
            results[date] = {
                "google_flights": self.scrape_google_flights(from_location, to_location, date),
                "skyscanner": self.scrape_skyscanner(from_location, to_location, date),
                "makemytrip": self.scrape_makemytrip(from_location, to_location, date)
            }
            time.sleep(WEEKLY_SCRAPER_DELAY)

        return results