# yet finish: set location
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import time
from datetime import date
from Model_and_Make_list import make_and_model_list
import re

make_list = make_and_model_list()[0]
model_list = make_and_model_list()[1]

def extract_car_info(car_info):
    
    make_pattern = re.compile(r'\b(?:' + '|'.join(make_list) +r')\b', flags=re.IGNORECASE)
    model_pattern = re.compile(r'\b(?:' + '|'.join(model_list) +r')\b', flags=re.IGNORECASE)
    

    make_match = make_pattern.search(car_info)
    model_match = model_pattern.search(car_info)

    make = make_match.group() if make_match else None
    model = model_match.group() if model_match else None

    return make, model

PATH = "C:/Program Files (x86)/chromedriver.exe"
chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=chrome_options)

locarion_of_searcher ="toronto"
driver.get("https://www.goauto.ca/vehicles?refinementList=%7B%22stock_type%22%3A%5B%22USED%22%5D%7D")
page_num = 2
max_failures = 5
failures = 0
page_to_scrap = 50
scrap_fail = 0
website = 'goauto'
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
    time.sleep(15)
    button_element = driver.find_element(By.CLASS_NAME, 'button_root__ebVgz')
    print('found button')
    time.sleep(3)
    driver.execute_script("arguments[0].click();", button_element)
    print('clicked button')
    time.sleep(3)
    input_area = WebDriverWait(driver, timeout=3).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[placeholder="Search…"]'))
            )
    time.sleep(3)
    input_area.send_keys("")
    time.sleep(3)
    driver.execute_script("arguments[0].value = '';", input_area)
    time.sleep(3)
    input_area.send_keys(locarion_of_searcher)
    time.sleep(2)
    print('entered toronto')
    time.sleep(3)
    submit_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Set my location')]")
    driver.execute_script("arguments[0].click();", submit_button)
    print('clicked')

except:
    print('location already settled')

while (page_num <= page_to_scrap):
    try:
        text_box = WebDriverWait(driver, timeout=10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "inventory_inventoryListing__vHmrR"))
        )
        time.sleep(3)
        blocks = text_box.find_elements(By.CLASS_NAME, 'inventory_inventoryCard__XCsAr')
        for block in blocks:
            try:
                element_position = block.location['y']
                driver.execute_script(f"window.scrollTo(0, {element_position});")
                link = block.find_element(By.CLASS_NAME, 'inventory_imageWrapper__xHDnp')
                link_to_there = link.get_attribute('href')
                print(link_to_there)
                image = WebDriverWait(link, timeout=3).until(
                EC.presence_of_element_located((By.TAG_NAME, 'img'))
                )
                link_to_image = image.get_attribute('src')
                print(link_to_image)
                year = block.find_element(By.CLASS_NAME, 'inventory_content__DIqP5').find_element(By.TAG_NAME, 'span')
                print(year.text)
                make_and_model = block.find_element(By.CLASS_NAME, 'inventory_content__DIqP5').find_element(By.TAG_NAME, 'h4')
                make = extract_car_info(make_and_model.text,)[0]
                print(make)
                model = extract_car_info(make_and_model.text)[1]
                print(model)
                mile = block.find_element(By.CLASS_NAME, 'inventory_content__DIqP5').find_element(By.CLASS_NAME,'inventory_mileage__M6cGj')
                mile_todf = mile.text
                for char in ', km"':
                    mile_todf = mile_todf.replace(char, '')
                print(mile_todf)
                try:
                    mile_todf = int(mile_todf)
                except:
                    continue
                price = block.find_element(By.CLASS_NAME, 'inventory_content__DIqP5').find_element(By.CLASS_NAME,'inventory_pricing__GwjgT')
                price_todf = price.text
                for char in '$,"':
                    price_todf = price_todf.replace(char, '')
                print(price_todf)
                try:
                    price_todf = int(price_todf)
                except:
                    continue
                available = block.find_element(By.CLASS_NAME, 'inventory_content__DIqP5').find_element(By.CLASS_NAME,'inventory_footer__wspJ5').find_element(By.TAG_NAME,'p')

                driver.execute_script("window.scrollBy(0, 175);")
                df.loc[len(df.index)] = [website, make, model, year.text, price_todf, mile_todf, available.text,date.today(),link_to_there,link_to_image]
            except NoSuchElementException:
                scrap_fail += 1
                print (f'{scrap_fail} piece of information fails to be scrapped')
                continue
            time.sleep(0.5)
        try:
            next = driver.find_element(By.XPATH, f"//button[text()='{page_num}']")
            page_num += 1
            print(page_num)
            time.sleep(3)
            next.click()
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
        






