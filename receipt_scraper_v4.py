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

import os

# Check for already downloaded files
print("Checking for files already downloaded..")
download_path = "/home/tooshy/Downloads/receipts"
dir_list = os.listdir(download_path)

for pdf in range(len(dir_list)):
    dir_list[pdf] = dir_list[pdf].rstrip('.pdf')
    dir_list[pdf] = dir_list[pdf].lstrip('receipt-')

downloaded_files = dir_list

# Chrome options

chrome_options = Options()
#Cookies
chrome_options.add_argument("--user-data-dir=/home/tooshy/.config/google-chrome")
chrome_options.add_argument('--profile-directory=Profile 2')
#Enable when need to check source code
chrome_options.add_experimental_option("detach", True)
# chrome_options.add_argument("--headless=new")

driver = webdriver.Chrome(options=chrome_options)

wait = WebDriverWait(driver, 7)

sale_count = len(downloaded_files)
print(f"Found {len(downloaded_files)} files!")
total_sales = 5843
sales = downloaded_files
failed_sales = []

def get_receipt():
    global sale_count
    rows = driver.find_elements(By.CLASS_NAME, 'table_table-row__14CWi')

    for row in rows:
        MAX_RETRIES = 3
    
        for i in range(MAX_RETRIES):
            try:
                receipt_no = row.find_element(By.CSS_SELECTOR, 'div.css-901oao.css-1hf3ou5.r-1jeb686.r-deyg0r.r-1r11ck1.r-16dba41.r-p1pxzi.r-11wrixw.r-61z16t.r-1mnahxq.r-1ez4vuq.r-13wfysu')
                if receipt_no.text in sales:
                    continue
            except:
                print("Error could not find receipt.. retrying..")
                time.sleep(1)
            else:
                break
        else:
            sale_count += 1
            print(f"Downloading {receipt_no.text}.. {sale_count}/{total_sales}")
            sales.append(receipt_no.text)

            try:
                receipt = row.find_element(By.CSS_SELECTOR, 'div.css-1dbjc4n.r-1awozwy.r-1loqt21.r-xoduu5.r-eqz5dr.r-bnwqim.r-1otgn73')

                driver.execute_script("arguments[0].click();", receipt)

                dwl_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[data-testid='receipt-download-rec']")))
                dwl_button.click()


                time.sleep(0.5)

                close_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[data-testid='close-modal']")))
                close_button.click()

            except:
                failed_sale = sales.pop
                failed_sales.append(failed_sale)
                print(f"Could not download {receipt_no_text}!")
                continue

def filter(period, date):
    try:
        last_date_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f"input[placeholder='{period}']")))
    except:
        last_date_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f"input[value='{period}']")))
    last_date_btn.click()
    previous_month = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "react-datepicker__navigation--previous")))
    time.sleep(0.2)
    current_month = driver.find_element(By.CLASS_NAME, "react-datepicker__current-month").text
    last_sales = date
    while last_sales[-2:] != current_month[-2:]:
        previous_month.click()
        current_month = driver.find_element(By.CLASS_NAME, "react-datepicker__current-month").text
    while last_sales[3:5] != month_converter.get(current_month[:-5]):
        previous_month.click()
        current_month = driver.find_element(By.CLASS_NAME, "react-datepicker__current-month").text
    time.sleep(0.2)
    weeks = driver.find_elements(By.CLASS_NAME, "react-datepicker__week")
    active = True
    for week in weeks:
        days = week.find_elements(By.TAG_NAME, "div")
        for day in days:
            #Used day_no as attributes can't be set
            day_no = day.text
            if len(day.text) == 1:
                day_no = '0' + day.text
            if day_no == last_sales[:2]:
                day.click()
                active = False
                break
        if active == False:
            break

month_converter = {
                    "January":"01",
                    "February":"02",
                    "March":"03",
                    "April":"04",
                    "May":"05",
                    "June":"06",
                    "July":"07",
                    "August":"08",
                    "September":"09",
                    "October":"10",
                    "November":"11",
                    "December":"12",
                  }

driver.get('https://kyteweb.com/sales')

time.sleep(7)

start_date = '01/01/21'
end_date = '12/05/23'
print(f"Starting from {end_date}.")
filter_open = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[data-testid='sale-filter-button']")))
filter_open.click()
filter('Start', start_date)
filter('End', end_date)
filter_close = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[data-testid='modal-cta']")))
filter_close.click()

print("\nContinuing the downloading process..")

get_receipt()

scroll_count = 0

#rearranged cuz filter is using MMDDYY for some reason
prev_end_date = f"{end_date[3:5]}/{end_date[0:2]}/{end_date[-2:]}"

while sale_count != total_sales:

    wait = WebDriverWait(driver, 7)

    MAX_RETRIES = 3
    
    for i in range(MAX_RETRIES):
        try:
            body = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[data-testid='search-input-sale']")))
            time.sleep(0.2)
            body.click()
            time.sleep(0.2)
        except:
            print("Error.. retrying..")
            time.sleep(1)
        else:
            break

    print("\nScrolling..")
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.5)
    body.send_keys(Keys.PAGE_DOWN)
    scroll_count += 1

    time.sleep(0.5)

    get_receipt()

    if scroll_count == 25:
        filter_start_date = start_date[:6] + '20' + start_date[-2:]
        time.sleep(1)
        end_date_find = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.css-901oao.r-1at3fau.r-1471scf.r-deyg0r.r-1r11ck1.r-7sbvxv.r-p1pxzi.r-11wrixw.r-61z16t.r-1mnahxq.r-1ez4vuq.r-13wfysu')))
        end_date = end_date_find.text[:8]
        filter_end_date = prev_end_date[:6] + '20' + prev_end_date[-2:]
        prev_end_date = f"{end_date[3:5]}/{end_date[0:2]}/{end_date[-2:]}"
        print("Its too heavy! Filtering out unneeded sales")
        filter_open = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[data-testid='sale-filter-button']")))
        filter_open.click()
        print(filter_start_date)
        print(filter_end_date)
        filter(filter_start_date, start_date)
        filter(filter_end_date, end_date)
        filter_close = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[data-testid='modal-cta']")))
        filter_close.click()
        back_to_top_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.css-901oao.r-1kihuf0.r-jwli3a.r-deyg0r.r-1gkfh8e.r-majxgm.r-1ilnil2.r-p1pxzi.r-11wrixw.r-61z16t.r-1mnahxq.r-utggzx.r-gy4na3.r-9aemit.r-bnwqim.r-1ez4vuq.r-13wfysu.r-tsynxw")))
        back_to_top_btn.click()
        print("\nContinuing the downloading process..")
        scroll_count = 0

    time.sleep(1)

print(len(sales))

print("All done!")