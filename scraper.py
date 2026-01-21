import requests
from bs4 import BeautifulSoup


class Scraper:
    def __init__(self, url, container_selector=None):
        self.url = url
        self.container_selector = container_selector

    def get_container(self):
        page = requests.get(self.url)
        page.raise_for_status()

        soup = BeautifulSoup(page.content, "html.parser")
        container = soup.select_one(self.container_selector)

        if not container:
            raise ValueError("Container sa nenašiel")

        return container
