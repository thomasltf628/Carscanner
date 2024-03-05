import requests 
from bs4 import BeautifulSoup 
import pandas as pd 

url = "https://www.driveaxis.ca/vehicle-listing/used/ontario-ca-fe8d4a51042?search=MINI%20COOPER"
headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36'}
response = requests.get(url, headers=headers) 
soup = BeautifulSoup(response.content, 'html.parser') 
print(response.status_code) 