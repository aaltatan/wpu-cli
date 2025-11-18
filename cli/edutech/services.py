from typing import Any, Literal, Self

from playwright.sync_api import Page


class PagePipeline:
    def __init__(self, page: Page, timeout: int) -> None:
        self._page = page
        self.timeout = timeout

    def select_grid_columns(self, *columns_ids: str) -> Self:
        for column_id in columns_ids:
            self._page.click(f"#{column_id}")

        return self

    def navigate_to_general_accounting(self, *, block: bool = True) -> Self:
        self._page.goto("http://edu/RAS/?sc=500#/_FIN/ACT/menu.php")

        if block:
            input("after selecting target year, press any key to continue ... ")

        return self

    def wait_for_timeout(self, timeout: int) -> Self:
        self._page.wait_for_timeout(timeout)
        return self

    def select_all_option(self, timeout: int = 3_000) -> Self:
        self._page.select_option(".ui-pg-selbox", "-1")
        self._page.wait_for_timeout(timeout)
        return self

    def fill_field(
        self,
        value: Any,
        selector: str,
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
