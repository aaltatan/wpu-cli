import time
from pathlib import Path
from typing import Any

import xlwings as xw
from playwright.sync_api import sync_playwright
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
    ws = wb.sheets(sheet_name)

    last_row: int = ws.range(first_cell).end("down").row
    first_row, first_col = first_cell
    next_row: int = first_row + 1

    rg_values = (next_row, first_col), (last_row, last_column)
    rg: list[list[Any]] = ws.range(*rg_values).value

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


def send_messages(messages: list[Message]) -> None:
    """
    send messages by playwright sync version
    """
    total = len(messages)

    with sync_playwright() as p:
        browser = p.chromium.launch(slow_mo=50, headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://web.whatsapp.com", timeout=60_000)

        input("After scanning QR code, Press any key to Continue ... ")

        page.context

        for message in track(messages, description="📩 Sending", total=total):
            url = f"https://web.whatsapp.com/send?phone={message.phone}"
            try:
                page.goto(url, timeout=60_000)

                for text in message.texts:
                    page.fill("footer .lexical-rich-text-input > div", text)
                    page.click('[aria-label="Send"]')

                time.sleep(2)

            except Exception:
                continue
