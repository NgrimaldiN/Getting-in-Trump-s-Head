import sys,os
sys.path.insert(0,os.path.abspath(os.path.join(os.path.dirname(__file__),'..','src')))
import requests
import time
from rollcall.browser_setup import get_browser
from rollcall.speech_filter_action import open_page_close_popup_and_click_filters
from rollcall.scroller import scroll_to_bottom
from rollcall.url_extractor import extract_urls
from rollcall.storage import store_urls

def main():
    browser = get_browser()
    url = 'https://rollcall.com/factbase/trump/search/'
    open_page_close_popup_and_click_filters(browser, url)
    scroll_to_bottom(browser)
    urls = extract_urls(browser)
    store_urls(urls)

if __name__ == "__main__":
    main()
