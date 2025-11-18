import math
from enum import StrEnum
from pathlib import Path
from typing import Literal, Self

import xlwings as xw
from playwright.sync_api import Page
from rich.progress import track
from selectolax.parser import HTMLParser

from cli.edutech.services import PagePipeline

from .schemas import JournalRowSelector, Row


class Chapter(StrEnum):
    ONE = "1"
    TWO = "2"
    THREE = "3"


class VoucherPagePipeline(PagePipeline):
    def navigate_to_add_new_voucher(self) -> Self:
        self._page.goto("http://edu/RAS/?sc=500#/_FIN/ACT/vouchers.php?id=JOV")
        self._page.wait_for_selector("#addVoucher")
        self._page.click("#addVoucher")
        self._page.wait_for_timeout(self.timeout)

        return self

    def add_new_rows(self, n: int) -> Self:
        for _ in range(n - 1):
            self._page.press("body", "Shift+N")

        return self

    def fill_row(self, row: Row, automata_row: JournalRowSelector) -> Self:
        self.fill_field(row.debit, automata_row.debit)
        self.fill_field(row.credit, automata_row.credit)
        self.fill_field(row.account_id, automata_row.account_id, kind="select")
        self.fill_field(
            row.cost_center, automata_row.cost_center, kind="select"
        )
        self.fill_field(row.notes, automata_row.notes)

        return self


def get_voucher_from_excel(
    filepath: Path,
    password: str,
    start_cell: tuple[int, int] = (1, 1),
    last_column: int = 6,
    sheet_name: str = "voucher",
):
    wb = xw.Book(filepath, password=password)
    ws: xw.Sheet = wb.sheets[sheet_name]

    last_row: int = ws.range(start_cell).end("down").row

    start_row, start_col = start_cell
    next_row: int = start_row + 1

    rg_values: tuple[tuple[int, int], tuple[int, int]] = (
        (next_row, start_col),
        (last_row, last_column),
    )

    data = ws.range(*rg_values).value

    if isinstance(data, list):
        return data

    message = "Invalid data"
    raise ValueError(message)


def get_salaries_voucher_data(  # noqa: PLR0913
    filepath: Path,
    password: str,
    start_cell: tuple[int, int],
    last_column: int,
    sheet_name: str,
    chapter: Chapter,
) -> list[Row]:
    rg = get_voucher_from_excel(
        filepath=filepath,
        password=password,
        start_cell=start_cell,
        last_column=last_column,
        sheet_name=sheet_name,
    )

    data: list[Row] = []

    for r in rg:
        faculty, string_account, notes, debit, credit, account_id = r

        faculty_string: str = faculty

        row = Row.from_kwargs(
            faculty=faculty,
            chapter=chapter,
            debit=debit,
            credit=credit,
            account_id=account_id,
            notes=notes,
            string_account=string_account,
            faculty_string=faculty_string,
        )
        data.append(row)

    return data


def _parse_ids(
    parser: HTMLParser,
    id_start_with: str,
    type_: Literal["input", "textarea"] = "input",
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
    timeout: int,
    data: list[Row],
):
    total = len(data)
    timeout_factor = math.ceil(len(data) / 10)

    pipeline = (
        VoucherPagePipeline(authenticated_page, timeout=timeout)
        .navigate_to_general_accounting()
        .navigate_to_add_new_voucher()
        .add_new_rows(len(data) - 1)
        .wait_for_timeout(timeout_factor * timeout)
    )

    parser = HTMLParser(pipeline.page.content())
    additional_data = _parse_additional_data(parser)

    for row, automata_row in track(
        zip(data, additional_data, strict=True), total=total
    ):
        pipeline.fill_row(row, automata_row)

    input("Press any key to close ... ")
