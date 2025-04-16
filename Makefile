# Путь к виртуальному окружению
VENV = .venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

# Запустить проект
run:
	$(PYTHON) -m olx_parser.main

# Установить зависимости из requirements.txt
install:
	$(PIP) install -r requirements.txt

# Создать виртуальное окружение
venv:
	python3 -m venv $(VENV)

# Удалить виртуальное окружение
clean:
	rm -rf $(VENV)

# Установить всё с нуля
setup: venv install
