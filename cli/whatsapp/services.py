import time
from pathlib import Path
from typing import Self

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


class WhatsappSender:
    def __init__(  # noqa: PLR0913
        self,
        playwright: Playwright,
        browser: Browser,
        context: BrowserContext,
        page: Page,
        timeout_between_messages: float,
        pageload_timeout: float,
    ) -> None:
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

    def close(self) -> None:
        self.page.close()
        self.context.close()
        self.browser.close()
        self.playwright.stop()

    def send(self, messages: list[Message]) -> None:
        total = len(messages)

        for message in track(messages, description="📩 Sending", total=total):
            try:
                self.page.goto(
                    f"https://web.whatsapp.com/send?phone={message.phone}",
                    timeout=60_000,
                )

                for text in message.texts:
                    text_input_selector = (
                        "footer .lexical-rich-text-input > div"
                    )
                    self.page.wait_for_selector(
                        text_input_selector, timeout=self.pageload_timeout
                    )
                    self.page.fill(text_input_selector, text)
                    self.page.click('[aria-label="Send"]')

                time.sleep(self.timeout_between_messages)

            except Exception as e:  # noqa: BLE001, PERF203
                logger.error(f"Error sending message to {message.phone}: {e}")
                continue
