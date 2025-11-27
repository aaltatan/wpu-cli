import time
from pathlib import Path
from typing import Any

import xlwings as xw
from playwright.sync_api import Page, sync_playwright
from rich.progress import track

from .schemas import Message


def _get_messages_from_excel(
    fullname: Path,
    password: str,
    sheet_name: str,
    first_cell: tuple[int, int],
    last_column: int,
) -> list[Any]:
    wb: xw.Book = xw.Book(fullname, password=password)
    ws = wb.sheets(sheet_name)

    last_row: int = ws.range(first_cell).end("down").row
    first_row, first_col = first_cell
    next_row: int = first_row + 1

    rg_values = (next_row, first_col), (last_row, last_column)
    data = ws.range(*rg_values).value

    if isinstance(data, list):
        return data

    message = "No data found in the specified range."
    raise ValueError(message)


def get_messages_from_excel(
    fullname: Path,
    password: str,
    sheet_name: str,
    first_cell: tuple[int, int],
    last_column: int,
):
    messages_dict: dict[str, list[str]] = {}

    rg = _get_messages_from_excel(
        fullname=fullname,
        password=password,
        sheet_name=sheet_name,
        first_cell=first_cell,
        last_column=last_column,
    )

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


def get_authenticated_whatsapp_page() -> Page:
    with sync_playwright() as p:
        browser = p.chromium.launch(slow_mo=50, headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://web.whatsapp.com", timeout=60_000)

        input("After scanning QR code, Press any key to Continue ... ")

        return page


def send_whatsapp_messages(
    page: Page, messages: list[Message], timeout_between_messages: float
) -> None:
    total = len(messages)

    for message in track(messages, description="📩 Sending", total=total):
        url = f"https://web.whatsapp.com/send?phone={message.phone}"
        try:
            page.goto(url, timeout=60_000)

            for text in message.texts:
                page.fill("footer .lexical-rich-text-input > div", text)
                page.click('[aria-label="Send"]')

            time.sleep(timeout_between_messages)

        except Exception:  # noqa: BLE001, S112
            continue
