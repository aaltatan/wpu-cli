from collections.abc import Generator
from contextlib import contextmanager
from datetime import datetime
from typing import Any, Literal, Self

from playwright.sync_api import Page, sync_playwright


def _login_to_edutech(page: Page, username: str, password: str) -> Page:
    page.wait_for_selector("#login", timeout=60_000)
    page.click("#login")
    page.fill('input[name="user_id"]', username)
    page.fill("#password", password)
    page.click('button[type="submit"]')

    page.wait_for_timeout(10_000)

    return page


@contextmanager
def open_authenticated_edutech_page(username: str, password: str) -> Generator[Page, None, None]:
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(slow_mo=50, headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("http://edu/", timeout=60_000)
    _login_to_edutech(page, username, password)

    try:
        yield page
    finally:
        page.close()
        context.close()
        browser.close()
        playwright.stop()


class PagePipeline:
    def __init__(self, page: Page) -> None:
        self._page = page

    @property
    def page(self) -> Page:
        return self._page

    def select_grid_columns(self, *columns_ids: str) -> Self:
        for column_id in columns_ids:
            self._page.click(f"#{column_id}")
        return self

    def navigate_to_general_accounting(self, financial_year: str) -> Self:
        self._page.goto("http://edu/RAS/?sc=500#/_FIN/ACT/menu.php")
        self.fill_searchbox("#financialYearId_label", financial_year)
        self.wait_for_timeout(4_000)
        return self

    def click(self, selector: str) -> Self:
        self._page.click(selector)
        return self

    def wait_for_timeout(self, timeout: int) -> Self:
        self._page.wait_for_timeout(timeout)
        return self

    def change_pagination_selection(
        self,
        option: Literal["10", "20", "50", "100", "200", "500", "all"],
        timeout: int = 3_000,
    ) -> Self:
        options = {
            "10": "10",
            "20": "20",
            "50": "50",
            "100": "100",
            "200": "200",
            "500": "500",
            "all": "-1",
        }

        self._page.select_option(".ui-pg-selbox", options.get(option, "-1"))
        self._page.wait_for_timeout(timeout)

        return self

    def fill_date_input(self, selector: str, value: datetime) -> Self:
        self._page.fill(selector, value.strftime("%d/%m/%Y"))
        return self

    def fill_searchbox(
        self, selector: str, value: str, *, nth_selected: int = 1, timeout: int = 3_000
    ) -> Self:
        self._page.fill(selector, value)
        self._page.wait_for_timeout(timeout)

        for _ in range(nth_selected):
            self._page.press("body", "ArrowDown")

        self._page.press("body", "Enter")

        return self

    def fill_input(self, selector: str, value: Any) -> Self:
        if value:
            self._page.fill(selector, str(value))

        return self
