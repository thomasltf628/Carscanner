from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
def scrapping_carmodel():
    PATH = "C:/Program Files (x86)/chromedriver.exe"
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=chrome_options)

    driver.get("https://www.kbb.com/car-make-model-list/used/view-all/model/")

    table = WebDriverWait(driver, timeout=10).until(
            EC.presence_of_element_located((By.TAG_NAME, "tbody"))
        )
    targets = table.find_elements(By.CLASS_NAME,'css-z687n')

    data ={
        'Make':[],
        'Model':[],
    }
    df = pd.DataFrame(data)

    for index, target in enumerate(targets, start=1):
        if index%3 == 1:
            new_model = target.text
            print(new_model)
        elif index%3 == 2:
            new_make = target.text
            print(new_make)
        else:
            df.loc[len(df.index)] = [new_make, new_model]
            continue
        
                
        time.sleep(0.2)
        driver.execute_script("window.scrollBy(0, 100);")

    df.to_csv('car_data_simple.csv', index=False)
    print("CSV file created successfully.")

    driver.quit()

scrapping_carmodel()