# 🛒 OLX Parser

English | [Русский](https://github.com/ptmasher/olx-parser/blob/main/README-ru.md) | [Українська](https://github.com/ptmasher/olx-parser/blob/main/README-ua.md)

A Python-based parser for OLX listings using BeautifulSoup.
It allows you to search for products, extract detailed item information, and calculate the average price from the main listing page.

## 📦 Installation

- Clone the repository:
```bash
git clone https://github.com/ptmasher/olx-parser.git
```

- Install dependencies
```bash
pip install -r requirements.txt
```

## 📚 Dependencies

- Python 3.6 or higher
- lxml
- beautifulsoup4
- requests

## 🖥️ Usage

### Simple run
```python
python main.py
```

### Functions

- Parse OLX page using 'get_page()' function
```python
soup = get_page("PlayStation 5", country="BG", currency="BGN", condition="Used")
```

- Parse items from the page and save information using 'parse_items()'
```python
parse_items(soup)
```

- Calculate average price of all items on the page using 'average_price()'
```python
average_price(soup)
```

### Example usage from code
```python
Parse the page and save information using 'parse_items()'

soup = get_page("Iphone 15", country="UA", currency="USD", condition="used")

parse_items(soup)
avg = average_price(soup)
print(f"Average price: {avg} UAH")
```

## ⚙️ Configuration
Settings are located in config.py:

- `countryDomain` — supported countries (`UA`, `PL`, etc.)
- `currencyDict` - available currencies (`USD`, `PLN`, etc.)
- `conditionDict` - item condition filters (`all`, `new`, `used`)
- CSS class constants for parsing: `NAME_CLASS`, `PRICE_CLASS`, etc.

## 📌 Notes
Works with current OLX website structure.

## 🤝 Contributing

Pull requests are welcome!

If you encounter any issues or bugs, feel free to [open an issue](https://github.com/ptmasher/olx-parser/issues) or contact me directly.

Thanks for contributing!

## 📝 License

This project is licensed under the MIT License