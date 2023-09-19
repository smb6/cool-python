import re
import asyncio
import time

from playwright.sync_api import Page, expect, Playwright, sync_playwright

def find_kamiq(playwright):
    browser = playwright.chromium.launch(headless=False)
    # page = browser.new_page()
    # chromium = playwright.chromium
    # browser = chromium.launch()
    page = browser.new_page()

    page.goto("https://playwright.dev/")

    # Expect a title "to contain" a substring.
    expect(page).to_have_title(re.compile("Playwright"))

    auto_deal = "https://www.auto-deal.co.il/%d7%aa%d7%95%d7%a6%d7%90%d7%95%d7%aa-%d7%97%d7%99%d7%a4%d7%95%d7%a9/"
    page.goto(auto_deal)
    page.locator("#filter-by-make-input").select_option(value="98")
    # page.wait_for_selector()
    time.sleep(5)
    # ll = page.locator("#filter-by-model-input").all_text_contents()
    mm = page.locator("#filter-by-model-input").all_inner_texts()
    pp = mm[0].split('\n')
    # page.get_by_label("filter-by-make-input").select_option(value="98")
    # print(ll)
    if 'פאביה' in pp:
        print('FABIA!!!')
        page.locator("#filter-by-model-input").select_option(value="185")
        time.sleep(10)

    if 'קאמיק' in pp:
        print('KAMIQ!!!')
    print(pp)


if __name__ == '__main__':
    with sync_playwright() as playwright:
        find_kamiq(playwright)