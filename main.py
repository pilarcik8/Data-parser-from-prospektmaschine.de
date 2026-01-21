import json

from scraper import Scraper
from parser import Parser
from datetime import datetime
from cataloge import Cataloge

def main():
    BASE_URL = "https://www.prospektmaschine.de/"

    # 1. Dostaneme linky z navbaru
    scraper = Scraper()

    soup = scraper.get_soup(BASE_URL)
    parser = Parser(BASE_URL)
    category_urls = parser.parse_navbar_has_child_hrefs(soup)

    catalogs = []
    for url in category_urls:
        if url == "https://www.prospektmaschine.de/produktliste/" or url == "https://www.prospektmaschine.de/liste-der-stadte/" or url == "https://www.prospektmaschine.de/blog/":
            continue

        # 2. Stranku rozbijeme na karty s udajmi
        soup = scraper.get_soup(url)
        container = parser.parse_container(soup)
        brochure_cards = parser.parse_container_to_cards(container)

        #3 Z každej karty vytiahne udaje a uloží
        for card in brochure_cards:
            title = parser.parse_title(card)
            thumbnail = parser.parse_thumbnail(card)

            detail_url = parser.parse_detail_url(card)
            shop_name = parser.parse_shop_name_from_url(detail_url)
            valid_from, valid_to = parser.parse_valid_dates_usa(card)
            parsed_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            catalog = Cataloge(
                title_param=title,
                thumbnail_param=thumbnail,
                shop_name_param=shop_name,
                valid_from_param=valid_from,
                valid_to_param=valid_to,
                parsed_time_param=parsed_time
            )
            catalogs.append(catalog)

    #4 Uložíme do JSON súboru
    data_for_json = [c.to_dict() for c in catalogs]

    with open("catalogs.json", "w", encoding="utf-8") as f:
        json.dump(data_for_json, f, ensure_ascii=False, indent=4)

    print("Uložené do catalogs.json")

if __name__ == "__main__":
    main()





