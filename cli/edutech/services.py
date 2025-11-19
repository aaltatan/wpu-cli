from datetime import datetime
from typing import Any, Literal, Self

from playwright.sync_api import Page


class PagePipeline:
    def __init__(self, page: Page) -> None:
        self._page = page

    def select_grid_columns(self, *columns_ids: str) -> Self:
        for column_id in columns_ids:
            self._page.click(f"#{column_id}")
        return self

    def navigate_to_general_accounting(self, financial_year: str) -> Self:
        self._page.goto("http://edu/RAS/?sc=500#/_FIN/ACT/menu.php")
        self.fill_input(
            selector="#financialYearId_label",
            value=financial_year,
            kind="select",
        )
        self.wait_for_timeout(4_000)
        return self

    def wait_for_timeout(self, timeout: int) -> Self:
        self._page.wait_for_timeout(timeout)
        return self

    def select_all_pagination_option(self, timeout: int = 3_000) -> Self:
        self._page.select_option(".ui-pg-selbox", "-1")
        self._page.wait_for_timeout(timeout)
        return self

    def fill_date_input(self, selector: str, date: datetime) -> Self:
        date_str = date.strftime("%d/%m/%Y")
        self._page.fill(selector=selector, value=date_str)
        return self

    def fill_input(
        self,
        *,
        selector: str,
        value: Any,
        kind: Literal["select", "input"] = "input",
    ) -> Self:
        if value:
            self._page.fill(selector, str(value))
            if kind == "select":
                self._page.wait_for_timeout(3_000)
                self._page.press("body", "ArrowDown")
                self._page.press("body", "Enter")

        return self

    @property
    def page(self) -> Page:
        return self._page
