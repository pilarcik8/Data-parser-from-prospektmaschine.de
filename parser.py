from datetime import datetime
from email.mime import text

class Parser:
    BASE_URL = "https://www.prospektmaschine.de"

    # Parser rozbije container na karty s udajmi
    def parse_container_to_cards(self, container):
        return container.select(
            "div.brochure-thumb.col-xs-6.col-sm-3"
        )

    def parse_detail_url(self, card):
        a = card.find("a", href=True)
        if not a:
            return None

        href = a.get("href")

        # len relatívna
        return self.BASE_URL.rstrip("/") + "/" + href.lstrip("/")
    
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

        # 2) lazy-load  
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
    
    def parse_shop_name_from_url(self, detail_url: str):
        if not detail_url:
            return None

        # odstránime domény
        url = detail_url
        if url.startswith(self.BASE_URL):
            url = url[len(self.BASE_URL):]

        parts = url.strip("/").split("/")
        if not parts or not parts[0]:
            return None

        slug = parts[0]

        name = slug.replace("-", " ")

        # každé slovo s veľkým prvým písmenom
        name = " ".join(word.capitalize() for word in name.split())

        return name

    # Pomocná funkcia na konverziu dátumu z EU formátu na USA formát
    def eu_to_usa_date_format(self, date_str: str) -> str:
        dt = datetime.strptime(date_str.strip(), "%d.%m.%Y")
        return dt.strftime("%m/%d/%Y")

