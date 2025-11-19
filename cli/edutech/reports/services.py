from dataclasses import dataclass
from datetime import datetime
from typing import Self

from playwright.sync_api import Page

from cli.edutech.services import PagePipeline

from .exceptions import NoRowsFoundError
from .schemas import JournalRow


class JournalsPagePipeline(PagePipeline):
    def navigate_to_journals_page(self) -> Self:
        self._page.goto("http://edu/RAS/?sc=500#/_FIN/ACT/journal.php")
        self._page.wait_for_timeout(3_000)
        return self

    def click_search_voucher(self) -> Self:
        self._page.click("#searchVoucher")
        return self


@dataclass
class JournalsPageFilters:
    from_date: datetime
    to_date: datetime
    accounts: list[str]
    grid_columns: list[str]


def get_journals(
    authenticated_page: Page,
    filters: JournalsPageFilters,
    financial_year: str,
):
    pipeline = (
        JournalsPagePipeline(authenticated_page)
        .navigate_to_general_accounting(financial_year=financial_year)
        .navigate_to_journals_page()
        .select_grid_columns(*filters.grid_columns)
        .fill_date_input("#fromDate", filters.from_date)
        .fill_date_input("#toDate", filters.to_date)
    )

    for account in filters.accounts:
        pipeline.fill_input(
            selector="#voucherAccountId_label", value=account, kind="select"
        )

    pipeline.click_search_voucher().wait_for_timeout(timeout=5_000)

    with pipeline.page.expect_response(
        "http://edu/RAS/app/_fin/act/views/scripts/journal_grid.php"
    ) as response:
        pipeline.select_all_pagination_option(timeout=5_000)
        data = response.value.json()

        if (
            isinstance(data, dict)
            and "rows" in data
            and isinstance(data["rows"], list)
        ):
            return [JournalRow(**row) for row in data["rows"]]

        message = "No rows found"
        raise NoRowsFoundError(message)
