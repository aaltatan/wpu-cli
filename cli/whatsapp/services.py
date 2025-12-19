import time
from typing import Self

from loguru import logger
from playwright.sync_api import Page, sync_playwright
from playwright.sync_api._generated import Browser, BrowserContext, Playwright
from rich.progress import track

from .schemas import Message


class WhatsappSender:
    def __init__(self, timeout_between_messages: float, pageload_timeout: float) -> None:
        playwright, browser, context, page = self._get_authenticated_page()
        self.playwright = playwright
        self.browser = browser
        self.context = context
        self.page = page
        self.timeout_between_messages = timeout_between_messages
        self.pageload_timeout = pageload_timeout

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:  # noqa: ANN001
        self.close()

    def _get_authenticated_page(
        self,
    ) -> tuple[Playwright, Browser, BrowserContext, Page]:
        playwright = sync_playwright().start()
        browser = playwright.chromium.launch(slow_mo=50, headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://web.whatsapp.com", timeout=60_000)

        input("After scanning QR code, Press any key to Continue ... ")

        return playwright, browser, context, page

    def close(self) -> None:
        self.page.close()
        self.context.close()
        self.browser.close()
        self.playwright.stop()

    def _send_single_message(self, message: str) -> None:
        text_input_selector = "footer .lexical-rich-text-input > div"
        self.page.wait_for_selector(text_input_selector, timeout=self.pageload_timeout)
        self.page.fill(text_input_selector, message)
        self.page.click('[aria-label="Send"]')

    def send(self, messages: list[Message]) -> None:
        iterable = track(messages, "📩 Sending", len(messages))

        for message in iterable:
            try:
                url = f"https://web.whatsapp.com/send?phone={message.phone}"
                self.page.goto(url, timeout=60_000)

                for text in message.texts:
                    self._send_single_message(text)

                time.sleep(self.timeout_between_messages)

            except Exception as e:  # noqa: BLE001, PERF203
                logger.error(f"Error sending message to {message.phone}: {e}")
                continue
