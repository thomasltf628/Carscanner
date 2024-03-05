import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time

make = "ford"
car_model = "explorer"

def get_data():
    url = f'https://www.goauto.ca/vehicles?refinementList=%7B%22make_name%22%3A%5B%22Audi%22%5D%2C%22model_name%22%3A%5B%22A4%22%5D%7D'
    headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/118.0.0.0 Mobile Safari/537.36'}
    r = requests.get(url, headers=headers)
    print(r.status_code)
    time.sleep(10)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def parse(soup):
    productslist = []
    results = soup.find_all('h4', {'class': 'inventory_makeAndModel__jLJyd typ-body-2 !font-bold'})
    print(len(results))
    """for item in results:
        product = {}
        try:
            product['title'] = item.find('h4', {'class': 'inventory_makeAndModel__jLJyd typ-body-2 !font-bold'}).text
            product['mile'] = item.find('span', {'class': 'inventory_mileage__M6cGj'}).text
            product['soldprice_str'] = item.find('p',{'class':'inventory_pricing__GwjgT typ-body-1 !font-bold'}).text
        except ValueError:
            continue        
        productslist.append(product)
    return productslist"""

def output(productslist):
    productsdf =  pd.DataFrame(productslist)
    productsdf.to_csv(str(datetime.now().date())  + "_GOAUTO_" + 'output.csv', index=False)
    print('Saved to CSV')
    return

def parse2(soup):
    productslist = []
    results = soup.find_all('div', {'class': 'inventory_content__DIqP5'})
    
    if results:
        for result in results:
            # Print or log the content of each result
            print(result.prettify())
    else:
        print("No results found.")

#output(parse(get_data()))

output(parse2(get_data()))

#print(soup.prettify()) 
