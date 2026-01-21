from scrapper import Scrapper
from parser import Parser


def main():
    url = "https://www.prospektmaschine.de/hypermarkte/"
    container_selector = "div.row.row-flex"

    # 1. Scraper stiahne stránku a vráti container
    scrapper = Scrapper(url, container_selector)
    container = scrapper.get_container()

    # 2. Parser rozbije container na karty s udajmi
    parser = Parser()
    brochure_cards = parser.parse_container_to_cards(container)

    #3 Z každej karty vytiahne udaje
    if brochure_cards is None:
        print("Nenašli sa žiadne brožúry.")
        return
    
    for card in brochure_cards:
        id = parser.parse_id(card)
        title = parser.parse_title(card)
        thumbnail = parser.parse_thumbnail(card)
        valid_from, valid_to = parser.parse_valid_dates_usa(card)

        print(f"ID: {id}")
        print(f"Title: {title}")
        print(f"Thumbnail: {thumbnail}")
        print(f"Valid From: {valid_from}")
        print(f"Valid To: {valid_to}")
        print("-" * 40)
        
if __name__ == "__main__":
    main()





