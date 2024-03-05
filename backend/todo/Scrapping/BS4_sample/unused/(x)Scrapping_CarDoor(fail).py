import requests
from bs4 import BeautifulSoup
import pandas as pd

searchterm = 'Honda civic sedan'

def search_result_get(searchterm):    
    list_search_item = searchterm.split()
    final_search_term = list_search_item[0]
    list_search_item.pop(0)
    for word in list_search_item:
        final_search_term += "%2520"
        final_search_term += word
    return final_search_term

def get_data(user_input_search):
    url = f'https://www.cardoor.ca/used-vehicles/?q={user_input_search}&_dFR%5Basis_vrp%5D%5B0%5D=Inventory'
    headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/118.0.0.0 Mobile Safari/537.36'}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    print(r.status_code) 
    return soup

def parse(soup):
    productslist = []
    results = soup.find_all('div', {'class': 's-item__info clearfix'})
    for item in results:
        product = {}
        try:
            product['title'] = item.find('div', {'class': 's-item__title'}).text
            soldprice_str = item.find('span', {'class': 's-item__price'}).text.replace('C','').replace('$','').strip()
            product['soldprice'] = float(soldprice_str)
        except ValueError:
            # Skip the item if the price cannot be converted to float
            continue        
        productslist.append(product)
    return productslist

def output(productslist, searchterm):
    productsdf =  pd.DataFrame(productslist)
    productsdf.to_csv(searchterm + 'output.csv', index=False)
    print('Saved to CSV')
    return

soup = get_data(search_result_get)