import time
from typing import Self

from loguru import logger
from playwright.sync_api import sync_playwright
from rich.progress import track

from .schemas import Message


class WhatsappSession:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(slow_mo=50, headless=False)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()

    def __enter__(self) -> Self:
        self.login()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:  # noqa: ANN001
        self.close()

    def login(self) -> None:
        self.page.goto(self.base_url, timeout=60_000)
        input("After scanning QR code, Press any key to Continue ... ")

    def close(self) -> None:
        self.page.close()
        self.context.close()
        self.browser.close()
        self.playwright.stop()


class WhatsappSender:
    def __init__(
        self, session: WhatsappSession, timeout_between_messages: float, pageload_timeout: float
    ) -> None:
        self.session = session
        self.timeout_between_messages = timeout_between_messages
        self.pageload_timeout = pageload_timeout

    def _send_single_message(self, message: str) -> None:
        text_input_selector = "footer .lexical-rich-text-input > div"
        self.session.page.wait_for_selector(text_input_selector, timeout=self.pageload_timeout)
        self.session.page.fill(text_input_selector, message)
        self.session.page.click('[aria-label="Send"]')

    def _get_send_url(self, message: Message) -> str:
        return f"{self.session.base_url}/send?phone={message.phone}"

    def send(self, messages: list[Message]) -> None:
        for message in track(messages, "📩 Sending", len(messages)):
            try:
                self.session.page.goto(self._get_send_url(message), timeout=60_000)

                for text in message.texts:
                    self._send_single_message(text)

                time.sleep(self.timeout_between_messages)

            except Exception as e:  # noqa: BLE001, PERF203
                logger.error(f"Error sending message to {message.phone}: {e}")
                continue
