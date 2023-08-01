from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementNotInteractableException

import time
import csv

# Chrome options

chrome_options = Options()
#Cookies
chrome_options.add_argument("--user-data-dir=/home/tooshy/.config/google-chrome")
chrome_options.add_argument('--profile-directory=Profile 2')
#Enable when need to check source code
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)

wait = WebDriverWait(driver, 7)

driver.get('https://kyteweb.com/sales')

time.sleep(7)

rows = driver.find_elements(By.CLASS_NAME, 'table_table-row__14CWi')

for row in rows:
    try:

        receipt_element = row.find_element(By.CSS_SELECTOR, 'div.css-1dbjc4n.r-1awozwy.r-1loqt21.r-xoduu5.r-eqz5dr.r-bnwqim.r-1otgn73')
        receipt = wait.until(EC.element_to_be_clickable((receipt_element)))
        receipt.click()

    except:
        action = ActionChains(driver)
        action.move_to_element(receipt).click().perform()

    time.sleep(1)

    dwl_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[data-testid='receipt-download-rec']")))
    dwl_button.click()

    time.sleep(0.5)

    close_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[data-testid='close-modal']")))
    close_button.click()

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

rows = driver.find_elements(By.CLASS_NAME, 'table_table-row__14CWi')

for row in rows:
    if not row.is_displayed():
        continue
    try:
        receipt_element = row.find_element(By.CSS_SELECTOR, 'div.css-1dbjc4n.r-1awozwy.r-1loqt21.r-xoduu5.r-eqz5dr.r-bnwqim.r-1otgn73')
        receipt = wait.until(EC.element_to_be_clickable((receipt_element)))
        receipt.click()

    except:
        action = ActionChains(driver)
        action.move_to_element(receipt).click().perform()

    time.sleep(1)

    dwl_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[data-testid='receipt-download-rec']")))
    dwl_button.click()

    time.sleep(0.5)

    close_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[data-testid='close-modal']")))
    close_button.click()


