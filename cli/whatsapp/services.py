import time
from pathlib import Path

import pandas as pd
from loguru import logger
from playwright.sync_api import Page, sync_playwright
from playwright.sync_api._generated import Browser, BrowserContext, Playwright
from rich.progress import track

from .schemas import Message


def get_messages_from_xlsx(filepath: Path) -> list[Message]:
    messages_dict: dict[str, list[str]] = {}
    data = pd.read_excel(filepath).to_dict(orient="records")

    for row in data:
        phone, text = row.values()
        if phone in messages_dict:
            messages_dict[phone].append(text)
        else:
            messages_dict[phone] = [text]

    return [Message(phone, texts) for phone, texts in messages_dict.items()]


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
