from playwright.sync_api import sync_playwright, Playwright, expect
import time
import datetime as dt
import os
import re

def run(playwright: Playwright, downloaded_files):
    pass
    start_url = "https://web.kyteapp.com/sales"

    user_data_dir = f"C:\\Users\\{os.getlogin()}\\AppData\\Local\\Google\\Chrome\\User Data"
    browser = playwright.chromium.launch_persistent_context(
        user_data_dir=user_data_dir
        ,headless=False
    )
    page = browser.new_page()
    page.goto(start_url)

    start_date = '01/01/2024'
    end_date = '30/01/2025'

    page.get_by_test_id('sale-filter-button').click()
    page.get_by_placeholder('start').fill(start_date)
    page.get_by_placeholder('end').fill(end_date)
    page.get_by_test_id('modal-cta').click()

    sale_list_header_bar = page.get_by_test_id('sale-list-header-sale')
    date_header = page.get_by_text('Date')
    sale_list_header_bar.locator(date_header).click()

    filtered_info_bar = page.get_by_test_id('filtered-info-bar').inner_text()
    match = re.search(r'(?<=from\s)([\d,]+(?:\.\d{1,2})?)(?=\ssales)', filtered_info_bar)
    
    receipt_count = int(match.group(0))

    print(f'{len(downloaded_files)}/{receipt_count}')

    x = 0

    while len(downloaded_files) != receipt_count:

        # print(x)
        if x == 150:
            sale_row = page.get_by_test_id(f'sale-row-sale-{x}')
            date_info = page.get_by_text('/')

            reset_timestamp = sale_row.locator(date_info).inner_text()
            reset_start_date = re.match(r'^[^,]+', reset_timestamp).group(0)

            reset_start_date = dt.datetime.strptime(reset_start_date, '%d/%m/%y')
            reset_start_date = dt.datetime.strftime(reset_start_date, '%d%m%Y')

            dir_list = os.listdir(download_path)

            for pdf in range(len(dir_list)):
                dir_list[pdf] = dir_list[pdf].rstrip('.pdf')
                dir_list[pdf] = dir_list[pdf].lstrip('receipt-')

            downloaded_files = dir_list

            print(f'{len(downloaded_files)}/{receipt_count}')

            page.reload()

            page.get_by_test_id('sale-filter-button').click()
            page.get_by_placeholder('start').fill(reset_start_date)
            page.get_by_placeholder('end').fill(end_date)
            page.get_by_test_id('modal-cta').click()

            sale_list_header_bar = page.get_by_test_id('sale-list-header-sale')
            date_header = page.get_by_text('Date')
            sale_list_header_bar.locator(date_header).click()

            x = 0
            # time.sleep(10)
        
        page.get_by_test_id(f"sale-row-sale-{x}").scroll_into_view_if_needed()
        sale_row = page.get_by_test_id(f"sale-row-sale-{x}")

        receipt_no = page.get_by_text("#")

        receipt_no = sale_row.locator(receipt_no).inner_text()
        
        if receipt_no in downloaded_files:
            x+=1
            continue

        receipt_button = page.get_by_test_id('sale-receipt-button-sale')

        sale_row.locator(receipt_button).click()

        # Start waiting for the download
        with page.expect_download() as download_info:
            # Perform the action that initiates download
            page.get_by_role('link', name='Download PDF').click()
        download = download_info.value

        # Wait for the download process to complete and save the downloaded file somewhere
        download.save_as("./receipts/" + f'{page.get_by_role('link',name='Download PDF').get_attribute('Download')}.pdf')

        page.get_by_test_id('close-modal').click()

        x += 1

    time.sleep(4)

print("Checking for files already downloaded..")
download_path = r"./receipts"
dir_list = os.listdir(download_path)
print(f"Found {len(dir_list)} files.")

for pdf in range(len(dir_list)):
    dir_list[pdf] = dir_list[pdf].rstrip('.pdf')
    dir_list[pdf] = dir_list[pdf].lstrip('receipt-')

downloaded_files = dir_list
# print(downloaded_files)

with sync_playwright() as playwright:
    run(playwright, downloaded_files)