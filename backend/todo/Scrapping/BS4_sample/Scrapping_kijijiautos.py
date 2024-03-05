#This script require multiple scrapping, as only 21 record could be scrappedeach time
#loop over different make and model at a time interval

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

make = "ford"
car_model = "explorer"

def get_data():
    url = f'https://www.kijijiautos.ca/cars'
    headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/118.0.0.0 Mobile Safari/537.36'}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    print(r.status_code) 
    return soup

def parse(soup):
    productslist = []
    results = soup.find_all('div', {'class': 'ccN7dZ'})
    for item in results:
        product = {}
        try:
            product['title'] = item.find('h2', {'class': 'G2jAym fcN7dZ z2jAym p2jAym b2jAym'}).text
            product['soldprice_str'] = item.find('span', {'data-testid': 'searchResultItemPrice'}).text
            product['mile'] = item.find('span', {'data-testid': 'VehicleListItemAttributeValue'}).text
        except ValueError:
            # Skip the item if the price cannot be converted to float
            continue        
        productslist.append(product)
    return productslist

def output(productslist):
    productsdf =  pd.DataFrame(productslist)
    productsdf.to_csv(str(datetime.now().date())  + "_kijijiautos_" + 'output.csv', index=False)
    print('Saved to CSV')
    return

output(parse(get_data()))