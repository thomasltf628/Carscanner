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

make_list = make_and_model_list()[0]
model_list = make_and_model_list()[1]
years = []
curr_year = int((str(datetime.date.today()))[:4])
for i in range (curr_year - 20, curr_year+1):
    years.append(i)
for index, year in enumerate(years):
    year = str(year)
    years[index] = year

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
province = "on"
city = "toronto"
url = f"https://www.carpages.ca/used-cars/search/?search_radius=100&province_code={province}&city={city}"
PATH = "C:/Program Files (x86)/chromedriver.exe"
chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=chrome_options)

driver.get(url)
page_num = 2
max_failures = 5
failures = 0
page_to_scrap = 50
scrap_fail = 0
website = 'carpages'
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

while (page_num <= page_to_scrap):
    try:
        text_box = WebDriverWait(driver, timeout=10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "main-container"))
            )
        time.sleep(3)
        blocks = text_box.find_elements(By.CLASS_NAME, 't-flex.t-gap-6.t-items-start.t-p-6')
        for block in blocks:
            try:
                element_position = block.location['y']
                driver.execute_script(f"window.scrollTo(0, {element_position});")
                year_make_and_model =  block.find_element(By.TAG_NAME, 'h4')
                make, model, year = extract_car_info(year_make_and_model.text)
                year = int(year)
                print(make, model, year)
                price = block.find_element(By.CLASS_NAME, 't-font-bold.t-text-xl')
                price_todf = price.text
                for char in '$,"':
                    price_todf = price_todf.replace(char, '')
                try:
                    price_todf = int(price_todf)
                except:
                    continue
                mileages = block.find_elements(By.CLASS_NAME, 'number')
                mile = ''
                for mileage in mileages:
                    mile += mileage.text
                """for char in 'KM, "':
                    mile = mile.replace(char, '')"""
                mile = ''.join(filter(str.isdigit, mile))
                print(mile)
                try:
                    mile = int(mile)
                except:
                    continue
                location = block.find_element(By.CLASS_NAME, 'vehicle__card--dealerInfo.t-m-0').find_element(By.TAG_NAME, 'p')
                print(location.text)
                listing_date = datetime.date.today()
                link_plus_img = block.find_element(By.TAG_NAME, 'a')
                link_to_buyer = link_plus_img.get_attribute('href')
                print(link_to_buyer)
                link_to_image = link_plus_img.find_element(By.TAG_NAME, 'img').get_attribute('src')
                print(link_to_image)                
                df.loc[len(df.index)] = [website, make, model, year, price_todf, mile, location.text,listing_date,link_to_buyer,link_to_image]
                time.sleep(0.5)
            except:
                scrap_fail += 1
                print (f'{scrap_fail} piece of information fails to be scrapped')
                continue
    
        try:
            driver.get(f'https://www.carpages.ca/used-cars/search/?num_results=50&search_radius=100&province_code=on&city=toronto&ll=43.6547%2C-79.3623&p={page_num}')
            page_num += 1
            print(page_num)
            time.sleep(1)
        except NoSuchElementException:
            print('404 not found')
            df.to_csv(f'{website}.csv', index=False)
            driver.quit()    
            break
    except Exception as e:
        print(f'Exception: {str(e)}')
        failures += 1
        if failures >= max_failures:
            df.to_csv(f'{website}.csv', index=False)
            print(f'Maximum failures ({max_failures}) reached. Exiting...')
            driver.quit()
            break
df.to_csv(f'{website}.csv', index=False)  