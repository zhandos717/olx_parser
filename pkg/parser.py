from urllib.parse import quote_plus

from bs4 import BeautifulSoup
from typing import List, Optional, Dict
from tqdm import tqdm
from pkg.utils import _fetch_url, _json_save, _get_prices
from pkg.config import *


def _parse_links(soup: BeautifulSoup) -> List[str]:
    items = soup.find_all("a", class_="css-1tqlkj0")
    return list({
        f"https://olx{domain}{item.get('href')}"
        for item in items if item.get("href")
    })


def _parse_item_page(link: str) -> Optional[Dict[str, str]]:
    soup = _fetch_url(link)
    if not soup:
        return None

    try:
        name_tag = soup.find("h4", attrs=NAME_CLASS)
        price_tag = soup.find("h3", attrs=PRICE_CLASS)
        description_tag = soup.find("div", attrs=CONDITION_CLASS)
        seller_link_tag = soup.find("a", attrs=SELLER_LINK_SELECTOR)
        seller_name_tag = seller_link_tag.find("h4", class_=SELLER_NAME_CLASS) if seller_link_tag else None

        # Проверяем, чего именно не хватает
        missing = []
        if not name_tag:
            missing.append("название")
        if not description_tag:
            missing.append("состояние")
        if not seller_link_tag:
            missing.append("продавец")

        if missing:
            print(f"⚠️ Не удалось извлечь {', '.join(missing)}: {link}")
            return None

        return {
            "name": name_tag.text.strip() if name_tag else "Нет названия",
            "price": price_tag.text.strip() if price_tag else "Нет цены",
            "description": description_tag.text.strip(),
            "seller_name": seller_name_tag.text.strip() if seller_name_tag else None,
            "seller_link": f"https://www.olx.kz{seller_link_tag['href']}" if seller_link_tag and seller_link_tag.has_attr(
                "href") else None,
            "link": link
        }

    except Exception as e:
        print(f"❌ Ошибка при разборе {link}: {e}")
        return None


def parse_items(soup: BeautifulSoup) -> None:
    if not soup:
        print("❌ Нет HTML для обработки.")
        return

    links = _parse_links(soup)
    print(f"🔗 Найдено ссылок: {len(links)}")

    all_data = []

    for link in tqdm(links, desc="📦 Парсинг товаров"):
        item = _parse_item_page(link)
        if item:
            all_data.append(item)
        else:
            print(f"⚠️ Пропущено: {link}")

    print(f"✅ Успешно обработано: {len(all_data)}")
    _json_save(all_data)


def average_price(soup: BeautifulSoup) -> int:
    if not soup:
        return 0

    price_list = _get_prices(soup)
    return int(sum(price_list) / len(price_list)) if price_list else 0


def get_page(query: str, country: str = 'KZ', currency: str = 'KZT', condition: str = 'all', city: str = 'astana') -> \
        Optional[
            BeautifulSoup]:
    from urllib.parse import quote_plus

    if not query:
        raise ValueError("The 'query' parameter is required and cannot be empty.")

    try:
        url = f"https://www.olx{countryDomain[country]}/list/{city}/q-{quote_plus(query)}/{currencyDict[currency]}{conditionDict[condition]}"
    except KeyError as e:
        print(f"Invalid value of {e}\nUse 'help' function to see available parameters")
        return None

    global domain
    domain = countryDomain[country]

    return _fetch_url(url)


def get_all_pages(query: str, country: str = 'KZ', currency: str = 'KZT',
                  condition: str = 'all', city: str = '') -> List[BeautifulSoup]:
    """
    Загружает все страницы OLX по заданному запросу.

    Parameters
    ----------
    query : str
        Ключевое слово (например: iphone).
    country : str
        Страна (по умолчанию: 'KZ').
    currency : str
        Валюта (по умолчанию: 'KZT').
    condition : str
        Состояние товара: 'all', 'used', 'new'
    city : str
        Название города (по желанию).

    Returns
    -------
    List[BeautifulSoup]
        Список HTML страниц.
    """

    pages = []
    page_number = 1
    global domain
    domain = countryDomain[country]

    while page_number <= 3:
        try:
            base_path = f"/list/{city}/" if city else "/list/"
            url = f"https://www.olx{domain}{base_path}q-{quote_plus(query)}/?page={page_number}{currencyDict[currency]}{conditionDict[condition]}"
            print(f"📄 Загружаем страницу {page_number} → {url}")

            soup = _fetch_url(url)
            if not soup:
                print("⚠️ Страница не загрузилась.")
                break

            items = soup.find_all("div", {"data-cy": "l-card"})
            if not items:
                print("🔚 Больше страниц нет.")
                break

            print(f"  ✅ Найдено {len(items)} объявлений на странице")
            pages.append(soup)
            page_number += 1

        except Exception as e:
            print(f"❌ Ошибка на странице {page_number}: {e}")
            break

    return pages
