from enum import StrEnum
from pathlib import Path
from typing import Literal, Self

import pandas as pd
from playwright.sync_api import Page
from rich.progress import track
from selectolax.parser import HTMLParser

from cli.edutech.services import PagePipeline

from .schemas import JournalRowSelector, Row


class Chapter(StrEnum):
    ONE = "1"
    TWO = "2"
    THREE = "3"

    def __str__(self) -> str:
        return self.value


class VoucherPagePipeline(PagePipeline):
    def navigate_to_add_new_voucher(self) -> Self:
        self._page.goto("http://edu/RAS/?sc=500#/_FIN/ACT/vouchers.php?id=JOV")
        self._page.wait_for_selector("#addVoucher")
        self._page.click("#addVoucher")
        self._page.wait_for_timeout(3_000)

        return self

    def add_new_rows(self, n: int) -> Self:
        for _ in range(n - 1):
            self._page.press("body", "Shift+N")

        return self

    def fill_row(self, row: Row, automata_row: JournalRowSelector) -> Self:
        self.fill_input(selector=automata_row.debit, value=row.debit)
        self.fill_input(selector=automata_row.credit, value=row.credit)
        self.fill_input(
            selector=automata_row.account_id,
            value=row.account_id,
            kind="select",
        )
        self.fill_input(
            selector=automata_row.cost_center,
            value=row.cost_center,
            kind="select",
        )
        self.fill_input(selector=automata_row.notes, value=row.notes)

        return self


def get_voucher_from_xlsx(filepath: Path, chapter: Chapter) -> list[Row]:
    data = pd.read_excel(filepath).to_dict(orient="records")

    return [
        Row.from_kwargs(
            faculty=row["faculty"],
            chapter=chapter,
            debit=row["debit"],
            credit=row["credit"],
            account_id=row["account_id"],
            notes=row["notes"],
            string_account=row["string_account"],
            faculty_string=row["faculty"],
        )
        for row in data
    ]


def _parse_ids(
    parser: HTMLParser, id_start_with: str, type_: Literal["input", "textarea"] = "input"
) -> list[str]:
    ids = parser.css(f'{type_}[id^="{id_start_with}"]')
    return [el.attributes.get("id") or "" for el in ids][1:]


def _parse_additional_data(parser: HTMLParser) -> list[JournalRowSelector]:
    data: list[JournalRowSelector] = []

    debit_inputs = _parse_ids(parser, "sumDebitId_show")
    credit_inputs = _parse_ids(parser, "sumCreditId_show")
    accounts = _parse_ids(parser, "accountId__label")
    cost_centers = _parse_ids(parser, "costCenterId__label")
    notes = _parse_ids(parser, "detailNote_", type_="textarea")

    for idx in range(len(debit_inputs)):
        row = {
            "debit": debit_inputs[idx],
            "credit": credit_inputs[idx],
            "account_id": accounts[idx],
            "cost_center": cost_centers[idx],
            "notes": notes[idx],
        }
        row = JournalRowSelector(**row)
        data.append(row)

    return data


def add_voucher(
    authenticated_page: Page,
    rows: list[Row],
    financial_year: str,
    timeout_after_inserting_rows: float,
):
    pipeline = (
        VoucherPagePipeline(authenticated_page)
        .navigate_to_general_accounting(financial_year=financial_year)
        .navigate_to_add_new_voucher()
        .add_new_rows(len(rows))
        .wait_for_timeout(int(timeout_after_inserting_rows * len(rows) / 5))
    )

    parser = HTMLParser(pipeline.page.content())
    additional_data = _parse_additional_data(parser)

    for row, automata_row in track(zip(rows, additional_data, strict=False), total=len(rows)):
        pipeline.fill_row(row, automata_row)

    input("Press any key to close ... ")
