import logging
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from products.scraper.base_scraper import BaseScraper
from backend_f.config import SCRAPER_DELAY
from selenium.webdriver.common.by import By
import time

class ShoppingScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)

    def scrape_amazon(self, search_query):
        """
        Scrape product information from Amazon India including images.

        Args:
            search_query (str): The search term to look for on Amazon.

        Returns:
            list: A list of dictionaries containing product information.
                  Each dictionary includes 'name', 'price', 'url', 'image_url', and 'image_bytes'.
        """
        url = f"https://www.amazon.in/s?k={search_query}"
        self.get_page(url)

        results = []
        wait = WebDriverWait(self.driver, 10)
        time.sleep(SCRAPER_DELAY)  # Rate limiting
        wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@data-component-type, 's-search-result')]")))
        items = self.driver.find_elements(By.XPATH, "//div[contains(@data-component-type, 's-search-result')]")

        for item in items:
            time.sleep(SCRAPER_DELAY)  # Rate limiting
            try:
                name = item.find_element(By.XPATH, ".//h2/a/span").text
                price = int(item.find_element(By.XPATH, ".//span[@class='a-price']").text.replace('₹','').replace(',',''))
                link = item.find_element(By.XPATH, ".//h2/a").get_attribute("href")
                image_url = item.find_element(By.XPATH, ".//img").get_attribute("src")  # Fetch image src attribute

                results.append({
                    "name": name,
                    "price": price,
                    "url": link,
                    "image_url": image_url
                })
            except NoSuchElementException as e:
                self.logger.warning(f"Element not found: {e}")
            except Exception as e:
                self.logger.error(f"Unexpected error: {e}")
        return results

    def scrape_flipkart(self, search_query):
        """
        Scrape product information from Flipkart including images.

        Args:
            search_query (str): The search term to look for on Flipkart.

        Returns:
            list: A list of dictionaries containing product information.
                  Each dictionary includes 'name', 'price', 'url', 'image_url', and 'image_bytes'.
        """
        url = f"https://www.flipkart.com/search?q={search_query}"
        self.get_page(url)

        results = []
        try:
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.presence_of_element_located((By.XPATH, "//div[@data-id]")))
            time.sleep(SCRAPER_DELAY)  # Rate limiting
            items = self.driver.find_elements(By.XPATH, "//div[@data-id]")
            for item in items:
                time.sleep(SCRAPER_DELAY)  # Rate limiting
                try:
                    name_element = item.find_element(By.XPATH, ".//div/a[2]").get_attribute("title")

                    price_element = int(item.find_element(By.XPATH, ".//div/a[3]/div/div").text.replace(',','').replace('₹',''))

                    link_element = item.find_element(By.XPATH, ".//a")
                    link = link_element.get_attribute("href") if link_element else ""

                    image_element = item.find_element(By.XPATH, ".//img")
                    image_url = image_element.get_attribute("src") if image_element else ""

                    results.append({
                        "name": name_element,
                        "price": price_element,
                        "url": link,
                        "image_url": image_url
                    })
                except NoSuchElementException as e:
                    logging.warning(f"Element not found: {e}")
                    logging.info("Trying the second approach")
                    try:
                        name_element = item.find_element(By.XPATH, ".//div/a/div[2]/div/div[2]").text
                        price_element = int(item.find_element(By.XPATH, ".//div/a/div[2]/div[2]/div/div/div").text.replace(',','').replace('₹',''))
                    except Exception:
                        logging.info("Trying the third approach")
                        name_element = item.find_element(By.XPATH, ".//div/a/div[2]/div/div").text
                        price_element = int(item.find_element(By.XPATH, ".//div/a/div[2]/div/div/div/div").text.replace(',','').replace('₹',''))
                    link_element = item.find_element(By.XPATH, ".//a")
                    link = link_element.get_attribute("href") if link_element else ""

                    image_element = item.find_element(By.XPATH, ".//img")
                    image_url = image_element.get_attribute("src") if image_element else ""

                    results.append({
                        "name": name_element,
                        "price": price_element,
                        "url": link,
                        "image_url": image_url
                    })
                except Exception as e:
                    logging.error(f"Unexpected error: {e}")
        except TimeoutException:
            logging.error("Timeout waiting for Flipkart results to load")
        except Exception as e:
            logging.error(f"Unexpected error during Flipkart scraping: {e}")

        return results