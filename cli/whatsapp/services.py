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


class WhatsappSender:
    def __init__(
        self, page: Page, timeout_between_messages: float, pageload_timeout: float
    ) -> None:
        self.page = page
        self.timeout_between_messages = timeout_between_messages
        self.pageload_timeout = pageload_timeout

    def _send_single_message(self, message: str) -> None:
        text_input_selector = "footer .lexical-rich-text-input > div"
        self.page.wait_for_selector(text_input_selector, timeout=self.pageload_timeout)
        self.page.fill(text_input_selector, message)
        self.page.click('[aria-label="Send"]')

    def send(self, messages: list[Message]) -> None:
        for message in track(messages, "📩 Sending", len(messages)):
            try:
                self.page.goto(
                    f"https://web.whatsapp.com/send?phone={message.phone}", timeout=60_000
                )

                for text in message.texts:
                    self._send_single_message(text)

                time.sleep(self.timeout_between_messages)

            except Exception as e:  # noqa: BLE001, PERF203
                logger.error(f"Error sending message to {message.phone}: {e}")
                continue
