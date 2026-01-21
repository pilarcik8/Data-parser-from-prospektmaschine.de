import requests
from bs4 import BeautifulSoup


class Scraper:
     def get_soup(self, url: str):
        page = requests.get(url)
        page.raise_for_status()
        return BeautifulSoup(page.content, "html.parser")
