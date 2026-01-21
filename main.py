from scraper import Scraper
from parser import Parser


def main():
    url = "https://www.prospektmaschine.de/hypermarkte/"
    container_selector = "div.row.row-flex"

    # 1. Scraper stiahne stránku a vráti container
    scraper = Scraper(url, container_selector)
    container = scraper.get_container()

    # 2. Parser rozbije container na karty s udajmi
    parser = Parser()
    brochure_cards = parser.parse_container_to_cards(container)

    #3 Z každej karty vytiahne udaje
    if brochure_cards is None:
        print("Nenašli sa žiadne brožúry.")
        return
    
    for card in brochure_cards:
        title = parser.parse_title(card)
        thumbnail = parser.parse_thumbnail(card)

        detail_url = parser.parse_detail_url(card)
        shop_name = parser.parse_shop_name_from_url(detail_url)

        valid_from, valid_to = parser.parse_valid_dates_usa(card)
        
if __name__ == "__main__":
    main()





