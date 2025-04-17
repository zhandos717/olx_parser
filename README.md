# 🛍️ OLX Parser

Парсер объявлений с сайта [OLX.kz](https://olx.kz), написанный на Python.  
Позволяет искать объявления по ключевому слову, собирать данные о товаре и продавце, сохранять всё в JSON.

---

## 🚀 Возможности

- 🔍 Поиск объявлений по запросу
- 📥 Сбор информации:
  - Название товара
  - Цена
  - Состояние
  - Имя продавца
  - Ссылка на продавца
  - Ссылка на объявление
- 📊 Подсчёт средней цены
- 💾 Сохранение в `data/data.json`
- 📈 Прогресс выполнения через `tqdm`

---

## 🛠 Установка и запуск

```bash
git clone git@github.com:zhandos717/olx_parser.git
cd olx-parser
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
make run
