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
    wait = WebDriverWait(driver, 7)
    receipt = wait.until(EC.visibility_of_element_located((By.XPATH, f'//*[@id="root"]/div/div/div/div/div/div[1]/div/div/div/div/div[1]/div[6]/div[1]/div/div/div/div[1]/div/div/div[{i+1}]/div/div[1]/div/div/div[1]/div/div[1]')))

    receipt.click()

    time.sleep(1)

    try:
        dwl_button = driver.find_element(By.XPATH, '/html/body/div[6]/div/div[2]/div/div/div/div[2]/div[3]/div[2]/div[2]/a/div')
    except:
        dwl_button = driver.find_element(By.XPATH, '/html/body/div[7]/div/div[2]/div/div/div/div[2]/div[3]/div[2]/div[2]/a/div')

    dwl_button.click()

    time.sleep(1)

    try:
        close_button = driver.find_element(By.XPATH, '/html/body/div[6]/div/div[2]/div/div/div/div[2]/div[1]/div/div[2]/div')
    except:
        close_button = driver.find_element(By.XPATH, '/html/body/div[7]/div/div[2]/div/div/div/div[2]/div[1]/div/div[2]/div')

    close_button.click()

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

body = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div/div/div/div[1]/div/div/div/div/div[1]/div[2]/div/div/div/div[1]')
body.click()
time.sleep(0.2)
body.send_keys(Keys.PAGE_DOWN)

time.sleep(1)

for i in range(489):
    try:
        for i in range(12):
            download(i+3)
            time.sleep(0.2)

    except:
        for i in range(12):
            download(i+4)
            time.sleep(0.2)

    wait = WebDriverWait(driver, 7)
    body = wait.until(EC.visibility_of_element_located(By.XPATH, '//*[@id="root"]/div/div/div/div/div/div[1]/div/div/div/div/div[1]/div[2]/div/div/div/div[1]'))
    time.sleep(0.2)
    body.click()
    time.sleep(0.2)

    body.send_keys(Keys.PAGE_DOWN)

    time.sleep(1)


