import time
from pathlib import Path

import xlwings as xw
from playwright.sync_api import Page, sync_playwright
from rich.progress import track

from .schemas import Message


def get_messages_from_excel(
    fullname: Path,
    password: str,
    sheet_name: str,
    first_cell: tuple[int, int],
    last_column: int,
) -> list[Message]:
    """
    read messages data from excel file
    """
    wb: xw.Book = xw.Book(fullname, password=password)
    ws: xw.Sheet = wb.sheets(sheet_name)

    last_row: int = ws.range(first_cell).end("down").row
    first_row, first_col = first_cell
    next_row: int = first_row + 1

    rg_values = (next_row, first_col), (last_row, last_column)
    rg: list[list] = ws.range(*rg_values).value

    messages_dict: dict[str, list[str]] = {}

    for row in rg:
        phone, text = row
        if phone in messages_dict:
            messages_dict[phone].append(text)
        else:
            messages_dict[phone] = [text]

    messages: list[Message] = [
        Message(phone, texts) for phone, texts in messages_dict.items()
    ]

    return messages


def _send_message(
    page: Page, message: str, send_btn_selector: str = '[aria-label="Send"]'
) -> None:
    """
    emulating sending single message
    """
    page.fill("footer .lexical-rich-text-input > div", message)
    page.click(send_btn_selector)


def send_messages(messages: list[Message]) -> None:
    """
    send messages by playwright
    """
    total = len(messages)

    with sync_playwright() as p:
        browser = p.chromium.launch(slow_mo=50, headless=False)
        page: Page = browser.new_page()
        page.goto("https://web.whatsapp.com", timeout=60000)

        input("After scanning QR code, Press any key to Continue ... ")

        for message in track(messages, description="📩 Sending", total=total):
            url = f"https://web.whatsapp.com/send?phone={message.phone}"
            try:
                page.goto(url, timeout=60_000)

                for text in message.texts:
                    _send_message(page, text)

                time.sleep(2)

            except Exception:
                continue
