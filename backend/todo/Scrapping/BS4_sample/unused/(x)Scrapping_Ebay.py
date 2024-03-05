import requests
from bs4 import BeautifulSoup
import pandas as pd

searchterm = 'MONITOR'

def get_data(searchterm):
    url = f'https://www.ebay.ca/sch/i.html?_from=R40&_trksid=p4432023.m570.l1313&_nkw={searchterm}&_sacat=0'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
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

soup = get_data(searchterm)
productslist = parse(soup)
output(productslist, searchterm)
"""
            
            'solddate': item.find('span', {'class': 's-item__title--tagblock__COMPLETED'}).find('span', {'class':'POSITIVE'}).text,
            'bids': item.find('span', {'class': 's-item__bids'}).text,
            'link': item.find('a', {'class': 's-item__link'})['href'],"""