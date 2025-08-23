import typer
from rich.progress import track

from src import utils as src_utils

from . import controllers, schemas

app = typer.Typer()
filepath = src_utils.get_salaries_filepath()


@app.command()
def generate_orders(
    start_cell: tuple[int, int] = (2, 1),
    last_column: int = 5,
    sheet_name: str = "orders",
    year: int | None = None,
    month: int | None = None,
):
    """ """
    excel_password: str = typer.prompt("Enter password for excel file", hide_input=True)
    month: int = month or typer.prompt(
        "Enter month (e.g.: 1 for January, 2 for February, etc.)", type=int
    )
    year: int = year or typer.prompt("Enter year (e.g.: 2025)", type=int)

    rows: list[list[str]] = controllers.get_orders_from_excel(
        filepath=filepath,
        password=excel_password,
        start_cell=start_cell,
        last_column=last_column,
        sheet_name=sheet_name,
    )

    for row in track(rows, description="📥 Generating", total=len(rows)):
        serial, name, gender, amount, national_id = row
        order = schemas.PaymentOrder(
            serial=serial,
            name=name,
            gender=gender,
            amount=amount,
            national_id=national_id,
        )
        controllers.generate_order(order, month=month, year=year)
        # controllers.generate_order_voucher(order, month=month, year=year)
