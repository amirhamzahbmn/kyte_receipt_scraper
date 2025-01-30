from playwright.sync_api import sync_playwright, Playwright
import time
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

    filtered_info_bar = page.get_by_test_id('filtered-info-bar').inner_text()
    match = re.search(r'(?<=from\s)([\d,]+(?:\.\d{1,2})?)(?=\ssales)', filtered_info_bar)
    
    receipt_count = match.group(0)

    for x in range(receipt_count):
        sale_row = page.get_by_test_id(f"sale-row-sale-{x}")
        receipt_no = page.get_by_text(re.compile("#", re.IGNORECASE))

        # sale_row.locator(receipt_no)

        receipt_no = sale_row.locator(receipt_no).inner_text()
        
        if receipt_no in downloaded_files:
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