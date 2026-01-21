from datetime import datetime

class Parser:

    def __init__(self, base_url_par):
        self.BASE_URL = base_url_par

    def parse_navbar_has_child_hrefs(self, soup):
        urls = []

        nav_ul = soup.select_one("ul.list-unstyled.navbar-nav")
        if not nav_ul:
            return urls

        for li in nav_ul.select("li.has_child"):
            a = li.select_one("a[href]")

            # nenastáva ale kvôli bezpečnosti
            if not a: 
                continue

            href = a.get("href")
            url = self.BASE_URL.rstrip("/") + "/" + href.lstrip("/")

            # tiež kvôli bezpečnosti
            if url:
                urls.append(url)

        return urls
    
    def parse_container(self, soup):
        return soup.select_one("div.row.row-flex")
    
    # Parser rozbije container na karty v ktorych najdeme udaje
    def parse_container_to_cards(self, container):
        return container.select(
            "div.brochure-thumb.col-xs-6.col-sm-3"
        )

    # link z ktoreho vieme zistit obchod
    def parse_detail_url(self, card):
        a = card.find("a", href=True)
        if not a:
            return None

        href = a.get("href")

        # len relatívna ceasta
        return self.BASE_URL.rstrip("/") + "/" + href.lstrip("/")

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
    
    # z karty vytiahne platnost v USA formáte MM/DD/YYYY
    def parse_valid_dates_usa(self, card):
        small = card.find("small", class_="hidden-sm")
        if not small:
            return None, None

        # Očakáva sa formát "DD.MM.YYYY - DD.MM.YYYY" napr. von Mittwoch 21.01.2026 (od stredy 21.01.2026) zapisane nebudu
        text = small.get_text(strip=True) 
        if "-" not in text:
            return None, None
        start_str, end_str = [x.strip() for x in text.split("-", 1)]

        return self.eu_to_usa_date_format(start_str), self.eu_to_usa_date_format(end_str)
    
    # z URL vytiahne názov obchodu
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

