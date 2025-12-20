import time
from collections.abc import Generator
from contextlib import contextmanager

from loguru import logger
from playwright.sync_api import Page, sync_playwright
from rich.progress import track

from .schemas import Message


@contextmanager
def open_whatsapp_page(url: str) -> Generator[Page, None, None]:
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(slow_mo=50, headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto(url, timeout=60_000)
    input("After scanning QR code, Press any key to Continue ... ")

    try:
        yield page
    finally:
        page.close()
        context.close()
        browser.close()
        playwright.stop()


def _send_whatsapp_message(page: Page, message: str, timeout: float) -> None:
    text_input_selector = "footer .lexical-rich-text-input > div"
    page.wait_for_selector(text_input_selector, timeout=timeout)
    page.fill(text_input_selector, message)
    page.click('[aria-label="Send"]')


def send_whatsapp_messages(
    page: Page, messages: list[Message], pageload_timeout: float, timeout_between_messages: float
) -> None:
    for message in track(messages, "📩 Sending", len(messages)):
        try:
            page.goto(f"https://web.whatsapp.com/send?phone={message.phone}", timeout=60_000)

            for text in message.texts:
                _send_whatsapp_message(page, text, pageload_timeout)

            time.sleep(timeout_between_messages)

        except Exception as e:  # noqa: BLE001, PERF203
            logger.error(f"Error sending message to {message.phone}: {e}")
            continue
