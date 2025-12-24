# ruff: noqa: B008

from devtools import debug
from typer_di import Depends, TyperDI

from cli.edutech.options import EdutechOptions
from cli.edutech.services import open_authenticated_edutech_page

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
    with open_authenticated_edutech_page(options.username, options.password) as page:
        voucher = get_voucher(page, filters, options.financial_year)
        debug(voucher)
