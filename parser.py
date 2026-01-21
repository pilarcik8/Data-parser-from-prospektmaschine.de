from datetime import datetime
from email.mime import text

class Parser:
    # Parser rozbije container na karty s udajmi
    def parse_container_to_cards(self, container):
        return container.select(
            "div.brochure-thumb.col-xs-6.col-sm-3"
        )
    
    # Z každej karty vytiahne udaje
    def parse_id(self, card):
        return card.get("data-brochure-id")

    def parse_title(self, card):
        strong = card.find("strong")
        return strong.text.strip() if strong else None
    
    def parse_thumbnail(self, card):
        img = card.find("img")
        if not img:
            return None

        # 1) klasický src
        src = img.get("src")
        if src:
            return src

        # 2) lazy-load varianty 
        for attr in ("data-src", "data-original", "data-lazy-src", "data-img", "data-url"):
            val = img.get(attr)
            if val:
                return val

        return None
    
    def parse_valid_dates_usa(self, card):
        small = card.find("small", class_="hidden-sm")
        if not small:
            return None, None

        text = small.get_text(strip=True) # Očakáva sa formát "DD.MM.YYYY - DD.MM.YYYY"
        start_str, end_str = [x.strip() for x in text.split("-", 1)]

        return self.eu_to_usa_date_format(start_str), self.eu_to_usa_date_format(end_str)

    # Pomocná funkcia na konverziu dátumu z EU formátu na USA formát
    def eu_to_usa_date_format(self, date_str: str) -> str:
        dt = datetime.strptime(date_str.strip(), "%d.%m.%Y")
        return dt.strftime("%m/%d/%Y")

