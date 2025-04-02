# Goal of scraping: Getting the latest information of used car on Autotrade platform sales and output to a csv file

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

# As the information of cars are grouped into a block like (Audi A3, 2014) , require regualar expression to break down distinct information into format ( Make: Audi, model: A3, year: 2014)
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

# This website could get location information by direct input of parameter in the url

province = "on"
city = "toronto"
url = f"https://www.autotrader.ca/cars/{province}/{city}"
headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36'}
PATH = "C:/Program Files (x86)/chromedriver.exe"
chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=chrome_options)

driver.get(url)
page_num = 2
max_failures = 5
failures = 0
page_to_scrap = 100
scrap_fail = 0
website = 'autotrader'
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

# Create an empty dataframe
df = pd.DataFrame(data)


while (page_num <= page_to_scrap):
    try:
        # Wait for the main element appear
        text_box = WebDriverWait(driver, timeout=10).until(
                EC.presence_of_element_located((By.ID, "listingsWrapperMainListing"))
            )
        time.sleep(3)
        blocks = text_box.find_elements(By.CLASS_NAME, 'dealer-split-wrapper')

        # Each block refer to one used car, scraping block by block
        for block in blocks:
            try:
                element_position = block.location['y']
                driver.execute_script(f"window.scrollTo(0, {element_position});") # scrolling to next element
                year_make_and_model =  block.find_element(By.CLASS_NAME, 'title-with-trim')
                make, model, year = extract_car_info(year_make_and_model.text)
                year = int(year)
                print(make, model, year)
                price = block.find_element(By.CLASS_NAME, 'price-amount')
                price_todf = price.text

                # Preprocessing of price scrapped
                for char in '$,"':
                    price_todf = price_todf.replace(char, '')
                print(price_todf)
                try:
                    price_todf = int(price_todf)
                except:
                    continue
                
                mileage = block.find_element(By.CLASS_NAME, 'odometer-proximity')
                mileage_todf = mileage.text

                # Preprocessing of mileage scrapped
                for char in 'KM, "':
                    mileage_todf = mileage_todf.replace(char, '')
                print(mileage_todf)
                try:
                    mileage_todf = int(mileage_todf)
                except:
                    continue
                location = block.find_element(By.CLASS_NAME, 'top-detail-area').find_element(By.CLASS_NAME, 'overflow-ellipsis')
                print(location.text)
                listing_date = datetime.date.today()
                link_to_buyer = block.find_element(By.CLASS_NAME, 'inner-link').get_attribute('href')
                print(link_to_buyer)
                
                element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'photo-area')))
                img_element = element.find_element(By.TAG_NAME, 'img')
                link_to_image = img_element.get_attribute('src')
                print(link_to_image)

                
                df.loc[len(df.index)] = [website, make, model, year, price_todf, mileage_todf, location.text,listing_date,link_to_buyer,link_to_image]
            except:
                # Statistic data of failure
                scrap_fail += 1
                print (f'{scrap_fail} piece of information fails to be scrapped')
                continue
            time.sleep(0.5)
        try:
            # Navigate to next page by locating of the next page button
            next = driver.find_element(By.CLASS_NAME, f'page-link-{page_num}')
            page_num += 1
            print(page_num)
            time.sleep(3)
            next.click()
        except NoSuchElementException:
            # Terminate the scraping if next page is not found
            print('404 not found')
            df.to_csv(f'{website}.csv', index=False)
            driver.quit()    
            break
    except Exception as e:
        # Save the current data to csv and auit the Webdriver in case unhandled error happens
        print(f'Exception: {str(e)}')
        failures += 1
        if failures >= max_failures:
            df.to_csv(f'{website}.csv', index=False)
            print(f'Maximum failures ({max_failures}) reached. Exiting...')
            driver.quit()
            break
# Save the current data to csv after the whole sucessful scrapping
df.to_csv(f'{website}.csv', index=False)  



