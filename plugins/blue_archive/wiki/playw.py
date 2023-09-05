import os
import time
import requests
from bs4 import  BeautifulSoup
from playwright.sync_api import sync_playwright

def fetch_dynamic_content(url):
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        page=browser.new_page()
        page.goto(url)
        time.sleep(20)
        page_content=page.content()
        browser.close()
    return page_content
def get_image_urls(page_content):
    soup = BeautifulSoup(page_content, 'html.parser')
    image_urls = [img['src'] for img in soup.find_all('img', src=True)]
    return image_urls

def main():
    url="http://ba.old.gamekee.com/155086.html"
    page_content=fetch_dynamic_content(url)
    image_urls = get_image_urls(page_content)
    for i in image_urls :
        if i.begin_with()
    print(image_urls)
if __name__=="__main__":
    main()