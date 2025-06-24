from pathlib import Path

from playwright.sync_api import Page

BASE_DIR = Path().resolve(__file__).parent.parent

def get_authenticated_page(
    p, username: str, password: str
) -> Page:
    
    browser = p.chromium.launch(slow_mo=10, headless=False)
    page = browser.new_page()
    page.goto("http://edu/")
    
    page.click("#login")
    page.fill('input[name="user_id"]', username)
    page.fill('#password', password)
    page.click('button[type="submit"]')
    
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