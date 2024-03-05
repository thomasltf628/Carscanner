
import requests 
from bs4 import BeautifulSoup 
import pandas as pd 

def get_data():
    url = 'https://www.facebook.com/marketplace/toronto/search/?query=toyota%20camry'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    print(r.status_code)
    return soup

get_data()
