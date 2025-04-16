import time
from olx_parser.parser import get_page, parse_items, average_price, _parse_links
from olx_parser.utils import _fetch_url

if __name__ == "__main__":
    query = input("Enter search query: ")
    start_time = time.time()

    soup = get_page(query)

    if not soup:
        print("Не удалось загрузить страницу.")
        exit(1)

    links = _parse_links(soup)
    print(f"🔗 Найдено {len(links)} объявлений по запросу '{query}'")

    print("⏳ Загружаем данные по каждому объявлению...")
    parse_items(soup)

    avg = average_price(soup)
    print(f"💰 Средняя цена: {avg} USD")

    elapsed = time.time() - start_time
    print(f"✅ Готово! Обработка заняла {elapsed:.2f} сек.")
