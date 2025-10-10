from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time

def open_page_close_popup_and_click_filters(browser, url):
    browser.get(url)
    close_btn=WebDriverWait(browser, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.cursor-pointer.text-right.mr-4.mt-2"))
        )
    close_btn.click()
    label = WebDriverWait(browser,5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='Speech']")))
    label.click()
    time.sleep(2)