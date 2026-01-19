# ruff: noqa: B008

from typer_di import Depends, TyperDI

from cli.edutech.options import Edutech
from cli.edutech.services import open_authenticated_edutech_page

from .options import TimeoutAfterInsertingRowsOpt, read_voucher_from_xlsx_wrapper
from .schemas import Row
from .services import add_voucher

app = TyperDI()


@app.callback()
def main() -> None:
    """Add vouchers to edutech."""


@app.command()
def add_salaries(
    timeout_after_inserting_rows: TimeoutAfterInsertingRowsOpt,
    edutech: Edutech = Depends(Edutech),
    rows: list[Row] = Depends(read_voucher_from_xlsx_wrapper),
):
    with open_authenticated_edutech_page(edutech.username, edutech.password) as page:
        add_voucher(
            rows=rows,
            authenticated_page=page,
            financial_year=edutech.financial_year,
            timeout_after_inserting_rows=timeout_after_inserting_rows,
        )
