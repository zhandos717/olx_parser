from bs4 import BeautifulSoup
from .utils import _fetch_url, _json_save, _get_prices
from .config import *



# gets every link on the website
def _parse_links(soup) -> list:

    links = set() # is set to avoid duplicates
    items = soup.find_all("a", class_="css-1tqlkj0")

    # building url and adding to links set
    for item in items:
        href = item.get("href")
        if href:
            links.add(f"https://olx{domain}{href}")
        
    return list(links)

def parse_items(soup) -> None:
    '''
    
    Parses item data from the OLX page and saves the extracted info as JSON.

    This function extracts all item links from the main page,
    fetches each item's detailed page, parses specific data fields
    (name, price, condition, seller, link), and saves the collected
    data into a JSON file.

    Parameters
    ----------
    soup: BeautifulSoup
        Parsed HTML of the OLX listing page.

    Returns
    -------
    None
        This function does not return anyting. Results are saved
        using the `json_save()` function.

    '''

    if not soup:
        return None

    links = _parse_links(soup)

    all_data = []

    # open link and get its HTML
    for link in links:

        soup = _fetch_url(link)
        if not soup:
            continue

        try:
            name = soup.find("h4", class_=NAME_CLASS)
            price = soup.find("h3", class_=PRICE_CLASS)
            condition_tags =soup.find_all("p", class_=CONDITION_CLASS)[1]
            condition = condition_tags.text.partition(":")[2]
            seller = soup.find("h4", class_=SELLER_CLASS)
        except AttributeError:
            continue

        data = {
            "name" : name.text.strip(),
            "price" : price.text.strip(),
            "condition" : condition.strip(),
            "seller" : seller.text.strip(),
            "link" : link
        }

        all_data.append(data)

    _json_save(all_data)



def average_price(soup: BeautifulSoup):
    '''
    Calculate the average price of all items on the OLX page.

    Parameters
    ----------
    soup: BeautifulSoup
        Parsed HTML of the OLX listing page.

    Return
    -------
    int
        Average price of all items, or None is soup is None.
    
    '''
    if not soup:
        return None
    price_list = _get_prices(soup)
    return int(sum((price_list))/len(price_list)) if price_list else 0



def get_page(query: str, country:str='UA', currency:str='USD', condition:str='all') -> str:
    """
    Builds URL for the website and returns the page

    Parameters
    ----------
    query: str
        Name of an item to be searched.

    country: str
        Country of OLX website.
        UA set as default.        

    currency: str
    Currency that all prices on the website will use.
    USD set as defaut.    
    
    condition: str
        Condition of an item
        All set as default.


    Return
    -------
    BeautifulSoup
        Parsed HTML of the OLX listing page.
    """

    if not query:
        raise ValueError("The 'query' parameter is required and cannot be empty.")

    #Build the URL
    try:
        url = f"https://www.olx{countryDomain[country]}/list/q-{"-".join(query.split())}/{currencyDict[currency]}{conditionDict[condition]}"
    except KeyError as e:
        print(f"Invalid value of {e}\nUse 'help' function to see available parameters")
        return None

    global domain
    domain = countryDomain[country]

    return _fetch_url(url)
