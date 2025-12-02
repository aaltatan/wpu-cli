import time
from pathlib import Path
from typing import Any

import xlwings as xw
from loguru import logger
from playwright.sync_api import Page, sync_playwright
from playwright.sync_api._generated import Browser, BrowserContext, Playwright
from rich.progress import track

from .schemas import Message


def _get_messages_from_salaries_file(
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


def get_messages_from_salaries_file(
    fullname: Path,
    password: str,
    sheet_name: str,
    first_cell: tuple[int, int],
    last_column: int,
):
    messages_dict: dict[str, list[str]] = {}

    rg = _get_messages_from_salaries_file(
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


def get_authenticated_whatsapp_page() -> tuple[
    Playwright, Browser, BrowserContext, Page
]:
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(slow_mo=50, headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://web.whatsapp.com", timeout=60_000)

    input("After scanning QR code, Press any key to Continue ... ")

    return playwright, browser, context, page


def close_whatsapp_page(
    playwright: Playwright,
    browser: Browser,
    context: BrowserContext,
    page: Page,
) -> None:
    page.close()
    context.close()
    browser.close()
    playwright.stop()


def send_whatsapp_messages(
    page: Page,
    messages: list[Message],
    timeout_between_messages: float,
    pageload_timeout: float,
) -> None:
    total = len(messages)

    for message in track(messages, description="📩 Sending", total=total):
        try:
            page.goto(
                f"https://web.whatsapp.com/send?phone={message.phone}",
                timeout=60_000,
            )

            for text in message.texts:
                text_input_selector = "footer .lexical-rich-text-input > div"
                page.wait_for_selector(
                    text_input_selector, timeout=pageload_timeout
                )
                page.fill(text_input_selector, text)
                page.click('[aria-label="Send"]')

            time.sleep(timeout_between_messages)

        except Exception as e:  # noqa: BLE001, PERF203
            logger.error(f"Error sending message to {message.phone}: {e}")
            continue
