import re
import json
import requests
from pathlib import Path
from typing import Optional, List, Dict
from bs4 import BeautifulSoup
from pkg.config import headers, MAIN_PAGE_PRICES_CLASS


def _fetch_url(url: str) -> Optional[BeautifulSoup]:
    """
    Загружает HTML-страницу по указанному URL и возвращает объект BeautifulSoup.
    """
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'lxml')
    except requests.RequestException as e:
        print(f"[Ошибка запроса] {url}: {e}")
        return None



def _get_prices(soup: BeautifulSoup) -> List[int]:
    """
    Извлекает список числовых цен с главной страницы объявлений.
    """
    prices = soup.find_all("p", class_=MAIN_PAGE_PRICES_CLASS)
    price_list = []

    for price_tag in prices:
        cleaned = re.sub(r"[^\d\s]", "", price_tag.text).replace(" ", "")
        match = re.match(r"(\d+)", cleaned)
        if match:
            price_list.append(int(match.group(1)))

    return price_list


def _json_save(data: List[Dict[str, str]], filename: str = "data.json") -> None:
    """
    Сохраняет данные в JSON-файл в папке `data/`.

    Parameters
    ----------
    data : List[Dict[str, str]]
        Данные для сохранения.
    filename : str
        Имя файла (по умолчанию: 'data.json').
    """
    output_dir = Path("data")
    output_dir.mkdir(parents=True, exist_ok=True)

    file_path = output_dir / filename

    try:
        with file_path.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        print(f"📁 Данные успешно сохранены в {file_path.resolve()}")
    except IOError as e:
        print(f"❌ Ошибка при сохранении файла: {e}")
