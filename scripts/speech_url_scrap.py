import requests
import time
from rollcall.browser_setup import get_browser
from rollcall.speech_filter_action import open_page_close_popup_and_click_filters
from rollcall.scroller import scroll_to_bottom
from rollcall.url_extractor import extract_urls

def main():
    browser = get_browser()
    url = 'https://rollcall.com/factbase/trump/search/'
    open_page_close_popup_and_click_filters(browser, url)
    scroll_to_bottom(browser)
    urls = extract_urls(browser)
    print(urls)

if __name__ == "__main__":
    main()
