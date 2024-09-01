import os
import time
from pathlib import Path
from urllib.parse import urlencode

from playwright.sync_api import sync_playwright
from rich.progress import track
import xlwings as xw


def get_messages_from_excel_file(filepath: Path) -> list[list]:
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
            params = {"phone": f"+{phone}", "text": text}
            query = urlencode(params)

            try:
                page.goto(
                    f"https://web.whatsapp.com/send?" + query, timeout=60000
                )
                page.is_visible(
                    'button[aria-label="Send"] span[data-icon="send"]'
                )
                page.click(
                    'button[aria-label="Send"] span[data-icon="send"]'
                )
                time.sleep(2)
            except:
                continue
