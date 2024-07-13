import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class BaseScraper:
    def __init__(self):
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chrome_options)

    def get_page(self, url):
        self.driver.get(url)

    def close(self):
        self.driver.quit()

    def save_results(self, results, filename):
        """
        Save the scraped results to a JSON file.

        Args:
            results (list or dict): The scraped data to save.
            filename (str): The name of the file to save the results to.
        """
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)