import time
import logging
from datetime import datetime, timedelta
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from backend.products.scraper.base_scraper import BaseScraper
from selenium.webdriver.common.by import By
from backend.backend_f.config import SCRAPER_DELAY, WEEKLY_SCRAPER_DELAY

class AirfareScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)

    def scrape_makemytrip(self, from_location, to_location, date):
        """
        Scrape flight information from MakeMyTrip.

        Args:
            from_location (str): Departure airport or city.
            to_location (str): Arrival airport or city.
            date (str): Flight date in YYYY-MM-DD format.

        Returns:
            list: A list of dictionaries containing flight information.
        """
        try:
            date_makemytrip = datetime.strptime(date, '%Y-%m-%d').strftime('%d/%m/%Y')

            url = f"https://www.makemytrip.com/flight/search?itinerary={from_location}-{to_location}-{date_makemytrip}&tripType=O&paxType=A-1_C-0_I-0&intl=false&cabinClass=E&ccde=IN&lang=eng"
            self.get_page(url)

            self.driver.implicitly_wait(10)

            results = []

            flight_items = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'listingCard')]")
            for item in flight_items:
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

            return results

        except TimeoutException:
            self.logger.error("Timeout waiting for elements to load on MakeMyTrip")
        except NoSuchElementException as e:
            self.logger.error(f"Element not found: {e}")
        except Exception as e:
            self.logger.error(f"Unexpected error during scraping: {e}")

        return []

    def scrape_ixigo(self, from_location, to_location, date):
        """
        Scrape flight information from ixigo.

        Args:
            from_location (str): Departure airport or city.
            to_location (str): Arrival airport or city.
            date (str): Flight date in YYYYMMDD format.

        Returns:
            list: A list of dictionaries containing flight information.
        """
        try:
            date_ixigo = datetime.strptime(date, '%Y-%m-%d').strftime('%d%m%Y')

            url = f"https://www.ixigo.com/search/result/flight?from={from_location}&to={to_location}&date={date_ixigo}&adults=1&children=0&infants=0&class=e&source=Search%20Form&hbs=true"
            self.get_page(url)

            self.driver.implicitly_wait(10)

            results = []

            flight_items = self.driver.find_elements(By.XPATH,
                                                     "//div[contains(@class, 'flightCard') or contains(@class, 'flight-listing')]")
            for item in flight_items:
                try:
                    airline = item.find_element(By.XPATH, ".//div[contains(@class, 'airlineName')]").text
                    price = item.find_element(By.XPATH, ".//span[contains(@class, 'price')]").text
                    departure_time = item.find_element(By.XPATH, ".//div[contains(@class, 'departure-time')]").text
                    results.append({
                        "airline": airline,
                        "price": price,
                        "departure_time": departure_time
                    })
                except NoSuchElementException:
                    continue

            return results

        except TimeoutException:
            self.logger.error("Timeout waiting for elements to load on ixigo")
        except NoSuchElementException as e:
            self.logger.error(f"Element not found: {e}")
        except Exception as e:
            self.logger.error(f"Unexpected error during scraping: {e}")

        return []

    def scrape_cleartrip(self, from_location, to_location, date):
        """
        Scrape flight information from Cleartrip.

        Args:
            from_location (str): Departure airport or city.
            to_location (str): Arrival airport or city.
            date (str): Flight date in YYYY-MM-DD format.

        Returns:
            list: A list of dictionaries containing flight information.
        """
        try:
            date_cleartrip = datetime.strptime(date, '%Y-%m-%d').strftime('%d/%m/%Y')

            url = f"https://www.cleartrip.com/flights/results?adults=1&childs=0&infants=0&class=Economy&depart_date={date_cleartrip}&from={from_location}&to={to_location}&intl=n&origin={from_location}&destination={to_location}"
            self.get_page(url)

            self.driver.implicitly_wait(10)

            results = []

            flight_items = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'listingCard')]")
            for item in flight_items:
                try:
                    airline = item.find_element(By.XPATH, ".//p[contains(@class, 'airlineName')]").text
                    price = item.find_element(By.XPATH, ".//p[contains(@class, 'blackText fontSize18')]").text
                    departure_time = item.find_element(By.XPATH, ".//p[contains(@class, 'appendBottom2 flightTimeInfo')]").text
                    results.append({
                        "airline": airline,
                        "price": price,
                        "departure_time": departure_time
                    })
                except NoSuchElementException:
                    continue

            return results

        except TimeoutException:
            self.logger.error("Timeout waiting for elements to load on Cleartrip")
        except NoSuchElementException as e:
            self.logger.error(f"Element not found: {e}")
        except Exception as e:
            self.logger.error(f"Unexpected error during scraping: {e}")

        return []

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


    def scrape_weekly_flights(self, from_location, to_location, start_date):
        results = {}
        date_format = "%Y-%m-%d"
        start_date = datetime.strptime(start_date, date_format)
        for i in range(7):
            date = (start_date + timedelta(days=i)).strftime(date_format)
            self.logger.info(f"Scraping flights for {date}")
            results[date] = {
                "scrape_ixigo": self.scrape_ixigo(from_location, to_location, date),
                "skyscanner": self.scrape_skyscanner(from_location, to_location, date),
                "makemytrip": self.scrape_makemytrip(from_location, to_location, date),
                "cleartrip":self.scrape_cleartrip(from_location, to_location, date)
            }
            time.sleep(WEEKLY_SCRAPER_DELAY)

        return results

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    scraper = AirfareScraper()
    from_location = "DEL"
    to_location = "BOM"
    start_date = "2024-07-15"

    weekly_results = scraper.scrape_weekly_flights(from_location, to_location, start_date)
    print(weekly_results)