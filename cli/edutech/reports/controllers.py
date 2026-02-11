# ruff: noqa: B008, T201
from dataclasses import dataclass

from typer_di import Depends, TyperDI

from cli.edutech.dependencies import Edutech
from cli.edutech.services import open_authenticated_edutech_page

from .options import AccountsOpt, FromDateOpt, GridColumnsOpt, ToDateOpt
from .services import get_voucher


@dataclass
class VoucherPageFilters:
    from_date: FromDateOpt
    to_date: ToDateOpt
    accounts: AccountsOpt
    grid_columns: GridColumnsOpt


app = TyperDI()


@app.callback()
def main() -> None:
    """Generate reports from edutech."""


@app.command(name="cash")
def generate_cash_report(
    edutech: Edutech = Depends(Edutech), filters: VoucherPageFilters = Depends(VoucherPageFilters)
) -> None:
    """Generate cash report."""
    with open_authenticated_edutech_page(edutech.username, edutech.password) as page:
        voucher = get_voucher(page, filters, edutech.financial_year)
        print(voucher)
