# ruff: noqa: B008

from playwright.sync_api import sync_playwright
from typer_di import Depends, TyperDI

from cli.edutech.options import EdutechOptions
from cli.edutech.services import get_edutech_authenticated_page

from .options import AddVouchersOptions
from .services import add_voucher, get_voucher_from_xlsx

app = TyperDI()


@app.callback()
def main() -> None:
    """Add vouchers to edutech."""


@app.command()
def add_salaries(
    options: AddVouchersOptions = Depends(AddVouchersOptions),
    edutech_options: EdutechOptions = Depends(EdutechOptions),
):
    rows = get_voucher_from_xlsx(options.filepath, options.chapter)
    with sync_playwright() as playwright:
        authenticated_page = get_edutech_authenticated_page(
            playwright, edutech_options.username, edutech_options.password
        )
        add_voucher(
            rows=rows,
            authenticated_page=authenticated_page,
            financial_year=edutech_options.financial_year,
            timeout_after_inserting_rows=options.timeout_after_inserting_rows,
        )
