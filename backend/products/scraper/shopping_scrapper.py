import time
import logging
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_scraper import BaseScraper
from selenium.webdriver.common.by import By
from config import SCRAPER_DELAY

class ShoppingScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)

    def scrape_amazon(self, search_query):
        """
        Scrape product information from Amazon.

        Args:
            search_query (str): The search term to look for on Amazon.

        Returns:
            list: A list of dictionaries containing product information.
        """
        url = f"https://www.amazon.com/s?k={search_query}"
        self.get_page(url)

        results = []
        items = self.driver.find_elements(By.XPATH, "//div[contains(@class, 's-result-item')]")
        for item in items:
            try:
                name = item.find_element(By.XPATH, ".//h2//span").text
                price = item.find_element(By.XPATH, ".//span[@class='a-price-whole']").text
                link = item.find_element(By.XPATH, ".//h2/a").get_attribute("href")
                results.append({
                    "name": name,
                    "price": price,
                    "url": link
                })
            except NoSuchElementException as e:
                self.logger.warning(f"Element not found: {e}")
            except Exception as e:
                self.logger.error(f"Unexpected error: {e}")

            time.sleep(0.5)  # Rate limiting

        return results

    def scrape_flipkart(self, search_query):
        """
        Scrape product information from Flipkart.

        Args:
            search_query (str): The search term to look for on Flipkart.

        Returns:
            list: A list of dictionaries containing product information.
        """
        url = f"https://www.flipkart.com/search?q={search_query}"
        self.get_page(url)

        results = []
        try:
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, '_1AtVbE')]")))

            items = self.driver.find_elements(By.XPATH, "//div[contains(@class, '_1AtVbE')]")
            for item in items:
                try:
                    name = item.find_element(By.XPATH, ".//a[contains(@class, 's1Q9rs')]").text
                    price = item.find_element(By.XPATH, ".//div[contains(@class, '_30jeq3')]").text
                    link = item.find_element(By.XPATH, ".//a[contains(@class, 's1Q9rs')]").get_attribute("href")
                    results.append({
                        "name": name,
                        "price": price,
                        "url": link
                    })
                except NoSuchElementException:
                    continue

                time.sleep(SCRAPER_DELAY)

        except TimeoutException:
            self.logger.error("Timeout waiting for Flipkart results to load")
        except Exception as e:
            self.logger.error(f"Unexpected error during Flipkart scraping: {e}")

        return results

    def scrape_ebay(self, search_query):
        """
        Scrape product information from eBay.

        Args:
            search_query (str): The search term to look for on eBay.

        Returns:
            list: A list of dictionaries containing product information.
        """
        url = f"https://www.ebay.com/sch/i.html?_nkw={search_query}"
        self.get_page(url)

        results = []
        try:
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.presence_of_element_located((By.XPATH, "//li[contains(@class, 's-item')]")))

            items = self.driver.find_elements(By.XPATH, "//li[contains(@class, 's-item')]")
            for item in items:
                try:
                    name = item.find_element(By.XPATH, ".//h3[contains(@class, 's-item__title')]").text
                    price = item.find_element(By.XPATH, ".//span[contains(@class, 's-item__price')]").text
                    link = item.find_element(By.XPATH, ".//a[contains(@class, 's-item__link')]").get_attribute("href")
                    results.append({
                        "name": name,
                        "price": price,
                        "url": link
                    })
                except NoSuchElementException:
                    continue

                time.sleep(SCRAPER_DELAY)

        except TimeoutException:
            self.logger.error("Timeout waiting for eBay results to load")
        except Exception as e:
            self.logger.error(f"Unexpected error during eBay scraping: {e}")

        return results