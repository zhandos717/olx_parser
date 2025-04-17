import time
from pkg.parser import get_all_pages, _parse_links, _parse_item_page
from pkg.utils import _json_save, _get_prices


def main():
    print("\n📦 Добро пожаловать в OLX Parser!")
    query = input("🔍 Введите поисковый запрос: ").strip()
    if not query:
        print("❌ Запрос не может быть пустым.")
        return

    start_time = time.time()

    # Загружаем все страницы
    pages = get_all_pages(query=query, country='KZ', currency='KZT', city='astana', condition='all')
    print(f"\n📄 Загружено страниц: {len(pages)}")

    # Собираем все ссылки с объявлений
    all_links = []
    for soup in pages:
        all_links.extend(_parse_links(soup))
    print(f"🔗 Найдено всего объявлений: {len(all_links)}")

    # Парсим каждое объявление
    print("\n⏳ Начинаем обработку объявлений...")
    all_data = []
    for link in all_links:
        item = _parse_item_page(link)
        if item:
            all_data.append(item)

    # Сохраняем в файл
    _json_save(all_data)

    # Средняя цена
    prices = _get_prices(pages[0]) if pages else []
    avg_price = int(sum(prices) / len(prices)) if prices else 0
    print(f"\n💰 Средняя цена (по первой странице): {avg_price} ₸")

    # Статистика
    elapsed = time.time() - start_time
    print(f"\n✅ Обработка завершена за {elapsed:.2f} сек.")
    print(f"📁 Данные сохранены в data/data.json\n")


if __name__ == "__main__":
    main()
