from dataclasses import dataclass
from datetime import datetime
from typing import Self

from playwright.sync_api import Page

from cli.edutech.services import PagePipeline

from .exceptions import NoRowsFoundError
from .schemas import JournalRow


@dataclass
class JournalsPageFilters:
    from_date: datetime
    to_date: datetime
    accounts: list[str]


class JournalsPagePipeline(PagePipeline):
    def navigate_to_journals_page(self) -> Self:
        self._page.goto("http://edu/RAS/?sc=500#/_FIN/ACT/journal.php")
        self._page.wait_for_timeout(self.timeout)
        return self

    def fill_date_input(self, selector: str, date: datetime) -> Self:
        date_str = date.strftime("%d/%m/%Y")
        self._page.fill(selector=selector, value=date_str)

        return self

    def click_search_voucher(self) -> Self:
        self._page.click("#searchVoucher")
        return self


def get_journals(
    authenticated_page: Page,
    timeout: int,
    filters: JournalsPageFilters,
):
    pipeline = (
        JournalsPagePipeline(authenticated_page, timeout=timeout)
        .navigate_to_general_accounting()
        .navigate_to_journals_page()
        .select_grid_columns(
            "tAccountName",
            "tAccountNameCode",
            "tVoucherType",
            "tVoucherNumber",
            "costCenterCol",
            "noteCol",
        )
        .fill_date_input("#fromDate", filters.from_date)
        .fill_date_input("#toDate", filters.to_date)
    )

    for account in filters.accounts:
        pipeline.fill_field(account, "#voucherAccountId_label", "select")

    pipeline.click_search_voucher().wait_for_timeout(timeout=5_000)

    with pipeline.page.expect_response(
        "http://edu/RAS/app/_fin/act/views/scripts/journal_grid.php"
    ) as response:
        pipeline.select_all_option(timeout=5_000)
        data = response.value.json()

        if (
            isinstance(data, dict)
            and "rows" in data
            and isinstance(data["rows"], list)
        ):
            return [JournalRow(**row) for row in data["rows"]]

        message = "No rows found"
        raise NoRowsFoundError(message)
