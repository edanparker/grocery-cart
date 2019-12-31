import requests
from bs4 import BeautifulSoup

grocery_items_dict = {}


def get_items_from_page(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find_all(attrs={"data-list-name": "catalogProductsList"})
    results_string = str(results)
    name_end_index = 0
    for i in range(24):
        name_start_index = results_string.find("data-product-name", name_end_index, len(results_string)) + 19
        name_end_index = results_string.find("\"", name_start_index, len(results_string))
        grocery_item_name = results_string[name_start_index:name_end_index]
        price_start_index = results_string.find("data-main-price", name_end_index, len(results_string)) + 17
        price_end_index = results_string.find("\"", price_start_index, len(results_string))
        grocery_item_price = float(results_string[price_start_index:price_end_index])
        grocery_items_dict[grocery_item_name] = grocery_item_price


def get_multiple_pages(number_of_pages):
    base_url = "https://www.metro.ca/en/online-grocery/search-page-"
    for i in range(number_of_pages):
        get_items_from_page(base_url + str(i+1))


def lookup_item_in_dict(query):
    result = [key for key, val in grocery_items_dict.items() if query.lower() in key.lower()]
    return "" if result == [] else result[0]


def print_dict():
    for kvp in grocery_items_dict:
        print(kvp + ": " + str(grocery_items_dict[kvp]))


get_multiple_pages(3)
print_dict()

