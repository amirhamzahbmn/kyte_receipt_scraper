from playwright.sync_api import sync_playwright, Playwright
import time
import os

def run(playwright: Playwright):
    pass
    start_url = "https://web.kyteapp.com/sales"

    user_data_dir = f"C:\\Users\\{os.getlogin()}\\AppData\\Local\\Google\\Chrome\\User Data"
    browser = playwright.chromium.launch_persistent_context(
        user_data_dir=user_data_dir
        ,headless=False
    )
    page = browser.new_page()
    page.goto(start_url)

    for x in range(10):
        sale_row = page.get_by_test_id(f"sale-row-sale-{x}")
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

    time.sleep(2)

with sync_playwright() as playwright:
    run(playwright)