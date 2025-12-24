import random
import time
from collections.abc import Generator
from contextlib import contextmanager
from typing import Protocol

from loguru import logger
from playwright.sync_api import Page, sync_playwright
from playwright_stealth import Stealth
from rich.progress import track

from .schemas import Message


class Timeout(Protocol):
    min_between_messages: float
    max_between_messages: float
    min_send_selector: float
    max_send_selector: float
    pageload: float


@contextmanager
def open_whatsapp_web_page(url: str, pageload_timeout: float) -> Generator[Page, None, None]:
    playwright = Stealth().use_sync(sync_playwright()).manager.start()
    browser = playwright.chromium.launch(slow_mo=50, headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto(url, timeout=pageload_timeout)
    input("After scanning QR code, Press any key to Continue ... ")

    try:
        yield page
    finally:
        page.close()
        context.close()
        browser.close()
        playwright.stop()


def _get_random_timeout(_min: float, _max: float) -> float:
    return random.uniform(_min, _max)  # noqa: S311


def _send_whatsapp_message(page: Page, message: str, timeout: float) -> None:
    text_input_selector = "footer .lexical-rich-text-input > div"
    page.wait_for_selector(text_input_selector, timeout=timeout)
    page.fill(text_input_selector, message)
    page.click('[aria-label="Send"]')


def send_whatsapp_messages_web(page: Page, messages: list[Message], timeout: Timeout) -> None:
    for message in track(messages, "📩 Sending", len(messages)):
        try:
            page.goto(
                f"https://web.whatsapp.com/send?phone={message.phone}", timeout=timeout.pageload
            )

            for text in message.texts:
                input_selector_timeout = _get_random_timeout(
                    timeout.min_send_selector, timeout.max_send_selector
                )

                _send_whatsapp_message(page, text, input_selector_timeout)

            timeout_between_messages = _get_random_timeout(
                timeout.min_between_messages, timeout.max_between_messages
            )

            time.sleep(timeout_between_messages)

        except Exception as e:  # noqa: BLE001, PERF203
            logger.error(f"Error sending message to {message.phone}: {e}")
            continue
