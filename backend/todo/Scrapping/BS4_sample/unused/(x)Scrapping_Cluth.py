
import requests 
from bs4 import BeautifulSoup 
import pandas as pd 

url = "https://www.clutch.ca/cars/toyota-highlander-hybrid"
headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36'}
response = requests.get(url, headers=headers) 
print(response.status_code) 
soup = BeautifulSoup(response.content, 'html.parser') 