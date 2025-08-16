import typer


from . import controllers, schemas

from src import utils as src_utils


app = typer.Typer()
filepath = src_utils.get_salaries_filepath()


@app.command()
def generate_orders(
    start_cell: tuple[int, int] = (2, 1),
    last_column: int = 5,
    sheet_name: str = "orders",
):
    """ """
    excel_password: str = typer.prompt("Enter password for excel file", hide_input=True)
    orders: list[schemas.PaymentOrder] = controllers.get_orders_from_excel(
        filepath=filepath,
        password=excel_password,
        start_cell=start_cell,
        last_column=last_column,
        sheet_name=sheet_name,
    )
    for order in orders:
        controllers.generate_order_template(order)
