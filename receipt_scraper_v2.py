from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import csv

# Chrome options

def download(i):
    max_retries = 3
    wait = WebDriverWait(driver, 10)
    receipt = wait.until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="root"]/div/div/div/div/div/div[1]/div/div/div/div/div[1]/div[6]/div[1]/div/div/div/div[1]/div/div/div[{i+1}]/div/div[1]/div/div/div[1]/div/div[1]')))
    
    receipt.click()

    time.sleep(1)

    for n in range(max_retries):
        try:
            dwl_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[data-testid='receipt-download-rec']")))

            dwl_button.click()
            break
        except Exception as e:
            if n < max_retries - 1:
                print(f"Error: {e}. retrying...")
                time.sleep(1)
            else:
                print(f"Error: {e}. Maximum number of retries reached.")

    time.sleep(1)

    for n in range(max_retries):
        try:
            close_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[data-testid='close-modal']")))

            close_button.click()
            break

        except Exception as e:
            if n < max_retries - 1:
                print(f"Error: {e}. retrying...")
                time.sleep(1)
            else:
                print(f"Error: {e}. Maximum number of retries reached.")

chrome_options = Options()
#Cookies
chrome_options.add_argument("--user-data-dir=/home/tooshy/.config/google-chrome")
chrome_options.add_argument('--profile-directory=Profile 2')
#Enable when need to check source code
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)

driver.get('https://kyteweb.com/sales')

time.sleep(10)

for i in range(9):

    download(i)

max_retries = 3
for i in range(max_retries):
    try:
        wait = WebDriverWait(driver, 7)
        body = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[data-testid='search-input-sale']")))
        time.sleep(0.2)
        body.click()
        time.sleep(0.2)

        body.send_keys(Keys.PAGE_DOWN)
        break
    except Exception as e:
        if i < max_retries - 1:
            print(f"Error: {e}. retrying...")
            time.sleep(1)
        else:
            print(f"Error: {e}. Maximum number of retries reached.")

time.sleep(1)

#First batch
for i in range(6):
    if i == 5:
        try:
            for i in range(13):
                download(i+3)
                time.sleep(0.2)

        except:
            try:
                for i in range(13):
                    download(i+4)
                    time.sleep(0.2)
            except:
                continue
    try:
        for i in range(12):
            download(i+3)
            time.sleep(0.2)

    except:
        try:
            for i in range(12):
                download(i+4)
                time.sleep(0.2)
        except:
            continue

    max_retries = 3
    for i in range(max_retries):
        try:
            wait = WebDriverWait(driver, 10)
            body = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[data-testid='search-input-sale']")))
            time.sleep(0.2)
            body.click()
            time.sleep(0.2)

            body.send_keys(Keys.PAGE_DOWN)
            break
        except Exception as e:
            if i < max_retries - 1:
                print(f"Error: {e}. retrying...")
                time.sleep(1)
            else:
                print(f"Error: {e}. Maximum number of retries reached.")

    time.sleep(1)

time.sleep(5)

total_scrolls = 70
max_scroll_batch = 7

for batch in range(total_scrolls):
    for scroll in range(max_scroll_batch):
        try:
            for i in range(12):
                download(i+3)
                time.sleep(0.2)

        except:
            for i in range(12):
                download(i+4)
                time.sleep(0.2)

        max_retries = 3
        for i in range(max_retries):
            try:
                wait = WebDriverWait(driver, 10)
                body = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[data-testid='search-input-sale']")))
                time.sleep(0.2)
                body.click()
                time.sleep(0.2)

                body.send_keys(Keys.PAGE_DOWN)
                break
            except Exception as e:
                if i < max_retries - 1:
                    print(f"Error: {e}. retrying...")
                    time.sleep(1)
                else:
                    print(f"Error: {e}. Maximum number of retries reached.")

        time.sleep(1)
    time.sleep(2.5)


