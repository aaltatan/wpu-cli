import math
from pathlib import Path
from typing import Literal, Any

import xlwings as xw
from playwright.sync_api import sync_playwright, Page
from selectolax.parser import HTMLParser
from rich.progress import track

from src import utils as src_utils

from .schemas import Row, AutomataRow


def get_voucher_from_excel(
    filepath: Path,
    password: str,
    start_cell: tuple[int, int] = (1, 1),
    last_column: int = 6,
    sheet_name: str = "voucher",
) -> list[list[str]]:
    """
    read voucher data from excel file
    """
    wb = xw.Book(filepath, password=password)
    ws: xw.Sheet = wb.sheets[sheet_name]

    last_row: int = ws.range(start_cell).end("down").row

    start_row, start_col = start_cell
    next_row: int = start_row + 1

    rg_values: tuple[tuple[int, int], tuple[int, int]] = (
        (next_row, start_col),
        (last_row, last_column),
    )

    rg = ws.range(*rg_values).value

    return rg


def get_salaries_voucher_data(
    filepath: Path,
    password: str,
    start_cell: tuple[int, int],
    last_column: int,
    sheet_name: str,
    chapter: Literal["1", "2", "3"],
) -> list[Row]:
    """
    read voucher data from salaries/partial `Journal Entry Template` file
    """
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
    """
    navigate to add new voucher playwright
    """
    page.goto("http://edu/RAS/?sc=500#/_FIN/ACT/vouchers.php?id=JOV")
    page.wait_for_selector("#addVoucher")
    page.click("#addVoucher")

    return page


def _navigate_to_general_accounting(page: Page) -> Page:
    """
    navigate to general accounting to select the current year playwright
    """
    page.goto("http://edu/RAS/?sc=500#/_FIN/ACT/menu.php")
    return page


def _fill_field(
    page: Page,
    value: Any,
    automata_value: Any,
    type_: Literal["select", "input"] = "input",
) -> None:
    """
    fill field
    """
    if value == "":
        return

    page.fill(f"#{automata_value}", str(value))
    if type_ == "select":
        page.wait_for_timeout(3_000)
        page.press("body", "ArrowDown")
        page.press("body", "Enter")


def _fill_row(page: Page, row: Row, automata_row: AutomataRow) -> None:
    """
    fill voucher row
    """
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
    """
    parse all ids from range of fields
    """
    ids = parser.css(f'{type_}[id^="{id_start_with}"]')
    ids = [el.attributes.get("id") for el in ids][1:]

    return ids


def _parse_additional_data(parser: HTMLParser) -> list[AutomataRow]:
    """
    parse all ids from all fields
    """
    data: list[AutomataRow] = []

    debits = _parse_ids(parser, "sumDebitId_show")
    credits = _parse_ids(parser, "sumCreditId_show")
    accounts = _parse_ids(parser, "accountId__label")
    cost_centers = _parse_ids(parser, "costCenterId__label")
    notes = _parse_ids(parser, "detailNote_", type_="textarea")

    for idx in range(len(debits)):
        row = {
            "debit": debits[idx],
            "credit": credits[idx],
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
        page = src_utils.get_authenticated_page(p, username, password)

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

        for row, automata_row in track(zip(data, additional_data), total=total):
            _fill_row(page, row, automata_row)

        input("Press any key to close ... ")
