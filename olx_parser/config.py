# config.py

NAME_CLASS = "css-10ofhqw"
MAIN_PAGE_PRICES_CLASS = "css-uj7mm0"
PRICE_CLASS = "css-fqcbii"
CONDITION_CLASS = "css-z0m36u"
SELLER_CLASS = "css-fka1fu"
domain = None

# UA set as default
countryDomain = {
    "BG": ".bg",
    "PL": ".pl",
    "PT": ".pt",
    "RO": ".ro",
    "KZ": ".kz",
    "UA": ".ua",
    "UZ": ".uz"
}

# USD set as default
currencyDict = {
    "UAH" : "?currency=UAH",
    "USD" : "?currency=USD",
    "EUR" : "?currency=EUR",
    "BGN" : "?currency=BGN",
    "PLN" : "?currency=PLN",
    "EUR" : "?currency=EUR",
    "RON" : "?currency=RON",
    "KZT" : "?currency=KZT",
    "UZS" : "?currency=UZS"
}

# ALL set as default
conditionDict = {
    "all" : "",
    "new" : "?search[filter_enum_state][0]=new",
    "used" : "?search[filter_enum_state][0]=used"
}

# headers for request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}




def help():
    print("Available country domains:")
    print(', '.join(countryDomain))

    print("\nAvailable item conditions:")
    print(', '.join(conditionDict.keys()))

    print("\nAvailable currencies:")
    print(', '.join(currencyDict.keys()))

def main() -> None:
    print(help())

if __name__ == "__main__":
    main()