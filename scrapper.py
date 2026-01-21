import requests
from bs4 import BeautifulSoup

URL = "https://www.prospektmaschine.de/hypermarkte/"

def get_container():
    page = requests.get(URL)
    page.raise_for_status()

    soup = BeautifulSoup(page.content, "html.parser")
    container = soup.select_one("div.row.row-flex")

    if not container:
        raise ValueError("Container sa nenašiel")

    return container

# docasne
if __name__ == "__main__":
    # len na rýchly debug
    c = get_container()
    print(c.prettify())
