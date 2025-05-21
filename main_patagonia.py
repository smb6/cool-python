from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

PRODUCT_URL = "https://www.patagonia.com/product/mens-strider-pro-running-shorts-5-inch/198077092155.html"
SIZES_TO_CHECK = ["Medium", "XS"]  # sizes we want to test

def check_size_on_sale(size_label_text, driver, wait):
    try:
        # find and click the size button by its label text (case-insensitive)
        size_btn = wait.until(EC.element_to_be_clickable((
            By.XPATH,
            f"//label[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{size_label_text.lower()}')]"
        )))
        size_btn.click()

        # give the page a moment to update
        time.sleep(1)

        # look for a sale price element
        sale_el = driver.find_element(By.CSS_SELECTOR, ".price .sale-price, .price .price-sales")
        return sale_el.text
    except Exception:
        return None

def main():
    # setup headless Chrome
    opts = webdriver.ChromeOptions()
    opts.add_argument("--headless")
    opts.add_argument("--disable-gpu")
    service = ChromeService()  # assumes chromedriver is on PATH
    driver = webdriver.Chrome(service=service, options=opts)
    driver.get(PRODUCT_URL)

    wait = WebDriverWait(driver, 15)

    results = {}
    for size in SIZES_TO_CHECK:
        price = check_size_on_sale(size, driver, wait)
        if price:
            results[size] = f"ON SALE at {price}"
        else:
            results[size] = "Not on sale"

    driver.quit()

    # print summary
    for size, status in results.items():
        print(f"{size}: {status}")

if __name__ == "__main__":
    main()
