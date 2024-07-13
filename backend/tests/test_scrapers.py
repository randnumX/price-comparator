import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import pytest
from datetime import datetime, timedelta
from backend.products.scraper.shopping_scrapper import ShoppingScraper
from backend.products.scraper.airfare_scraper import AirfareScraper

@pytest.fixture
def shopping_scraper():
    scraper = ShoppingScraper()
    yield scraper
    scraper.close()

@pytest.fixture
def airfare_scraper():
    scraper = AirfareScraper()
    yield scraper
    scraper.close()

class TestRandomTests:
    def test_one_is_equal_to_one(self):
        assert "ONe"=="ONe"
class TestShoppingScraper:
    @pytest.mark.parametrize("search_query", ["laptop", "smartphone"])
    def test_scrape_flipkart(self, shopping_scraper, search_query):
        results = shopping_scraper.scrape_flipkart(search_query)
        assert isinstance(results, list)
        assert len(results) > 0
        for item in results:
            assert "name" in item
            assert "price" in item
            assert "url" in item

    @pytest.mark.parametrize("search_query", ["laptop", "smartphone"])
    def test_scrape_ebay(self, shopping_scraper, search_query):
        results = shopping_scraper.scrape_ebay(search_query)
        assert isinstance(results, list)
        assert len(results) > 0
        for item in results:
            assert "name" in item
            assert "price" in item
            assert "url" in item

    @pytest.mark.parametrize("search_query", ["shirt", "shoes"])
    def test_scrape_myntra(self, shopping_scraper, search_query):
        results = shopping_scraper.scrape_myntra(search_query)
        assert isinstance(results, list)
        assert len(results) > 0
        for item in results:
            assert "name" in item
            assert "price" in item
            assert "url" in item

class TestAirfareScraper:
    @pytest.mark.parametrize("from_location, to_location", [("SFO", "LAX"), ("DEL", "BOM")])
    def test_scrape_google_flights(self, airfare_scraper, from_location, to_location):
        date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        results = airfare_scraper.scrape_google_flights(from_location, to_location, date)
        assert isinstance(results, list)
        assert len(results) > 0
        for item in results:
            assert "flight_info" in item
            assert "price" in item

    @pytest.mark.parametrize("from_location, to_location", [("SFO", "LAX"), ("DEL", "BOM")])
    def test_scrape_skyscanner(self, airfare_scraper, from_location, to_location):
        date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        results = airfare_scraper.scrape_skyscanner(from_location, to_location, date)
        assert isinstance(results, list)
        assert len(results) > 0
        for item in results:
            assert "airline" in item
            assert "price" in item
            assert "departure_time" in item

    @pytest.mark.parametrize("from_location, to_location", [("DEL", "BOM"), ("BLR", "CCU")])
    def test_scrape_makemytrip(self, airfare_scraper, from_location, to_location):
        date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        results = airfare_scraper.scrape_makemytrip(from_location, to_location, date)
        assert isinstance(results, list)
        assert len(results) > 0
        for item in results:
            assert "airline" in item
            assert "price" in item
            assert "departure_time" in item

    @pytest.mark.parametrize("from_location, to_location", [("SFO", "LAX"), ("DEL", "BOM")])
    def test_scrape_weekly_flights(self, airfare_scraper, from_location, to_location):
        start_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        results = airfare_scraper.scrape_weekly_flights(from_location, to_location, start_date)
        assert isinstance(results, dict)
        assert len(results) == 7
        for date, flights in results.items():
            assert isinstance(flights, dict)
            assert "google_flights" in flights
            assert "skyscanner" in flights
            assert "makemytrip" in flights
            for source, flight_list in flights.items():
                assert isinstance(flight_list, list)
                assert len(flight_list) > 0