#loop over different make and model at a time interval
#choose place
#solve problem of 21 items by ListItemPage-0,1,2,3,4

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import time
import datetime
from Model_and_Make_list import make_and_model_list
import re
from selenium.webdriver.common.keys import Keys



make_list = make_and_model_list()[0]
model_list = make_and_model_list()[1]
years = []
curr_year = int((str(datetime.date.today()))[:4])
for i in range (curr_year - 20, curr_year+1):
    years.append(i)
for index, year in enumerate(years):
    year = str(year)
    years[index] = year

url = "https://www.kijijiautos.ca/cars/#od=down&sb=rel"
headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36'}
PATH = "C:/Program Files (x86)/chromedriver.exe"
chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=chrome_options)

def extract_car_info(car_info):
    
    make_pattern = re.compile(r'\b(?:' + '|'.join(make_list) +r')\b', flags=re.IGNORECASE)
    model_pattern = re.compile(r'\b(?:' + '|'.join(model_list) +r')\b', flags=re.IGNORECASE)
    year_pattern = re.compile(r'\b(?:' + '|'.join(years) +r')\b', flags=re.IGNORECASE)
    

    make_match = make_pattern.search(car_info)
    model_match = model_pattern.search(car_info)
    year_match = year_pattern.search(car_info)

    make = make_match.group() if make_match else None
    model = model_match.group() if model_match else None
    year = year_match.group() if year_match else None

    return make, model, year

driver.get(url)
max_failures = 5
failures = 0
scrap_fail = 0
max_scrolls = 120
scroll_count = 0    
num_of_page_to_scrap = 50
website = 'kijijiauto'
locarion_of_searcher = 'Toro'
data ={
        'source':[],
        'make':[],
        'model':[],
        'year':[],
        'price':[],
        'mileage':[],
        'location':[],
        'listing_date':[],
        'link_to_buyer':[],
        'link_to_image':[],
    }
df = pd.DataFrame(data)

try:
    button_element = driver.find_element(By.CSS_SELECTOR, '[data-testid="LocationLabelLink"]')
    print('found button')

    driver.execute_script("arguments[0].click();", button_element)
    print('clicked button')

    input_area = WebDriverWait(driver, timeout=10).until(
                EC.presence_of_element_located((By.ID, 'LocationAutosuggest'))
            )
    time.sleep(3)
    input_area.send_keys("")
    time.sleep(3)
    driver.execute_script("arguments[0].value = '';", input_area)
    time.sleep(3)
    input_area.send_keys(locarion_of_searcher)
    time.sleep(2)
    input_area.send_keys(Keys.BACKSPACE * 1)
    time.sleep(3)
    print('entered toronto')
    time.sleep(3)
    submit_button = driver.find_element(By.CSS_SELECTOR, '[data-testid="LocationModalSubmitButton"]')
    driver.execute_script("arguments[0].click();", submit_button)
    print('clicked')

except:
    print('location already settled')

try:
    text_box = WebDriverWait(driver, timeout=10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="SearchResultList"]'))
        )
    time.sleep(3)
    for i in range(num_of_page_to_scrap):
        print(i)
        page = driver.find_element(By.CSS_SELECTOR, f'[data-testid="ListItemPage-{i}"]')
        blocks = page.find_elements(By.TAG_NAME, 'article')
        for block in blocks:
            element_position = block.location['y']
            driver.execute_script(f"window.scrollTo(0, {element_position});")
            try:
                id_car = block.find_element(By.CSS_SELECTOR, '[data-testid="VehicleListItem"]').get_attribute('data-test-ad-id')
                print(id_car)
                link_to_buyer = f'https://www.kijijiautos.ca/vip/{id_car}'
                year_make_and_model =  block.find_element(By.TAG_NAME, 'h2')
                make, model, year = extract_car_info(year_make_and_model.text)
                print(make,model,year)
                price = block.find_element(By.CLASS_NAME, 'mcN7dZ').find_element(By.CSS_SELECTOR, '[data-testid="searchResultItemPrice"]')
                price_todf = price.text
                for char in '$,"':
                    price_todf = price_todf.replace(char, '')
                try:
                    price_todf = int(price_todf)
                except:
                    continue
                mileage_location = block.find_element(By.CLASS_NAME, 'icN7dZ').find_elements(By.TAG_NAME, 'li')
                for index, ele in enumerate (mileage_location):
                    dummy = ele.find_element(By.TAG_NAME, 'span')
                    if index == 0:
                        mileage = dummy.text
                        for char in 'km, "':
                            mileage = mileage.replace(char, '')
                        print(mileage)
                    elif index == 1:
                        location = dummy.text
                        print(location)
                    else:
                        continue
                try:
                    mileage = int(mileage)
                except:
                    continue
                                
                listing_date = datetime.date.today()            
                element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'b1E1YI')))
                img_element = element.find_element(By.TAG_NAME, 'img')
                link_to_image = img_element.get_attribute('src')
                print(link_to_image)
                """driver.execute_script("window.scrollBy(0, 170);")"""
                df.loc[len(df.index)] = [website, make, model, year, price_todf, mileage, location,listing_date,link_to_buyer,link_to_image]
            except:
                scrap_fail += 1
                print (f'{scrap_fail} piece of information fails to be scrapped')
                continue
            time.sleep(1)
        time.sleep(2)
        print('next page')
except Exception as e:
    print(f'Exception: {str(e)}')
    failures += 1
    if failures >= max_failures:
        df.to_csv(f'{website}.csv', index=False)
        print(f'Maximum failures ({max_failures}) reached. Exiting...')
        driver.quit()
df.to_csv(f'{website}.csv', index=False)  
