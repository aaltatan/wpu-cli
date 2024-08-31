import os
from pathlib import Path

import xlwings as xw
from playwright.sync_api import Page


def get_salaries_workbook(filepath: Path) -> xw.Book:
    
    return xw.Book(filepath, password=os.environ.get('EXCEL_PASSWORD'))


def get_authenticated_page(p) -> Page:
    
    browser = p.chromium.launch(slow_mo=10, headless=False)
    page = browser.new_page()
    page.goto("http://edu/")
    
    page.fill('#user_id', os.environ.get('AUTOMATA_USERNAME'))
    page.fill('#password', os.environ.get('AUTOMATA_PASSWORD'))
    page.click('#loginBtn')
    
    return page


def get_salaries_filepath() -> Path:
  
    BASE_DIR = Path().resolve(__file__)
    
    home = BASE_DIR.home()
    desktop_path = home / 'Desktop'
    onedrive_path = Path('D:\\OneDrive\\financial\\In_Progress')

    glob = list(desktop_path.glob('[Salaries|Partial]*.xlsb'))

    if len(glob):
        filepath = glob[0]
    else:
        glob = list(onedrive_path.glob('[Salaries|Partial]*.xlsb'))
        filepath = glob[0]

    return filepath