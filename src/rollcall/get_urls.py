import requests
from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_experimental_option("detach", True)
path_to_web_driver = chromedriver_autoinstaller.install()
service = Service(executable_path=path_to_web_driver)
browser = webdriver.Chrome(service=service,
                           options=chrome_options)

    

url='https://rollcall.com/factbase/trump/search/'

browser.get(url)
close_btn = browser.find_element(By.CSS_SELECTOR, "div.cursor-pointer.text-right.mr-4.mt-2")
close_btn.click()

label = WebDriverWait(browser,5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='Speech']")))
label.click()

time.sleep(2)

prev_height = 0
while True:
    browser.execute_script("window.scrollBy(0, 3000);")
    time.sleep(2)
    new_height = browser.execute_script("return window.scrollY;")
    if new_height == prev_height:
        break
    prev_height = new_height





