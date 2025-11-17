import math
from pathlib import Path
from typing import Any, Literal

import xlwings as xw
from playwright.sync_api import Page, sync_playwright
from rich.progress import track
from selectolax.parser import HTMLParser

from cli.utils import get_authenticated_page

from .schemas import AutomataRow, Row


def get_voucher_from_excel(
    filepath: Path,
    password: str,
    start_cell: tuple[int, int] = (1, 1),
    last_column: int = 6,
    sheet_name: str = "voucher",
) -> list[list[str]]:
    wb = xw.Book(filepath, password=password)
    ws: xw.Sheet = wb.sheets[sheet_name]

    last_row: int = ws.range(start_cell).end("down").row

    start_row, start_col = start_cell
    next_row: int = start_row + 1

    rg_values: tuple[tuple[int, int], tuple[int, int]] = (
        (next_row, start_col),
        (last_row, last_column),
    )

    return ws.range(*rg_values).value


def get_salaries_voucher_data(  # noqa: PLR0913
    filepath: Path,
    password: str,
    start_cell: tuple[int, int],
    last_column: int,
    sheet_name: str,
    chapter: Literal["1", "2", "3"],
) -> list[Row]:
    rg: list[list[str]] = get_voucher_from_excel(
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


def _navigate_to_add_new_voucher(page: Page) -> Page:
    page.goto("http://edu/RAS/?sc=500#/_FIN/ACT/vouchers.php?id=JOV")
    page.wait_for_selector("#addVoucher")
    page.click("#addVoucher")

    return page


def _navigate_to_general_accounting(page: Page) -> Page:
    page.goto("http://edu/RAS/?sc=500#/_FIN/ACT/menu.php")
    return page


def _fill_field(
    page: Page,
    value: Any,
    automata_value: Any,
    type_: Literal["select", "input"] = "input",
) -> None:
    if value == "":
        return

    page.fill(f"#{automata_value}", str(value))
    if type_ == "select":
        page.wait_for_timeout(3_000)
        page.press("body", "ArrowDown")
        page.press("body", "Enter")


def _fill_row(page: Page, row: Row, automata_row: AutomataRow) -> None:
    _fill_field(page, row.debit, automata_row.debit)
    _fill_field(page, row.credit, automata_row.credit)
    _fill_field(page, row.account_id, automata_row.account_id, type_="select")
    _fill_field(page, row.cost_center, automata_row.cost_center, type_="select")
    _fill_field(page, row.notes, automata_row.notes)


def _parse_ids(
    parser: HTMLParser,
    id_start_with: str,
    type_: Literal["input", "textarea"] = "input",
) -> list[str]:
    ids = parser.css(f'{type_}[id^="{id_start_with}"]')
    return [el.attributes.get("id") for el in ids][1:]


def _parse_additional_data(parser: HTMLParser) -> list[AutomataRow]:
    data: list[AutomataRow] = []

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
        row = AutomataRow(**row)
        data.append(row)

    return data


def add_voucher(
    timeout: int,
    data: list[Row],
    username: str,
    password: str,
):
    with sync_playwright() as p:
        page = get_authenticated_page(p, username, password)

        page.wait_for_timeout(timeout)

        page = _navigate_to_general_accounting(page)

        input("after selecting target year, press any key to continue ... ")

        page = _navigate_to_add_new_voucher(page)

        page.wait_for_timeout(timeout)

        for _ in range(len(data) - 1):
            page.press("body", "Shift+N")

        timeout_factor = math.ceil(len(data) / 10)

        page.wait_for_timeout(timeout * timeout_factor)

        parser = HTMLParser(page.content())

        additional_data = _parse_additional_data(parser)

        total = len(data)

        for row, automata_row in track(
            zip(data, additional_data, strict=True), total=total
        ):
            _fill_row(page, row, automata_row)

        input("Press any key to close ... ")
