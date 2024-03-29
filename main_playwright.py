import re
import asyncio
import time

import requests
from playwright.sync_api import Page, expect, Playwright, sync_playwright
# from bidi.algorithm import get_display
# import bidiutils

HEB_DEGEM = "דגם"

def find_kamiq(playwright):
    browser = playwright.chromium.launch(headless=True)
    # page = browser.new_page()
    # chromium = playwright.chromium
    # browser = chromium.launch()
    page = browser.new_page()

    # page.goto("https://playwright.dev/")

    # Expect a title "to contain" a substring.
    # expect(page).to_have_title(re.compile("Playwright"))

    auto_deal = "https://www.auto-deal.co.il/%d7%aa%d7%95%d7%a6%d7%90%d7%95%d7%aa-%d7%97%d7%99%d7%a4%d7%95%d7%a9/"
    page.goto(auto_deal)
    page.locator("#filter-by-make-input").select_option(value="98")
    # page.wait_for_selector()
    time.sleep(5)
    # ll = page.locator("#filter-by-model-input").all_text_contents()
    mm = page.locator("#filter-by-model-input").all_inner_texts()
    pp = mm[0].split('\n')
    # page.get_by_label("filter-by-make-input").select_option(value="98")
    # print(ll)\
    pp.remove(HEB_DEGEM)
    print(f"Found {len(pp)} models")
    print(pp)
    if 'פאביה' in pp:
        print('FABIA!!!')
        # page.locator("#filter-by-model-input").select_option(value="185")
        # time.sleep(5)
    else:
        print('\n\nNO FABIA :-(')

    if 'קאמיק' in pp:
        print('\n\nFOUND KAMIQ!!!')
    else:
        print('\n\nNO KAMIQ :-(')

    print("\n\n")
    prod: [{None, None}] = []

    prod.append({'key': 'key', })


if __name__ == '__main__':
    import urllib

    # url = 'https://data.gov.il/api/3/action/datastore_search?resource_id=053cea08-09bc-40ec-8f7a-156f0677aff3&limit=5&q=title:jones'
    # fileobj = urllib.request.urlopen(url)
    # print(fileobj.read())
    CARS_URL = "https://data.gov.il/api/3/action/datastore_search?resource_id=053cea08-09bc-40ec-8f7a-156f0677aff3"
    CARS_URL = "https://data.gov.il/api/3/action/datastore_search?mispar_rechev=5537334"
    response = requests.get(CARS_URL)
    print(response.json())
    # with sync_playwright() as playwright:
    #     find_kamiq(playwright)
