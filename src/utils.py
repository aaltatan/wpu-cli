import os

from playwright.sync_api import Page


def get_authenticated_page(p) -> Page:
    
    browser = p.chromium.launch(slow_mo=10, headless=False)
    page = browser.new_page()
    page.goto("http://edu/")
    
    page.fill('#user_id', os.environ.get('AUTOMATA_USERNAME'))
    page.fill('#password', os.environ.get('AUTOMATA_PASSWORD'))
    page.click('#loginBtn')
    
    return page