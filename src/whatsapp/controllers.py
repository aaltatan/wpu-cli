import os
import time
from pathlib import Path

from playwright.sync_api import sync_playwright
from rich.progress import track
import xlwings as xw


def get_messages_from_excel_file(filepath: Path):
    """
    read messages data from salaries/partial file from `whatsapp` sheet
    """
    wb = xw.Book(filepath, password=os.environ.get("EXCEL_PASSWORD"))
    ws = wb.sheets("whatsapp")
    lr = ws.range("A1000000").end("up").row
    rg = ws.range(f"A2:C{lr}").value

    return rg


def send_messages(messages: list[list]) -> None:
    """
    send messages by playwright
    """
    total = len(messages)

    with sync_playwright() as p:

        browser = p.chromium.launch(slow_mo=50, headless=False)
        page = browser.new_page()
        page.goto("https://web.whatsapp.com", timeout=60000)

        input("After scanning QR code, Press any key to Continue ... ")

        for message in track(messages, description="📩 Sending", total=total):

            _, phone, text = message
            
            url: str = f"https://web.whatsapp.com/send?phone={phone}&text={text}"
            try:
                page.goto(url, timeout=60_000)
                btn_selector: str = 'button[aria-label="Send"] span[data-icon="send"]'
                page.is_visible(btn_selector)
                page.click(btn_selector)
                time.sleep(2)
            except:
                continue