# ruff: noqa: B008

from devtools import debug
from playwright.sync_api import sync_playwright
from typer_di import Depends, TyperDI

from cli.edutech.options import EdutechOptions
from cli.edutech.services import get_edutech_authenticated_page

from .options import VoucherPageFilters
from .services import get_voucher

app = TyperDI()


@app.callback()
def main() -> None:
    """Generate reports from edutech."""


@app.command(name="cash")
def generate_cash_report(
    options: EdutechOptions = Depends(EdutechOptions),
    filters: VoucherPageFilters = Depends(VoucherPageFilters),
) -> None:
    """Generate cash report."""
    with sync_playwright() as playwright:
        authenticated_page = get_edutech_authenticated_page(
            playwright, options.username, options.password
        )
        voucher = get_voucher(authenticated_page, filters, options.financial_year)
        debug(voucher)
