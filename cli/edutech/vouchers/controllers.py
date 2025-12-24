# ruff: noqa: B008

from typer_di import Depends, TyperDI

from cli.edutech.options import EdutechOptions
from cli.edutech.services import open_authenticated_edutech_page

from .options import AddVouchersOptions
from .services import add_voucher

app = TyperDI()


@app.callback()
def main() -> None:
    """Add vouchers to edutech."""


@app.command()
def add_salaries(
    options: EdutechOptions = Depends(EdutechOptions),
    vouchers_options: AddVouchersOptions = Depends(AddVouchersOptions),
):
    with open_authenticated_edutech_page(options.username, options.password) as page:
        add_voucher(
            rows=vouchers_options.rows,
            authenticated_page=page,
            financial_year=options.financial_year,
            timeout_after_inserting_rows=vouchers_options.timeout_after_inserting_rows,
        )
