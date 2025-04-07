import re
import json
import requests
from bs4 import BeautifulSoup
from .config import headers, MAIN_PAGE_PRICES_CLASS


def _fetch_url(url) -> BeautifulSoup | None:
        # parse the link
    try: 
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching page: {e}")
        return None

    return BeautifulSoup(response.text, 'lxml')


def _get_prices(soup) -> list[int]:
    
    price_list = []
    prices = soup.find_all("p", class_=MAIN_PAGE_PRICES_CLASS)
    for price in prices:
        # separates numbers with price from everything else
        cleaned_price = re.sub(r"[^\d\s]", "", price.text).replace(" ", "")
        match = re.match(r"(\d+)", cleaned_price)
        if match:
            price_list.append(int(match.group(1)))

    return price_list


def _json_save(data: list[dict[str, str]]) -> None:
    with open("data.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)